from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.home_view, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('search/', views.search_view, name='search'),
    path('lists/', views.lists_view, name='lists'),
    path('list/<int:list_id>/', views.list_details_view, name='list-details'),
    path('list/<int:list_id>/delete/', views.delete_list_view, name='delete-list'),
]
