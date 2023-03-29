from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


User= get_user_model()

def gen_slug(slug: str) -> str:
    return slugify(slug,allow_unicode=False)


class Product(models.Model):

    name: str = models.CharField(max_length=255)
    price: str = models.CharField(max_length=255)
    rank: float = models.FloatField(default=0)
    user: User = models.ForeignKey(User,on_delete=models.CASCADE)
    category: str = models.ForeignKey('ProductCategory',on_delete=models.CASCADE)

    created_time: timezone = models.DateTimeField(auto_now_add=True)
    updated_time: timezone = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-created_time']



class ProductCategory(models.Model):
    
    name: str = models.CharField(max_length=255)

    def __str__(self):
        return self.pk
    

class WishlistItem(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} -- {self.product.name} -- {self.user.email}"

    def save(self, *args, **kwargs):
        if WishlistItem.objects.filter(user=self.user, product__category=self.product.category).exists():
            raise ValidationError('You can add only one product from each category to your wishlist!')
        super().save(*args, **kwargs)