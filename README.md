# Proyecto-Inicial-Practicas
markdown# API CRUD de Gestión de Clientes

Sistema completo de gestión de clientes con autenticación JWT, desarrollado con FastAPI, SQLAlchemy y MySQL.

##Características

- *Autenticación JWT* - Sistema de login seguro con tokens
- *CRUD Completo* - Crear, Leer, Actualizar y Eliminar clientes
- *Base de datos MySQL* - Persistencia de datos confiable
- *Validación de datos* - Con Pydantic
- *Documentación automática* - Swagger UI integrado
- *CORS habilitado* - Listo para conectar con frontend
- *Validación de duplicados* - Previene teléfonos repetidos
- *Seguridad* - Contraseñas encriptadas con bcrypt

## Tecnologías

- *Backend:* FastAPI (Python 3.8+)
- *Base de datos:* MySQL 8.0+
- *ORM:* SQLAlchemy
- *Autenticación:* JWT (JSON Web Tokens)
- *Validación:* Pydantic
- *Encriptación:* bcrypt

## Instalación

### 1. Clonar el repositorio
bash
git clone https://gitlab.com/tu-usuario/crud-clientes-backend.git
cd crud-clientes-backend


### 2. Crear entorno virtual (recomendado)

*Windows:*
bash
python -m venv venv
venv\Scripts\activate


*Linux/Mac:*
bash
python3 -m venv venv
source venv/bin/activate


### 3. Instalar dependencias
bash
pip install -r requirements.txt


### 4. Configurar base de datos

*Crear base de datos en MySQL:*
sql
CREATE DATABASE empresa_clientes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


*Crear archivo .env* (copiar desde .env.example):
bash
cp .env.example .env


*Editar .env* con tus credenciales:
env
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=empresa_clientes
SECRET_KEY=cambia_esta_clave_por_una_segura_en_produccion


### 5. Ejecutar la API
bash
python -m uvicorn main:app --reload


La API estará disponible en: *http://127.0.0.1:8000*

## Documentación

Una vez ejecutada la API, accede a:

- *Swagger UI (interactivo):* http://127.0.0.1:8000/docs
- *ReDoc:* http://127.0.0.1:8000/redoc

## Uso de la API

### 1. Registrar un usuario

*Endpoint:* POST /register
json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123"
}


### 2. Iniciar sesión

*Endpoint:* POST /login

username: admin
password: admin123


*Respuesta:*
json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}


### 3. Usar el token

En todas las peticiones protegidas, incluir el header:

Authorization: Bearer {access_token}


### 4. Crear un cliente

*Endpoint:* POST /clientes/
json
{
  "nombre": "Juan",
  "apellidos": "Pérez García",
  "edad": 30,
  "fecha_nacimiento": "1994-05-15",
  "telefono": "666777888",
  "direccion": "Calle Mayor 123, Madrid"
}


## 📡 Endpoints disponibles

### Autenticación

| Método | Endpoint | Descripción | Autenticación |
| POST | /register | Registrar nuevo usuario |  No |
| POST | /login | Iniciar sesión |  No |
| GET | /users/me | Usuario actual |  Sí |

### Clientes (CRUD)

| Método | Endpoint | Descripción | Autenticación |
| POST | /clientes/ | Crear cliente |  Sí |
| GET | /clientes/ | Listar clientes |  Sí |
| GET | /clientes/{id} | Ver cliente |  Sí |
| PUT | /clientes/{id} | Actualizar cliente |  Sí |
| DELETE | /clientes/{id} | Eliminar cliente |  Sí |

## Estructura del proyecto

CRUDClientes/
├── bbdd.py              # Configuración de base de datos
├── modelo.py            # Modelos SQLAlchemy (tablas)
├── esquemas.py          # Schemas Pydantic (validación)
├── autor.py             # Autenticación y JWT
├── crud.py              # Operaciones CRUD
├── main.py              # Aplicación FastAPI (rutas)
├── requirements.txt     # Dependencias
├── .env.example         # Plantilla de configuración
├── .gitignore          # Archivos ignorados por Git
└── README.md           # Este archivo


## Seguridad

- Las contraseñas se almacenan encriptadas con *bcrypt*
- Autenticación mediante *tokens JWT*
- Validación de datos con *Pydantic*
- Protección contra duplicados (teléfonos)
- CORS configurado para frontend

## Conectar con Frontend

El backend está listo para conectarse con cualquier frontend (React, Vue, Angular, etc.)

*URL base:* http://localhost:8000

*Ejemplo en JavaScript:*
javascript
// Login
const response = await fetch('http://localhost:8000/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ username: 'admin', password: 'admin123' })
});
const { access_token } = await response.json();

// Listar clientes
const clientes = await fetch('http://localhost:8000/clientes/', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});


## Autores

- *Mario CV* - Backend Developer - [GitHub/GitLab]

## Licencia

Este proyecto es privado y de uso educativo.

## Despliegue

Para desplegar en producción:

1. Cambiar SECRET_KEY a una clave segura
2. Configurar allow_origins en CORS con la URL del frontend
3. Usar una base de datos MySQL en la nube
4. Desplegar en Railway, Render o similar
