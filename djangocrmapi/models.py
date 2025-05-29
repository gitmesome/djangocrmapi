from django.db import models

class CustomerFormSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=14)  # (123) 456-7890
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)  # 5 or 9 digit ZIP code
    lat = models.FloatField()
    lng = models.FloatField()
    job_type = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    service_date = models.DateTimeField()

    submitted_at = models.DateTimeField(auto_now_add=True)  # Optional: track submission time

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_date.date()}"

