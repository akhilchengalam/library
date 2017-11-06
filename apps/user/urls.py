from django.conf.urls import url
from django.contrib.auth import views as auth_views
from apps.user import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login,{'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{ 'next_page': '/'}, name='logout'),
    url(r'^payment', views.ChargeView.as_view(), name='charge'),
    # url(r"^payments/", include("payments.urls")),
]