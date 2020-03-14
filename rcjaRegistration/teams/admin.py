from django.contrib import admin
from common.admin import *
from coordination.adminPermissions import AdminPermissions
from django.contrib import messages

from .models import *

from events.admin import BaseWorkshopAttendanceAdmin

# Register your models here.

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

@admin.register(Team)
class TeamAdmin(BaseWorkshopAttendanceAdmin):
    list_display = [
        'name',
        'event',
        'division',
        'mentorUserName',
        'school',
        'campus',
        'homeState',
    ]
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Event', {
            'fields': ('event', 'division')
        }),
        ('School', {
            'fields': ('mentorUser', 'school', 'campus',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Event', {
            'fields': ('event', 'division')
        }),
        ('School', {
            'description': "Select this team's mentor.<br>If they are a mentor for one school that school will be autofilled. If they are mentor of more than one school you will need to select the school. Leave school blank if independent.<br>You can select campus after you have clicked save.",
            'fields': ('mentorUser', 'school',)
        }),
    )

    inlines = [
        StudentInline
    ]

    search_fields = BaseWorkshopAttendanceAdmin.search_fields + [
        'name',
    ]

    actions = [
        'export_as_csv'
    ]
    exportFields = [
        'event',
        'division',
        'mentorUserName',
        'mentorUserEmail',
        'school',
        'campus',
        'homeState',
    ]

@admin.register(Student)
class StudentAdmin(AdminPermissions, admin.ModelAdmin, ExportCSVMixin):
    list_display = [
        '__str__',
        'team',
    ]
    autocomplete_fields = [
        'team',
    ]
    list_filter = [
        'team__event',
        'team__division',
    ]
    search_fields = [
        'firstName',
        'lastName',
        'team__name',
        'team__school__state__name',
        'team__school__state__abbreviation',
        'team__school__region__name',
        'team__school__name',
        'team__school__abbreviation',
        'team__campus__name',
        'team__mentorUser__first_name',
        'team__mentorUser__last_name',
        'team__mentorUser__email',
        'team__event__name',
        'team__division__name',
    ]
    actions = [
        'export_as_csv'
    ]
    exportFields = [
        'team',
        'firstName',
        'lastName',
        'yearLevel',
        'gender',
        'birthday',
    ]

    # State based filtering

    @classmethod
    def fieldsToFilterRequest(cls, request):
        return [
            {
                'field': 'team',
                'fieldModel': Team,
                'fieldAdmin': TeamAdmin,
            }
        ]

    stateFilterLookup = 'team__event__state__coordinator'
