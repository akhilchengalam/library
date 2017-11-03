from django.contrib import admin
from apps.books.models import Book, BookList, Catagory


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = ('name', 'catagory', 'author', 'photo', 'pdf', 'description')

    class meta:
        model = Book
        exclude = ('slug',)


admin.site.register(Catagory)
admin.site.register(Book, BookAdmin)
admin.site.register(BookList)
