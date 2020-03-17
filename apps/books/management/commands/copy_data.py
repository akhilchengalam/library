from django.core.management.base import BaseCommand
from apps.books.models import Book
import cryptography.fernet


class Command(BaseCommand):

    def handle(self, *args, **options):
        books = Book.objects.all()
        for book in books:
        	book.name1 = book.name
        	book.author1=book.author
        	book.description1 = book.description
        	book.save()
        	print(book.id)
