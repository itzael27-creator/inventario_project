#RUTAS PRINCIPALES
from django.contrib import admin  # Permite conservar la ruta /admin/ de Django.
from django.urls import path, include  # Declara rutas e incorpora otras configuraciones.

urlpatterns = [
    # Panel administrativo original de Django; se conserva como herramienta auxiliar.
    path('admin/', admin.site.urls),
    # Incluye la API REST existente bajo el prefijo /api/.
    path('api/', include('inventario.api.urls')),
    # Incluye las rutas HTML de la app inventario desde la raiz del sitio.
    path('', include('inventario.urls')),
    # Incluye login, logout y otras vistas de autenticacion de Django.
    path('accounts/', include('django.contrib.auth.urls')),
]
