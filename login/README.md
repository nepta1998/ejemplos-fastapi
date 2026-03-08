# FastAPI Login Demo (fake_db)

Demo web en FastAPI:

- registro de usuario (correo + contraseña)
- inicio de sesión con `fastapi-login`
- ruta privada `/home` protegida por sesión
- persistencia fake en memoria (solo durante la ejecución)

## Requisitos

- Python 3.11+
- Poetry

## Instalación (Poetry)

```bash
poetry install
```

## Ejecutar (comando recomendado)

```bash
poetry run fastapi dev app/main.py
```

Abrir en navegador:

- <http://127.0.0.1:8000/login>

## Configuración

Variables opcionales:

- `APP_SECRET=...` (secreto JWT)
- `ACCESS_TOKEN_EXPIRE_MINUTES=60`

## Nota de persistencia

Los usuarios se guardan **solo en memoria**. Si reinicias la app, se pierden.

## Flujo demo

1. Entrar a `/register` y crear usuario.
2. Ir a `/login` y autenticar.
3. Login exitoso redirige a `/home`.
4. Sin sesión activa, `/home` redirige a `/login`.
5. Desde `/home`, usar botón **Cerrar sesión**.

## Librería usada para login

- [fastapi-login](https://fastapi-login.readthedocs.io/)
