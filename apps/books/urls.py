from django.conf.urls import url, include
from apps.books import views


urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^book_catagory/(?P<pk>[0-9]+)/$', views.CatagoryView.as_view(), name='catagory'),
    url(r'^book_detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^search', views.Searchview.as_view(), name='search'),

]