from django.db import models


CATEGORY_CHOICES = (
    ('Clothing', 'Clothing'),
    ('Fashion', 'Fashion'),
    ('Food', 'Food'),
    ('Housing', 'Housing'),
    ('Music', 'Music'),
    ('Social', 'Social'),
    ('Other', 'Other')
)


class Product(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)


    class Meta:
        db_table = 'Product'
