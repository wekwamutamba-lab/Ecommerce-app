# store/models.py
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    BADGE_CHOICES = [
        ('new',  'New'),
        ('sale', 'Sale'),
        ('hot',  'Hot'),
        ('',     'None'),
    ]

    name           = models.CharField(max_length=200)
    description    = models.TextField()
    price          = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image_url      = models.URLField(blank=True)
    category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    badge          = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True)
    is_featured    = models.BooleanField(default=False)
    in_stock       = models.BooleanField(default=True)
    created_at     = models.DateTimeField(default=timezone.now)  # ← fixed line

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        """Calculates % off if original_price is set."""
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return None