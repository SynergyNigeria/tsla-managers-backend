import random

from django.db import models


def upload_to_application(instance, filename):
    return f"applications/{instance.application_id}/{filename}"


def create_application_id():
    while True:
        application_id = f"TSA-{random.randint(100000, 999999)}"

        if not ManagerApplication.objects.filter(application_id=application_id).exists():
            return application_id


class ManagerApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending review", "Pending review"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    application_id = models.CharField(
        max_length=10,
        unique=True,
        default=create_application_id,
        editable=False,
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="Pending review")
    note = models.TextField(
        default="Your application is pending review. Check this site for updates from the admin team."
    )
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=80)
    showroom = models.CharField(max_length=180)
    networth = models.PositiveIntegerField()
    education = models.CharField(max_length=120)
    management_years = models.CharField(max_length=80)
    management_history = models.TextField(blank=True)
    online_interview = models.CharField(max_length=80)
    car_capacity = models.PositiveIntegerField(blank=True, null=True)
    id_proof = models.FileField(upload_to=upload_to_application)
    cv = models.FileField(upload_to=upload_to_application, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.application_id} - {self.first_name} {self.last_name}"

    def public_payload(self):
        return {
            "id": self.application_id,
            "status": self.status,
            "note": self.note,
            "submittedAt": self.submitted_at.isoformat(),
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "showroom": self.showroom,
            "carCapacity": self.car_capacity,
        }
