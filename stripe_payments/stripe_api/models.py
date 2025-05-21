from django.db import models

class StripePayment(models.Model):
    stripe_session_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.amount} {self.currency} - {self.status}"
