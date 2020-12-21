from django.urls import path, include

from rest_framework import routers

from identity import views

router = routers.DefaultRouter()
router.register(r'login', views.UserLoginView, basename='user-login')
router.register(r'register', views.UserCreationView, basename='user-register')



urlpatterns = [

    path(r'', include(router.urls)),

 ]