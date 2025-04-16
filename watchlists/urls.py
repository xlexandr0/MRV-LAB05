from django.urls import path
from . import views

app_name = 'watchlists'

urlpatterns = [
    path('', views.user_watchlists, name='user_watchlists'),
    path('create/', views.create_watchlist, name='create_watchlist'),
    path('<int:watchlist_id>/', views.watchlist_detail, name='watchlist_detail'),
    path('<int:watchlist_id>/edit/', views.edit_watchlist, name='edit_watchlist'),
    path('<int:watchlist_id>/delete/', views.delete_watchlist, name='delete_watchlist'),
    path('<int:watchlist_id>/add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('item/<int:item_id>/update/', views.update_watchlist_item, name='update_item'),
    path('item/<int:item_id>/delete/', views.delete_watchlist_item, name='delete_item'),
]