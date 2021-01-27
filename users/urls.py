from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view())
]
