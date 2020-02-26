from django.contrib import admin
from common.admin import *

from .models import *

# Register your models here.

class UserQuestionResponseInline(admin.TabularInline):
    model = UserQuestionResponse
    extra = 0

    # Only user can ever change their response
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = [
        'questionText',
        'required',
    ]
