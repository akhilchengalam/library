from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime as dt
import requests


class Book(models.Model):
    """
        Stores the details of a book
    """
    name = models.CharField(max_length=162)
    catagory = models.ForeignKey('Catagory', on_delete=models.CASCADE)
    photo = models.URLField(blank=True)
    author = models.CharField(max_length=162)
    published_date = models.DateTimeField(default=dt.now())
    pdf = models.FileField(blank=True, null=False, storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                           upload_to='files', default='/files/book.pdf')
    description = models.TextField(max_length=6000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Catagory(models.Model):
    """
        Book categories
    """
    name = models.CharField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class BookList(models.Model):
    """
        Collecting details from api
    """
    name = models.CharField(max_length=162)
    bookid = models.CharField(max_length=162)
    collected = models.BooleanField(default=False)

    def __str__(self):
       return self.name


@receiver(post_save, sender=BookList)
def my_handler(sender, instance,  **kwargs):
    if instance.collected == False:
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes/"+instance.bookid)
        data = r.json()
        if Catagory.objects.filter(name=data["volumeInfo"]["categories"][0]).exists():
            category=Catagory.objects.get(name=data["volumeInfo"]["categories"][0])
        else:
            category = Catagory.objects.create(name=data["volumeInfo"]["categories"][0])
        book = Book.objects.create(name=data["volumeInfo"]["title"],catagory=category,author=data["volumeInfo"]["authors"][0],
            photo=data["volumeInfo"]["imageLinks"]["thumbnail"],description=data["volumeInfo"]["description"])
        BookList.objects.filter(bookid=instance.bookid).update(collected=True)
        category.save()
        book.save()



