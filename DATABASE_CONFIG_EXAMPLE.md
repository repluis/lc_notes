# Configuración de Base de Datos

Este proyecto utiliza una arquitectura orientada al dominio (DDD) que permite cambiar fácilmente entre diferentes bases de datos.

## Cambiar de Base de Datos

Para cambiar la base de datos, solo necesitas modificar el archivo `lc_proyect/settings.py`:

### 1. SQLite (Por defecto)

```python
DB_ENGINE = 'sqlite3'
```

No requiere configuración adicional.

### 2. MySQL

```python
DB_ENGINE = 'mysql'
```

Y configurar las variables de entorno o modificar los valores por defecto:

```bash
export DB_NAME=lc_notes
export DB_USER=root
export DB_PASSWORD=tu_password
export DB_HOST=localhost
export DB_PORT=3306
```

O modificar directamente en `settings.py` los valores por defecto.

**Instalar driver de MySQL:**
```bash
pip install mysqlclient
# o
pip install pymysql
```

### 3. PostgreSQL

```python
DB_ENGINE = 'postgresql'
```

Y configurar las variables de entorno:

```bash
export DB_NAME=lc_notes
export DB_USER=postgres
export DB_PASSWORD=tu_password
export DB_HOST=localhost
export DB_PORT=5432
```

**Instalar driver de PostgreSQL:**
```bash
pip install psycopg2-binary
```

## Arquitectura DDD

El proyecto está estructurado con:

- **Dominio** (`notes_home/domain/`): Entidades de negocio
- **Repositorios** (`notes_home/repositories/`): Abstracción de acceso a datos
- **Servicios** (`notes_home/services/`): Lógica de negocio

Esta estructura permite cambiar de base de datos sin modificar la lógica de negocio, solo cambiando la configuración en `settings.py`.

## Migraciones

Después de cambiar la base de datos, ejecuta las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

