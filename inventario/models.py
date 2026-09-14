from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    marca = models.CharField(max_length=50)
    cantidad_min = models.IntegerField()
    cantidad_max = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    # Se asigna una sola vez, cuando el producto se registra.
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Hace que Django muestre el nombre en vez de "Producto object (ID)".
        return self.nombre