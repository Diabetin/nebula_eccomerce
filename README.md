# Nebula Eccomerce

Proyecto de evaluación final del Módulo 8 de la certificación para Desarrollador Full Stack Python.  
Ecommerce básico desarrollado con Django, PostgreSQL y Bootstrap.

## Enlace al repositorio

Repositorio público en GitHub:  
https://github.com/Diabetin/nebula_eccomerce

## Requisitos

- Python 3.12
- Git
- PostgreSQL (ej. versión 14+)
- Pip

### Dependencias principales

El proyecto usa, entre otras:

- Django 6.x
- psycopg2 (conector PostgreSQL)
- Bootstrap (desde estáticos/plantillas)

Todas las dependencias están definidas en `requirements.txt`.

## Instalación y entorno virtual

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Diabetin/nebula_eccomerce.git
   cd nebula_eccomerce/Eccomerce_Nebula_shop
   ```

2. Crear y activar entorno virtual:

   ```bash
   python -m venv venv
   # En Windows (PowerShell):
   venv\Scripts\Activate.ps1
   # En Windows (cmd):
   venv\Scripts\activate.bat
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar base de datos PostgreSQL:

   Crear una base de datos `nebula_shop` y un usuario con permisos.  
   Asegúrate de que los datos coinciden con la configuración en `Eccomerce_Nebula_shop/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'nebula_shop',
           'USER': 'postgres',
           'PASSWORD': 'tu_password',
           'HOST': '127.0.0.1',
           'PORT': '5433',
       }
   }
   ```

## Cómo ejecutar en local

1. Aplicar migraciones:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Levantar el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

3. Acceder en el navegador:

   - Sitio principal: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

## Rutas principales

### Públicas

- `/` – Página principal / listado de productos
- `/product/<int:product_id>/` – Detalle de producto

### Cliente (usuarios registrados)

- `/carrito/` – Ver carrito  
- `/product/<int:product_id>/add/` – Agregar producto al carrito  
- `/product/<int:product_id>/remove/` – Quitar producto del carrito  
- `/realizar_pago/` – Simular pago  
- `/crear_orden/` – Crear orden de compra  
- `/ordenes/` – Ver órdenes del cliente  
- `/ordenes/<int:order_id>/` – Detalle de una orden  
- `/login_customer/` – Inicio de sesión cliente  
- `/register_customer/` – Registro de cliente  
- `/logout_costumer/` – Cerrar sesión cliente  

### Admin / staff

- `/login/` – Login de administrador/staff (vista propia)  
- `/register_admin/` – Registro de usuario administrador  
- `/logout/` – Logout admin/staff  
- `/products/crud/` – CRUD de productos  
- `/products/` – Listado de productos
- `/categories/` – CRUD de categorías  
- `/admin/` – Panel de administración estándar de Django  

## Creación de usuarios administradores

No es necesario tener usuarios administradores predefinidos.  
Pueden crearse directamente desde la ruta:

- `/register_admin/`

Para crear nuevos usuarios administradores se requiere una **master key**:

- Master key: `modulo7`

Esta clave se solicita en el formulario de registro de administrador y actúa como mecanismo de seguridad para evitar que cualquier usuario pueda elevar privilegios sin autorización.

## Credenciales de prueba sugeridas

Puedes crear los usuarios de prueba directamente desde la aplicación usando las rutas de registro, por lo que no es obligatorio que existan usuarios pre-cargados en la base de datos.

Ejemplo de usuarios que el evaluador puede crear:

### ADMIN (creado en `/register_admin/` usando la master key)

- Usuario: `admin`
- Email: `admin@example.com`
- Password: `Admin123!`

Panel de administración:  
http://127.0.0.1:8000/admin/

### CLIENTE (creado en `/register_customer/`)

- Usuario: `cliente`
- Email: `cliente@example.com`
- Password: `Cliente123!`

Login de cliente:  
http://127.0.0.1:8000/login_customer/