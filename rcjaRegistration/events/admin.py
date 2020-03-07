from django.contrib import admin
from common.admin import *
from coordination.adminPermissions import AdminPermissions

from .models import *
from regions.models import State

# Register your models here.

@admin.register(DivisionCategory)
class DivisionCategoryAdmin(AdminPermissions, admin.ModelAdmin):
    pass

@admin.register(Division)
class DivisionAdmin(AdminPermissions, admin.ModelAdmin, ExportCSVMixin):
    list_display = [
        'name',
        'state',
        'category',
        'description',
    ]
    search_fields = [
        'name',
        'state__name',
        'state__abbreviation',
        'category__name'
    ]
    list_filter = [
        'category',
        'state',
    ]
    actions = [
        'export_as_csv',
    ]
    exportFields = [
        'name',
        'state',
        'category',
        'description',
    ]

admin.site.register(Year)

class AvailableDivisionInline(admin.TabularInline):
    model = AvailableDivision
    extra = 0
    autocomplete_fields = [
        'division',
    ]

@admin.register(Event)
class EventAdmin(AdminPermissions, admin.ModelAdmin, ExportCSVMixin):
    list_display = [
        'name',
        'eventType',
        'year',
        'state',
        'startDate',
        'endDate',
        'registrationsOpenDate',
        'registrationsCloseDate',
        'directEnquiriesTo'
    ]
    fieldsets = (
        (None, {
            'fields': ('year', ('state', 'globalEvent'), 'name', 'eventType')
        }),
        ('Dates', {
            'fields': ('startDate', 'endDate', 'registrationsOpenDate', 'registrationsCloseDate')
        }),
        ('Team settings', {
            'fields': ('maxMembersPerTeam', 'event_maxTeamsPerSchool', 'event_maxTeamsForEvent',)
        }),
        ('Billing settings', {
            'fields': ('entryFeeIncludesGST', 'event_billingType', 'event_defaultEntryFee', ('event_specialRateNumber', 'event_specialRateFee'), 'paymentDueDate')
        }),
        ('Details', {
            'fields': ('directEnquiriesTo', 'eventDetails', 'location', 'additionalInvoiceMessage')
        }),
    )
    autocomplete_fields = [
        'state',
        'directEnquiriesTo',
    ]
    inlines = [
        AvailableDivisionInline,
    ]
    list_filter = [
        'state',
        'eventType',
        'year',
    ]
    search_fields = [
        'name',
        'state__name',
        'state__abbreviation',
        'directEnquiriesTo__first_name',
        'directEnquiriesTo__last_name',
        'directEnquiriesTo__email',
    ]
    actions = [
        'export_as_csv'
    ]
    exportFields = [
        'name',
        'year',
        'state',
        'startDate',
        'endDate',
        'registrationsOpenDate',
        'registrationsCloseDate',
        'directEnquiriesTo'
    ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':130})},
    }

    # State based filtering

    def fieldsToFilter(self, request):
        from coordination.adminPermissions import reversePermisisons
        from users.models import User
        return [
            {
                'field': 'state',
                'queryset': State.objects.filter(
                    coordinator__user=request.user,
                    coordinator__permissions__in=reversePermisisons(Event, ['add', 'change'])
                )
            },
            {
                'field': 'directEnquiriesTo',
                'queryset': User.objects.filter(
                    homeState__coordinator__user=request.user,
                    homeState__coordinator__permissions__in=reversePermisisons(Event, ['add', 'change'])
                )
            }
        ]

    def stateFilteringAttributes(self, request):
        from coordination.models import Coordinator

        return {
            'state__coordinator__in': Coordinator.objects.filter(user=request.user)
        }
