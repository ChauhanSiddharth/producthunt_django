from django.db import models
from django.contrib.auth.models import User
from db_file_storage.model_utils import delete_file, delete_file_if_needed
from django.core.validators import RegexValidator


# Create your models here.
class Product(models.Model):
    CATEGORIES = (
        ('ELECTRONIC', 'Electronic'),
        ('FURNITURE', 'Furniture'),
        ('JOBS', 'Jobs'),
        ('WEBSITE', 'Website'),
        ('MOBILE APP', 'Mobile App'),
        ('GENERAL','General'),
    )
    title = models.CharField(max_length = 255)
    url = models.URLField(max_length=200, null=True, blank=True,
                          validators=
                            [RegexValidator(
                                regex= '/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/',
                                message='Not a valid URL',
                            )])
    pub_date = models.DateTimeField()
    votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to = 'products.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)
    icon = models.ImageField(upload_to = 'products.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)
    body = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='ELECTRONIC',
    )
    hunter = models.ForeignKey(User, on_delete = models.CASCADE)


    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'image')
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
        delete_file(self, 'image')

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'icon')
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
        delete_file(self, 'icon')

class ConsolePicture(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
