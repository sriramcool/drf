import django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, default=99.99, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 

    @property
    def sale_price(self):
        return f"{float(self.price)*0.2}"

    def get_discount(self):
        return "50%"

    def __str__(self):
        return self.title
