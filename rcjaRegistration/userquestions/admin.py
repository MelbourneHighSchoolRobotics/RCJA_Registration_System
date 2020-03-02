from django.contrib import admin
from common.admin import *

from .models import *

# Register your models here.

class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    readonly_fields = [
        'updatedDateTime',
    ]

    # Only user can ever change their response
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'shortTitle',
        'questionText',
        'required',
    ]