from django.db import models

class Product(models.Model):
    category = models.CharField(max_length=255)  # Changed to JSONField to store a list of categories
    url = models.URLField()
    title = models.TextField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    category_image_url = models.URLField(blank=True, null=True)  # Ensure this field is defined
    price = models.CharField(max_length=255)  # Using CharField to store price as a string
    mrp = models.CharField(max_length=255)  # Using CharField to store MRP as a string
    last_7_day_sale = models.CharField(max_length=25, blank=True, null=True)  # Using CharField
    available_skus = models.JSONField()  # Keeping JSONField to store sizes and colors
    fit = models.CharField(max_length=255, blank=True, null=True)
    fabric = models.CharField(max_length=255, blank=True, null=True)
    neck = models.CharField(max_length=255, blank=True, null=True)
    sleeve = models.CharField(max_length=255, blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()

