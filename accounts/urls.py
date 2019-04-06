from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from .views import login,signup,logout

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
] + static(settings.MEDIA_URL, document_root = settings.DEFAULT_FILE_STORAGE)
