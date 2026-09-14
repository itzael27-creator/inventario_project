"""Configuracion global del proyecto inventario_project."""

from pathlib import Path  # Permite construir rutas compatibles con Windows y Linux.

# Construye las rutas internas del proyecto a partir de BASE_DIR.
# BASE_DIR apunta a la carpeta que contiene manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuracion basica de desarrollo; debe revisarse antes de publicar.
# Clave usada por Django para firmar sesiones y otros datos internos.
SECRET_KEY = 'django-insecure-og(lf^h6m7mds$k2f8$h*_&ws_=9fkd1u%vzse$#3sithp5xt0'

# True muestra errores detallados durante el desarrollo local.
DEBUG = True

# Lista de dominios permitidos; vacia funciona con el servidor local de desarrollo.
ALLOWED_HOSTS = []


# Aplicaciones instaladas y disponibles para el proyecto.

# Middleware procesa cada peticion antes y despues de las vistas.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo que contiene las URLs principales del proyecto.
ROOT_URLCONF = 'inventario_project.urls'

# Configuracion para localizar y renderizar templates HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # No se necesita una carpeta global de templates.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Punto de entrada para servidores WSGI de produccion.
WSGI_APPLICATION = 'inventario_project.wsgi.application'


# Configuracion de la base de datos.
# Conexion existente a PostgreSQL. No se cambia para conservar la base actual.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'bd_inventario',
        'USER': 'postgres',
        'PASSWORD': 'Buchin06',
        'HOST': 'localhost',
        'PORT': '5432',
        
    }
}

# Apps de Django, Django REST Framework y la app principal del inventario.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages', 
    'django.contrib.staticfiles',  # Sirve CSS, JavaScript e imagenes.
    'rest_framework',  # Habilita la API REST existente.
    'inventario.apps.InventarioConfig',  # Registra la app inventario.
]


# Validadores que comprueban la seguridad de las contrasenas.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Idioma y zona horaria que usa el proyecto.
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Configuracion para CSS, JavaScript e imagenes estaticas.
# Prefijo URL que Django usa para servir archivos estaticos.
STATIC_URL = 'static/'


# Configuracion de correo para desarrollo.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# Este es para iniciar sesión
LOGIN_URL = '/accounts/login/'
# URL posterior a un login exitoso.
LOGIN_REDIRECT_URL = '/'
# Este nos sirve para mandar al usuario al incio de sesion cuando se cierra la sesión 
LOGOUT_REDIRECT_URL = '/accounts/login/'