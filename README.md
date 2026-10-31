# FitSupply

<p align="center">
  <strong>Sports supplement inventory and relationship management</strong><br>
  <em>Aplicación web para la gestión de suplementos deportivos, productos, proveedores y clientes.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2.5-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/UI-Bootstrap%205-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Status-Development-orange" alt="Status">
</p>

## 🇪🇸 Español

### Descripción

**FitSupply** es una aplicación web desarrollada con Django para apoyar la administración de un negocio de suplementos deportivos. El sistema reúne funciones para gestionar el catálogo de productos, los proveedores y los clientes desde un panel privado.

Este repositorio corresponde a un proyecto en desarrollo y forma parte de un portafolio de aprendizaje en desarrollo web.

### Funcionalidades implementadas en el código

- **Autenticación:** registro de usuarios, inicio y cierre de sesión.
- **Productos:** registro, búsqueda por código, actualización y eliminación.
- **Proveedores:** registro y búsqueda de proveedores persona natural y empresa; edición y activación/desactivación.
- **Clientes:** registro, búsqueda por distintos datos, edición y activación/desactivación.
- **Panel de gestión:** accesos a los módulos de productos, proveedores y clientes.

> Nota: algunas pantallas y rutas del módulo de productos necesitan revisión para que coincidan con los nombres de campos y rutas definidos en el código. La documentación no implica que todos los flujos hayan sido probados de extremo a extremo.

### Tecnologías

- Python
- Django 5.2.5
- MySQL (motor configurado en `mysite/settings.py`)
- Bootstrap 5.3.8 (CSS cargado desde CDN)
- Django Templates

### Estructura del proyecto

```text
FitSupply/
├── manage.py
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── myapp/
    ├── migrations/
    ├── templates/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

### Requisitos

- Python compatible con Django 5.2.
- MySQL Server.
- Un controlador de Python para MySQL compatible con la instalación local.
- pip y un entorno virtual recomendado.

El repositorio todavía no incluye un archivo `requirements.txt`; por eso, la lista completa y reproducible de dependencias debe definirse antes de considerar cerrada la instalación.

### Configuración local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/salinascarlos-rgb/FitSupply.git
   cd FitSupply
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Instala Django y el controlador MySQL que se defina para el proyecto. La versión exacta del controlador debe documentarse junto con las dependencias.

   ```bash
   python -m pip install "Django==5.2.5"
   ```

4. Crea una base de datos MySQL llamada `fitsupply` y configura usuario, contraseña, host y puerto mediante variables de entorno una vez que `mysite/settings.py` haya sido adaptado para leerlas.

5. Aplica las migraciones y ejecuta el servidor:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Abre http://127.0.0.1:8000/ en el navegador.

> **Importante:** el paso de configuración de base de datos requiere primero externalizar las credenciales que actualmente están escritas en `mysite/settings.py`. No uses las credenciales publicadas en el repositorio.

### Seguridad

Antes de desplegar o utilizar el sistema con datos reales:

- Cambiar y revocar las credenciales que hayan sido publicadas en el repositorio.
- Leer `SECRET_KEY`, credenciales de base de datos y configuración sensible desde variables de entorno.
- Establecer `DEBUG = False` en producción.
- Configurar `ALLOWED_HOSTS), HTTPS y cookies seguras según el entorno.
- No subir bases de datos con información personal ni archivos locales.
- Revisar el historial de Git: borrar un secreto del último commit no lo elimina de commits anteriores.
- Probar permisos, validaciones y operaciones sensibles antes de usar datos reales.

### Estado del proyecto

En desarrollo. La instalación reproducible, la configuración segura por variables de entorno, las pruebas automatizadas y la revisión de algunas rutas y plantillas están pendientes de completar.

### Autor

**Carlos** — [salinascarlos-rgb](https://github.com/salinascarlos-rgb)

---

## 🇬🇧 English

### Overview

**FitSupply** is a Django web application intended to support the management of a sports-supplement business. It brings together product catalog, supplier and customer management features in a private dashboard.

This repository is a work in progress and is part of a software-development learning portfolio.

### Features present in the source code

- **Authentication:** user registration, sign-in and sign-out.
- **Products:** create, search by code, update and delete product records.
- **Suppliers:** register and search individual and company suppliers; edit, activate and deactivate records.
- **Customers:** register, search by several fields, edit, activate and deactivate records.
- **Dashboard:** navigation to the product, supplier and customer modules.

> Note: some product-page templates and routes need alignment with the model field names and URL patterns. The listed features have not all been verified through end-to-end testing.

### Tech stack

- Python
- Django 5.2.5
- MySQL (configured database backend)
- Bootstrap 5.3.8 (CSS loaded from a CDN)
- Django Templates

### Setup

See the Spanish **Configuración local** section above for the current setup outline. A complete dependency lock/requirements file and environment-based database configuration still need to be added before setup can be considered fully reproducible.

### Security

Do not deploy this project with the credentials currently present in the repository. Rotate exposed credentials, move secrets to environment variables, disable Django debug mode in production, configure allowed hosts and HTTPS, and keep personal data and local database files out of version control.

### Project status

In development. Reproducible dependency installation, secure environment configuration, automated tests and review of some product routes/templates remain outstanding.

---

*Learning by building — one feature at a time.*
