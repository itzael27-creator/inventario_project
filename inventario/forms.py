from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'nombre',
            'descripcion',
            'marca',
            'cantidad_min',
            'cantidad_max',
            'precio',
            'stock',
        )
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'cantidad_min': forms.NumberInput(attrs={'min': 0}),
            'cantidad_max': forms.NumberInput(attrs={'min': 0}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'min': 0}),
        }
