# from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('engine/', include('apps.engine.urls')),
    path('', include('apps.home.urls')),
    # path('admin/', admin.site.urls),
]
