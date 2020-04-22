from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from products.views import home
from accounts.views import login, signup, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home" ),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path(r'^files/', include('db_file_storage.urls')),
]
#+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
