from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from .views import create, detail, upvote

urlpatterns = [
    path('create/', create, name='create'),
    path('<int:product_id>', detail, name='detail'),
    path('<int:product_id>/upvote', upvote, name='upvote'),
] + static(settings.MEDIA_URL, document_root = settings.DEFAULT_FILE_STORAGE)
