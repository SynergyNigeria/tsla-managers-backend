from django.contrib import admin

from .models import ManagerApplication


@admin.register(ManagerApplication)
class ManagerApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_id",
        "full_name",
        "email",
        "showroom",
        "status",
        "submitted_at",
    )
    list_filter = ("status", "state", "showroom", "submitted_at")
    list_editable = ("status",)
    search_fields = ("application_id", "first_name", "last_name", "email", "phone")
    readonly_fields = ("application_id", "submitted_at", "updated_at")
    fieldsets = (
        ("Admin decision", {"fields": ("status", "note")}),
        (
            "Applicant",
            {
                "fields": (
                    "application_id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "submitted_at",
                    "updated_at",
                )
            },
        ),
        (
            "Location and profile",
            {
                "fields": (
                    "city",
                    "state",
                    "showroom",
                    "networth",
                    "education",
                    "management_years",
                    "management_history",
                    "online_interview",
                    "car_capacity",
                )
            },
        ),
        ("Files", {"fields": ("id_proof", "cv")}),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
