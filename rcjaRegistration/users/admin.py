from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from .models import User
from coordination.adminPermissions import AdminPermissions
from common.admin import ExportCSVMixin

# Unregister group

admin.site.unregister(Group)

# User admin

class SchoolAdministratorInline(admin.TabularInline):
    from schools.models import SchoolAdministrator
    model = SchoolAdministrator
    extra = 0
    verbose_name = "School administrator of"
    verbose_name_plural = "School administrator of"
    autocomplete_fields = [
        'school',
        'campus',
    ]

class CoordinatorInline(admin.TabularInline):
    from coordination.models import Coordinator
    model = Coordinator
    extra = 0
    verbose_name = "Coordinator of"
    verbose_name_plural = "Coordinator of"

class User_QuestionResponse_Filter(admin.SimpleListFilter):
    title = "Question"
    parameter_name = "question"

    def lookups(self, request, model_admin):
        from userquestions.models import Question
        options = []
        for question in Question.objects.all():
            option = (question.id),question.shortTitle
            options.append(option)
        return options

    def queryset(self, request, queryset):
        try:
            return queryset.filter(questionresponse__response = True, questionresponse__question__id = int(self.value()))
        except (ValueError,TypeError):
            return queryset

@admin.register(User)
class UserAdmin(AdminPermissions, DjangoUserAdmin, ExportCSVMixin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': (
            'email',
            'password'
        )}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'mobileNumber',
            'homeState',
            'homeRegion',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        (_('Flags'), {'fields': (
            'forcePasswordChange',
            'forceDetailsUpdate',
        )}),
        (_('Important dates'), {'fields': (
            'last_login',
            'date_joined',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2'
            ),
        }),
    )
    ordering = ('email',)

    readonly_fields = DjangoUserAdmin.readonly_fields + (
        'user_permissions',
        'groups',
        'last_login',
        'date_joined',
    )
    list_display = [
        'email',
        'first_name',
        'last_name',
        'mobileNumber',
        'homeState',
        'homeRegion',
        'is_staff',
        'is_superuser',
        'is_active',
    ]
    search_fields = [
        'email',
        'first_name',
        'last_name',
        'mobileNumber',
        'homeState__name',
        'homeState__abbreviation',
        'homeRegion__name',
    ]
    list_filter = DjangoUserAdmin.list_filter + (
        'homeState',
        'homeRegion',
        User_QuestionResponse_Filter,
    )
    from userquestions.admin import QuestionResponseInline
    inlines = [
        SchoolAdministratorInline,
        CoordinatorInline,
        QuestionResponseInline,
    ]
    autocomplete_fields = [
        'homeState',
    ]
    actions = [
        'export_as_csv',
        'setForcePasswordChange',
        'setForceDetailsUpdate'
    ]
    exportFields = [
        'email',
        'first_name',
        'last_name',
        'mobileNumber',
        'homeState',
        'homeRegion',
        'is_staff',
        'is_superuser',
        'is_active',
    ]
    exportFieldsManyRelations = ['questionresponse_set']

    # State based filtering

    def fieldsToFilter(self, request):
        from coordination.adminPermissions import reversePermisisons
        from regions.models import State
        return [
            {
                'field': 'homeState',
                'queryset': State.objects.filter(
                    coordinator__user=request.user,
                    coordinator__permissions__in=reversePermisisons(User, ['add', 'change'])
                )
            }
        ]

    def stateFilteringAttributes(self, request):
        from coordination.models import Coordinator
        return {
            'homeState__coordinator__in': Coordinator.objects.filter(user=request.user)
        }

    # Actions

    def setForcePasswordChange(self, request, queryset):
        queryset.update(forcePasswordChange=True)
    setForcePasswordChange.short_description = "Force password change"
    setForcePasswordChange.allowed_permissions = ('change',)

    def setForceDetailsUpdate(self, request, queryset):
        queryset.update(forceDetailsUpdate=True)
    setForceDetailsUpdate.short_description = "Require details update"
    setForceDetailsUpdate.allowed_permissions = ('change',)
