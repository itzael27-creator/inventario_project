from rest_framework.routers import DefaultRouter
from inventario.api.views import ProductoViewSet

router = DefaultRouter()
# Genera automáticamente las rutas CRUD bajo /api/productos/.
router.register('productos', ProductoViewSet, basename='producto')
urlpatterns = router.urls
