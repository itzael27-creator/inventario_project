from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


@login_required
def dashboard(request):
    # login_required impide acceder al panel sin iniciar sesión.
    total_productos = Producto.objects.count()
    # Se considera stock bajo cuando hay cinco unidades o menos.
    stock_bajo = Producto.objects.filter(stock__lte=5).count()
    productos_recientes = Producto.objects.order_by('-fecha_registro')[:5]

    contexto = {
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'productos_recientes': productos_recientes,
    }

    return render(
        request,
        'inventario/dashboard.html',
        contexto
    )


@login_required
def lista_productos(request):
    productos = Producto.objects.all()

    return render(
        request,
        'inventario/lista_productos.html',
        {'productos': productos}
    )


@login_required
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_productos')

    return render(request, 'inventario/crear_producto.html', {'form': form})


@login_required
def editar_producto(request, producto_id):
    producto = Producto.objects.filter(id=producto_id).first()
    if producto is None:
        messages.error(request, 'El producto que intentas editar no existe.')
        return redirect('lista_productos')

    # instance permite actualizar el registro actual en vez de crear otro.
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('lista_productos')

    return render(
        request,
        'inventario/crear_producto.html',
        {'form': form, 'modo_edicion': True, 'producto': producto},
    )


@login_required
def eliminar_producto(request, producto_id):
    # Se exige POST para evitar eliminaciones accidentales mediante un enlace GET.
    if request.method == 'POST':
        producto = Producto.objects.filter(id=producto_id).first()
        if producto is not None:
            producto.delete()
        else:
            messages.error(request, 'El producto que intentas eliminar no existe.')

    return redirect('lista_productos')