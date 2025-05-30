from django.contrib import admin
from django.urls import path, include
from dogcodes import views as dogcodes_views

urlpatterns = [
    path('', dogcodes_views.home_view, name='home'),  # Homepage renders base.html or home.html
    path('admin/', admin.site.urls),
    path('', include('dogcodes.urls')),
    path('signup/', dogcodes_views.signup_view, name='signup'),
    path('login/', dogcodes_views.login_view, name='login'),
    path('logout/', dogcodes_views.logout_view, name='logout'),
    path('search/', dogcodes_views.search_view, name='search'),
    path('lists/', dogcodes_views.lists_view, name='lists'),
    path('list/<int:list_id>/', dogcodes_views.list_details_view, name='list-details'),
    path('list/<int:list_id>/delete/', dogcodes_views.delete_list_view, name='delete-list'),
]
