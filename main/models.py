from django.db import models
from django.urls import reverse
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Category Name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


@receiver(post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файлы с файловой системы при удалении объекта Product.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



class ContactRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        if self.product:
            return f"{self.name} - {self.phone} (Товар: {self.product.name})"
        return f"{self.name} - {self.phone}"
