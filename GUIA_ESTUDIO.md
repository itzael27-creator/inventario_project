# Guia de estudio del sistema de inventario

Este documento explica el proyecto existente y los cambios realizados para construir el panel personalizado. El panel HTML usa la app `inventario`; la carpeta `productos` existente no participa en este flujo.

## 1. Estructura principal

```text
inventario_project/
├── manage.py                         # Entrada para ejecutar comandos Django
├── inventario_project/
│   ├── settings.py                   # Configuracion global
│   └── urls.py                       # Rutas generales del proyecto
├── inventario/
│   ├── models.py                     # Modelo Producto
│   ├── forms.py                      # Formulario basado en Producto
│   ├── views.py                      # Logica del panel
│   ├── urls.py                       # Rutas de la app
│   ├── api/                          # API REST existente
│   ├── migrations/                   # Historial de cambios de la BD
│   ├── templates/
│   │   ├── registration/login.html   # Login que usa Django
│   │   └── inventario/               # Templates del panel
│   └── static/inventario/assets/     # CSS, JavaScript, librerias e imagenes
└── GUIA_ESTUDIO.md
```

Django busca templates dentro de `templates/` y archivos estaticos dentro de `static/` cuando `APP_DIRS = True` y `django.contrib.staticfiles` esta instalado.

## 2. Recorrido de una peticion

### Usuario no autenticado

1. El navegador solicita `/`.
2. `inventario_project/urls.py` envia la peticion a `inventario/urls.py`.
3. La ruta vacia (`''`) llama a `views.dashboard`.
4. `@login_required` detecta que no hay sesion.
5. Django redirige a `/accounts/login/`, segun `LOGIN_URL`.
6. Django busca exactamente `inventario/templates/registration/login.html`.

### Usuario autenticado

1. El formulario de login envia usuario, contrasena y token CSRF mediante POST.
2. Django valida las credenciales y crea la sesion.
3. `LOGIN_REDIRECT_URL = '/'` envia al usuario al dashboard.
4. `dashboard()` consulta `Producto` y envia los resultados a `dashboard.html`.

### Cerrar sesion

`base.html` envia un formulario POST a la URL con nombre `logout`. Django elimina la sesion y redirige a `/accounts/login/`, segun `LOGOUT_REDIRECT_URL`.

## 3. Modelo: `inventario/models.py`

`Producto` representa una fila de la tabla de productos.

- `nombre`: texto de hasta 100 caracteres.
- `descripcion`: texto largo.
- `marca`: texto de hasta 50 caracteres.
- `cantidad_min` y `cantidad_max`: limites de inventario.
- `precio`: decimal con hasta 10 digitos y 2 decimales.
- `stock`: cantidad disponible; inicia en cero.
- `fecha_registro`: Django la establece automaticamente al crear el producto.

El modelo es la fuente de verdad para las migraciones, el formulario y el serializer de la API. No se agregaron campos que no existieran en el modelo actual.

## 4. Formulario: `inventario/forms.py`x|x

`ProductoForm` hereda de `forms.ModelForm`. Django genera los campos y las validaciones basandose en `Producto`.

La tupla `fields` define que campos aparecen en el formulario. `fecha_registro` no aparece porque debe asignarlo Django, no el usuario.

Los `widgets` cambian la forma HTML de algunos campos:

- `Textarea` da mas espacio para la descripcion.
- `NumberInput` permite valores numericos y define limites del navegador.
- `step = 0.01` permite introducir precios con centavos.

## 5. Vistas: `inventario/views.py`

Todas las vistas del panel llevan `@login_required`. Esto protege cada URL aunque alguien intente escribirla directamente.

### `dashboard(request)`

- `count()` cuenta todos los productos.
- `filter(stock__lte=5)` cuenta productos con stock menor o igual a cinco.
- `order_by('-fecha_registro')[:5]` obtiene los cinco mas recientes.
- El diccionario `contexto` entrega esos datos al template.

### `lista_productos(request)`

Obtiene `Producto.objects.all()` y lo envia como `productos` a la tabla.

### `crear_producto(request)`

- En GET, `request.POST` esta vacio y se muestra un formulario nuevo.
- En POST, `ProductoForm` recibe los datos enviados.
- `is_valid()` comprueba campos obligatorios y tipos.
- `save()` crea el registro en PostgreSQL usando el ORM.
- `redirect()` lleva a la lista y evita duplicar el envio al recargar.

### `editar_producto(request, producto_id)`

- Busca el producto por su ID con `get_object_or_404`.
- Crea `ProductoForm` usando `instance=producto`, por lo que el formulario aparece rellenado.
- Cuando el formulario es valido, `form.save()` actualiza la misma fila existente.
- No crea una migracion porque editar valores no cambia la estructura de la tabla.

### `eliminar_producto(request, producto_id)`

- Solo acepta solicitudes POST para evitar eliminar por accidente al abrir un enlace.
- Busca el producto por su ID.
- `producto.delete()` elimina esa fila de la base de datos.
- La tabla incluye CSRF y una confirmacion en el navegador antes de enviar el borrado.

## 6. Templates

### `base.html`

Es el layout compartido. Contiene:

- `{% load static %}` para cargar CSS, JavaScript e imagenes.
- Sidebar con Dashboard, Productos y Registrar producto.
- Navbar con `{{ request.user.username }}`.
- Formulario POST de logout con `{% csrf_token %}`.
- `{% block contenido %}` para que cada pagina inserte su contenido.

### `dashboard.html`

Extiende `inventario/base.html` y muestra `total_productos`, `stock_bajo` y `productos_recientes`. El bloque `{% for producto in productos_recientes %}` crea una fila por producto.

### `lista_productos.html`

Extiende el layout y recorre `productos` para mostrar nombre, marca, precio, stock y fecha.

### `crear_producto.html`

Extiende el layout, recorre los campos de `form` y muestra errores de validacion. El token CSRF protege el POST.

### `registration/login.html`

No extiende `base.html` porque el usuario aun no ha iniciado sesion. Incluye sus propios archivos estaticos y usa los nombres de campo que espera `AuthenticationForm`: `username` y `password`.

## 7. URLs

### URLs del proyecto

`inventario_project/urls.py` conecta tres grupos:

- `/api/` conserva la API REST existente.
- `/` incluye las URLs HTML de `inventario`.
- `/accounts/` incluye las vistas de autenticacion de Django.

### URLs de la app

- `/` -> `dashboard`
- `/productos/` -> `lista_productos`
- `/productos/nuevo/` -> `crear_producto`
- `/productos/<id>/editar/` -> `editar_producto`
- `/productos/<id>/eliminar/` -> `eliminar_producto`

Los nombres (`dashboard`, `lista_productos`, `crear_producto` y `logout`) permiten usar `{% url %}` sin escribir rutas fijas en los templates.

## 8. API existente

La API no fue eliminada ni reemplazada.

- `api/serializer.py` transforma `Producto` a JSON y JSON a datos de Django.
- `api/views.py` usa `ModelViewSet`, que ofrece listar, consultar, crear, actualizar y eliminar.
- `api/urls.py` registra el recurso `productos` en un `DefaultRouter`.

La API queda disponible bajo `/api/productos/`.

## 9. Assets y Spark Admin

Los recursos quedaron en:

```text
inventario/static/inventario/assets/
```

Los templates los referencian con el namespace de la app, por ejemplo:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'inventario/assets/css/main.css' %}">
```

El namespace evita conflictos si otra app tiene archivos con el mismo nombre.

## 10. Cambios realizados paso a paso

1. Se revisaron modelos, vistas, URLs, settings, API, templates y assets existentes.
2. Se detecto que la carpeta `template/` no seguia la estructura estandar de Django.
3. Se movieron los templates a `inventario/templates/`.
4. Se movieron los assets a `inventario/static/inventario/assets/`.
5. Se elimino un `login.html` duplicado y se conservo una sola copia en `templates/registration/`.
6. Se corrigio `Producto` para declarar `fecha_registro`, que ya existia en la migracion y era usada por el dashboard.
7. Se creo `ProductoForm` para validar todos los campos obligatorios del modelo.
8. Se corrigio `crear_producto` para usar el formulario en lugar de guardar solo tres campos.
9. Se crearon las paginas de lista y registro de productos.
10. Se conservaron la API, la conexion PostgreSQL y las rutas de autenticacion.
11. Se eliminaron ajustes `LOGIN_*` duplicados de `urls.py`; deben vivir en `settings.py`.
12. Se agregaron docstrings y comentarios breves en los modulos Python para facilitar el estudio.

## 11. Comandos utiles

Ejecutar desde la carpeta que contiene `manage.py`:

```powershell
py manage.py check
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Para crear un usuario administrador del panel, usa `createsuperuser`. El panel personalizado usa la autenticacion de Django; `/admin/` se conserva, pero no es necesario para el uso normal.

## 12. Que estudiar despues

1. Modelos y migraciones.
2. ORM: `count`, `filter`, `order_by`, `all`.
3. Formularios `ModelForm` y validacion.
4. Decorador `login_required` y sesiones.
5. Contexto de templates y herencia con `extends`.
6. URLs con `include`, `path` y nombres.
7. Serializers y ViewSets de Django REST Framework.
