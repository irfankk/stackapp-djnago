from django.urls import path, include

from rest_framework import routers

from stackapi import views

router = routers.DefaultRouter()


urlpatterns = [

    path(r'^', include(router.urls)),
    path(r'search', views.SearchView.as_view())

]