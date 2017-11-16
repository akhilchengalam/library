from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from apps.books.models import Book, Catagory
from apps.user.models import Profile


class Home(generic.ListView):
    """
        Index page to list latest book collections
    """
    template_name = 'books/index.html'
    model = Book
    context_object_name = 'latest'
    queryset = Book.objects.all().order_by('-published_date')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        cat_list = Catagory.objects.order_by('name')
        context['categories'] = cat_list
        return context


class CatagoryView(generic.ListView):
    """
        Displays category wise books
    """
    template_name = 'books/catagory_list.html'
    model = Catagory
    context_object_name = 'catagory'
    paginate_by = 8

    def get_queryset(self):
        try:
            pk = self.kwargs.get('pk')
            q = self.model.objects.get(pk=int(pk))
            return q.book_set.all()
        except ObjectDoesNotExist:       # AttributeError, DoesNotExist
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['cat'] = self.model.objects.get(pk=int(pk))
        cat_list = Catagory.objects.order_by('name')
        context['categories'] = cat_list
        obj=Catagory.objects.get(id=pk)
        context['cat_name'] = obj.name
        return context


class DetailView(generic.DetailView):
    """
        Dispaly the details of a book
    """
    model = Book
    template_name = 'books/detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_list = Catagory.objects.order_by('name')
        context['categories'] = cat_list
        return context


class Searchview(generic.ListView):
    """
        Dispaly the search results
    """
    model = Book
    template_name = 'books/search_results.html'
    context_object_name = 'search_books'
    paginate_by = 8

    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(name__icontains=self.request.GET['key'])

    def get_context_data(self):

        context = super().get_context_data()
        cat_list = Catagory.objects.order_by('name')
        context['categories'] = cat_list
        context['key'] = self.request.GET['key']
        return context