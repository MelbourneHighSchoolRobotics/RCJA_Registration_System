from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from common.models import *
from django.utils.translation import ugettext_lazy as _


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
    homeState = models.ForeignKey('regions.State', verbose_name='Home state', on_delete=models.PROTECT, null=True, blank=True)
    homeRegion = models.ForeignKey('regions.Region', verbose_name='Home region', on_delete=models.PROTECT, null=True, blank=True)

    # Preferences and settings
    currentlySelectedSchool = models.ForeignKey('schools.School', verbose_name='Currently selected school', on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    # *****Clean*****

    def clean(self):
        super().clean()
        # Force case insentive email
        if User.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('User with this Email address already exists.')})

    # *****Permissions*****

    # *****Save & Delete Methods*****

    # *****Methods*****

    # *****Get Methods*****

    def fullname_or_email(self):
        return self.get_full_name() or self.email

    # *****CSV export methods*****

    # *****Email methods*****
