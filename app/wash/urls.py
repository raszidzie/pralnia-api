from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wash import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('clothes', views.ClotheViewSet)

app_name = 'wash'

urlpatterns = [
    path('', include(router.urls))
]