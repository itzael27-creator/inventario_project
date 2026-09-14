
# Este archivo permite ejecutar comandos Django desde la terminal.
import os  # Permite definir variables de entorno del proyecto.
import sys  # Permite leer los argumentos escritos en la terminal.


def main():
    # Indica a Django que debe usar la configuracion de este proyecto.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_project.settings')
    try:
        # Importa el ejecutor de comandos solo cuando se necesita ejecutar manage.py.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Muestra un mensaje claro si Django no esta instalado en el entorno activo.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando recibido, por ejemplo check, migrate o runserver.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Ejecuta main solo cuando este archivo se llama directamente.
    main()
