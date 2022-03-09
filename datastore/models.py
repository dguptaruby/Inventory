from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username

class Company(models.Model):
    title = models.CharField(max_length=200, help_text="Company Name")
    description = models.TextField(help_text="Company Description")
    address = models.TextField(help_text="Company Address")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Product(models.Model):
    barcode = models.CharField(max_length=13,help_text="Product Barcode")
    title = models.CharField(max_length=200, help_text="Product Title")
    description = models.TextField(help_text="Product Description")
    price = models.FloatField(help_text="Product Cost")
    quantity = models.FloatField(help_text="Enter Product Quantity")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Store(models.Model):
    title = models.CharField(max_length=200, help_text="Store Name")
    address = models.TextField(help_text="Store address")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return self.title