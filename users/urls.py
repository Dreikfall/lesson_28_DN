from django.urls import path, include

from users import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('delete/', views.UserDeleteView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('<int:pk>/update/', views.UserUpdateView.as_view())
]