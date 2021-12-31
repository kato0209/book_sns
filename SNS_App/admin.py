from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username','ProfileImage']

    fieldsets = UserAdmin.fieldsets + (
            ('profile-image', {'fields': ('ProfileImage',)}),
    )

class MemberInlineAdmin(admin.TabularInline):
    model = Room.room_member.through

class RoomAdmin(admin.ModelAdmin):
    inlines = (MemberInlineAdmin,)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TweetModel)
admin.site.register(Like)
admin.site.register(Connection)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Room,RoomAdmin)
admin.site.register(Message)
admin.site.register(Entries)