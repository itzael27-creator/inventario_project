from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	# Evita mostrar únicamente el ID interno del producto.
	list_display = (
		'nombre',
		'marca',
		'precio',
		'stock',
		'fecha_registro',
	)

	search_fields = ('nombre', 'marca')

	list_filter = ('stock', 'marca')
