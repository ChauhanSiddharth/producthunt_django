from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from .views import login,signup,logout, myprofile, deletePost, editPost, addInfo

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/', myprofile, name='profile'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('addinfo/', addInfo ,name='addinfo'),
    path('<int:product_id>/delete', deletePost, name='delete'),
    path('<int:product_id>/updatepost', editPost, name='updatePost'),
] + static(settings.MEDIA_URL, document_root = settings.DEFAULT_FILE_STORAGE)
