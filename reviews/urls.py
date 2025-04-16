from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('movie/<int:movie_id>/', views.movie_reviews, name='movie_reviews'),
    path('add/<int:movie_id>/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('vote/<int:review_id>/', views.review_vote, name='review_vote'),
    path('comment/<int:review_id>/', views.add_comment, name='add_comment'),
]