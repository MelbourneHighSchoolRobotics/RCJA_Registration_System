from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import django.apps as djangoApps

from django.contrib.auth.models import Permission
from coordination.models import Coordinator

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        # Case insensitive username lookup
        return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': username})

class User(AbstractUser):
    """User model"""
    # Replace username with email
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Custom manager because no username field
    objects = UserManager()

    # Additional fields
    mobileNumber = models.CharField('Mobile number', max_length=12, null=True, blank=True)
    homeState = models.ForeignKey('regions.State', verbose_name='Home state', on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'typeRegistration': True})
    homeRegion = models.ForeignKey('regions.Region', verbose_name='Home region', on_delete=models.PROTECT, null=True, blank=True)

    # Preferences and settings
    currentlySelectedSchool = models.ForeignKey('schools.School', verbose_name='Currently selected school', on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    # Flags
    forcePasswordChange = models.BooleanField('Force password change', default=False)
    forceDetailsUpdate = models.BooleanField('Force details update', default=False)

    # For axes to work
    backend = 'axes.backends.AxesBackend'

    # *****Clean*****

    def clean(self):
        super().clean()
        # Force case insentive email
        if User.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('User with this email address already exists.')})

    # *****Permissions*****
    @classmethod
    def coordinatorPermissions(cls, level):
        if level in ['full']:
            return [
                'add',
                'view',
                'change',
            ]
        elif level in ['viewall', 'eventmanager', 'schoolmanager', 'billingmanager', 'webeditor']:
            return [
                'view',
            ]
        
        return []

    # Used in state coordinator permission checking
    def getState(self):
        return self.homeState

    # *****Save & Delete Methods*****

    # *****Methods*****

    def updateUserPermissions(self):
        # Get coordinator objects for this user
        coordinators = Coordinator.objects.filter(user=user)

        # Staff flag
        user.is_staff = user.is_superuser or coordinators.exists()
        user.save()

        # Permissions

        # Get permissions for all models for all states that this user is a coordinator of
        permissionsToAdd = []

        for coordinator in coordinators:
            for model in djangoApps.apps.get_models():
                if hasattr(model, 'coordinatorPermissions'):
                    permissionsToAdd += map(lambda x: f'{x}_{model._meta.object_name.lower()}', getattr(model, 'coordinatorPermissions')(coordinator.permissions))

        # Add permissions to user
        permissionObjects = Permission.objects.filter(codename__in=permissionsToAdd)
        user.user_permissions.clear()
        user.user_permissions.add(*permissionObjects)

    # Reset forcePasswordChange
    def set_password(self, password):
        super().set_password(password)
        self.forcePasswordChange = False

    def setCurrentlySelectedSchool(self):
        # Set currentlySelectedSchool to another school for this user or None if no other schools
        if self.schooladministrator_set.exists():
            self.currentlySelectedSchool = self.schooladministrator_set.first().school
        else:
            self.currentlySelectedSchool = None
        self.save(update_fields=['currentlySelectedSchool'])

    # *****Get Methods*****

    def fullname_or_email(self):
        return self.get_full_name() or self.email

    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()} ({self.email})"
        return self.email

    # *****CSV export methods*****

    # *****Email methods*****
