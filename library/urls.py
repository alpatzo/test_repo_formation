from django.urls import path
from . import views

urlpatterns = [
    path('all_books', views.get_all_books, name="all_books"),
    path('get_book/<int:pk>', views.get_book, name="get_book"),
    path('delete/<int:book_id>',views.delete_book, name="delete_book"),
    path('create',views.create_book, ),
    path('update',views.update_book, )
]