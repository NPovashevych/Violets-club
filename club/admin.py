from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from club.models import Variety, Violet, Status, Member


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Violet)
class VioletAdmin(admin.ModelAdmin):
    list_filter = ("variety",)
    search_fields = ("sort",)


@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "experience",
        "status",
        "country",
        "city",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": (
            "experience",
            "status",
            "country",
            "city",)}
         ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": (
            "experience",
            "status",
            "country",
            "city",)}
         ),
    )
