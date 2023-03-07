from django.urls import (path, include,)
from rest_framework.routers import DefaultRouter
from books import views



router = DefaultRouter()

router.register('profile', views.UserProfileViewSet)
router.register('books', views.BooksViewSet, basename='books')
router.register('categories', views.CategoryViewSet)
router.register('editors', views.EditorViewSet)

app_name = 'books'

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('read-books/', views.ReadBooksView.as_view()),
    path('read-books/add/', views.ReadBooksAddView.as_view()),
    path('read-books/<int:pk>/', views.ReadBooksDeleteView.as_view()),
    path('', include(router.urls)),
]

