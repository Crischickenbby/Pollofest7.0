# 🚀 Guía Completa: Despliegue de Flask + PostgreSQL en Railway

## 📋 Índice
1. [Preparación del Proyecto Local](#preparación-del-proyecto-local)
2. [Configuración de Archivos de Despliegue](#configuración-de-archivos-de-despliegue)
3. [Configuración de Railway](#configuración-de-railway)
4. [Migración de Base de Datos](#migración-de-base-de-datos)
5. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
6. [Lista de Verificación Final](#lista-de-verificación-final)

---

## 📁 Preparación del Proyecto Local

### 1. Estructura de Archivos Requerida
```
mi-proyecto/
├── app.py                  # Archivo principal de Flask
├── config.py              # Configuración de base de datos
├── requirements.txt       # Dependencias de Python
├── Procfile              # Configuración para Railway
├── Dockerfile            # Configuración de Docker (opcional pero recomendado)
├── nixpacks.toml         # Configuración de dependencias del sistema
├── start.sh              # Script de inicio personalizado
├── .env                  # Variables locales (NO subir a Git)
├── .gitignore           # Archivos a ignorar en Git
└── app/
    ├── templates/        # Plantillas HTML
    └── static/          # CSS, JS, imágenes
```

### 2. Archivo `requirements.txt`
```txt
Flask==3.1.2
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
```

### 3. Archivo `config.py`
```python
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Producción: usar DATABASE_URL completa
    DATABASE_CONFIG = DATABASE_URL
else:
    # Desarrollo: usar variables individuales
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'mi_base_datos')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE_CONFIG = {
        'host': DB_HOST,
        'database': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD
    }

# Función para obtener una conexión a la base de datos
def get_db_connection():
    if isinstance(DATABASE_CONFIG, str):
        # Producción: usar DATABASE_URL
        return psycopg2.connect(DATABASE_CONFIG)
    else:
        # Desarrollo: usar diccionario de configuración
        return psycopg2.connect(**DATABASE_CONFIG)
```

### 4. Configuración en `app.py`
```python
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configurar clave secreta desde variables de entorno
app.secret_key = os.getenv('SECRET_KEY', 'clave-por-defecto-cambiar-en-produccion')

# Configuración para producción
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
```

### 5. Archivo `.env` (LOCAL - NO subir a Git)
```env
# Configuración local
DB_HOST=localhost
DB_NAME=mi_base_datos
DB_USER=postgres
DB_PASSWORD=mi_password
SECRET_KEY=generar_clave_secreta_aqui
```

### 6. Archivo `.gitignore`
```gitignore
# Variables de entorno
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Base de datos
*.db
*.sqlite3

# Logs
*.log

# IDEs
.vscode/
.idea/
*.swp
*.swo
```

---

## ⚙️ Configuración de Archivos de Despliegue

### 1. Archivo `Procfile`
```
web: bash start.sh
```

### 2. Archivo `start.sh`
```bash
#!/bin/bash
pip uninstall -y psycopg2 psycopg2-binary
pip install psycopg2-binary==2.9.9 --force-reinstall --no-cache-dir
exec gunicorn --bind 0.0.0.0:$PORT app:app
```

### 3. Archivo `nixpacks.toml`
```toml
[phases.setup]
aptPkgs = ["libpq-dev", "gcc", "python3-dev"]

[phases.install]
cmds = ["pip install --upgrade pip"]
```

### 4. Archivo `Dockerfile` (Opcional pero recomendado)
```dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## 🚂 Configuración de Railway

### 1. Crear Cuenta y Proyecto
1. Ve a [railway.app](https://railway.app)
2. Crea cuenta con GitHub
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Conecta tu repositorio

### 2. Agregar PostgreSQL
1. En tu proyecto Railway, haz clic en "+"
2. Selecciona "Database"
3. Elige "PostgreSQL"
4. Railway creará automáticamente la base de datos

### 3. Configurar Variables de Entorno
En la pestaña "Variables" del servicio web, agrega:

```
DATABASE_URL = ${{Postgres.DATABASE_PUBLIC_URL}}
SECRET_KEY = tu-clave-secreta-aqui
FLASK_ENV = production
```

### 4. Obtener URLs de Conexión
En la pestaña "Variables" de PostgreSQL encontrarás:
- `DATABASE_URL`: URL interna (para la aplicación)
- `DATABASE_PUBLIC_URL`: URL externa (para herramientas como pgAdmin)

---

## 💾 Migración de Base de Datos

### 1. Crear Backup de Base de Datos Local
```bash
# Usando pg_dump (desde terminal)
pg_dump -h localhost -U postgres -d mi_base_datos > backup.sql

# O usar pgAdmin:
# 1. Clic derecho en base de datos → Backup...
# 2. Format: Plain
# 3. Encoding: UTF8
# 4. Data Options: Pre-data ✓, Data ✓, Post-data ✓
```

### 2. Configurar pgAdmin para Railway
1. Abrir pgAdmin
2. Add New Server:
   - **Name**: Railway PostgreSQL
   - **Host**: tramway.proxy.rlwy.net (del PUBLIC_URL)
   - **Port**: 33215 (del PUBLIC_URL)
   - **Database**: railway
   - **Username**: postgres
   - **Password**: (del PUBLIC_URL)

### 3. Restaurar en Railway
1. Clic derecho en base de datos "railway" → Restore...
2. Seleccionar archivo de backup
3. Data Options: Clean before restore ✓
4. Restore

### Script de Prueba de Conexión
Crear `test_db.py`:
```python
import psycopg2
import os

# URL de conexión de Railway (cambiar por la tuya)
DATABASE_URL = "postgresql://postgres:PASSWORD@HOST:PORT/railway"

try:
    print("Intentando conectar a Railway PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("✅ Conexión exitosa!")
    
    # Verificar qué tablas existen
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tablas = cur.fetchall()
    
    print(f"\n📊 Tablas encontradas ({len(tablas)}):")
    for tabla in tablas:
        print(f"  - {tabla[0]}")
        
        # Contar registros en cada tabla
        try:
            cur.execute(f'SELECT COUNT(*) FROM "{tabla[0]}"')
            count = cur.fetchone()[0]
            print(f"    📋 Registros: {count}")
        except Exception as e:
            print(f"    ⚠️  Error consultando: {e}")
    
    cur.close()
    conn.close()
    print("\n✅ Test completado exitosamente!")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

---

## 🔧 Solución de Problemas Comunes

### Error: `ImportError: libpq.so.5`
**Solución**: Usar `psycopg2-binary` y el script `start.sh`
```bash
pip uninstall -y psycopg2 psycopg2-binary
pip install psycopg2-binary==2.9.9 --force-reinstall --no-cache-dir
```

### Error: Base de datos no conecta
**Verificar**:
1. Variable `DATABASE_URL` correcta
2. Usar `DATABASE_PUBLIC_URL` para conexiones externas
3. Verificar que la base de datos se llame "railway"

### Error: Application failed to respond
**Verificar**:
1. Variables de entorno configuradas
2. Puerto correcto (`PORT` variable de Railway)
3. Logs en Railway para ver error específico

### Error: Tablas no existen
**Solución**:
1. Verificar que el restore de pgAdmin fue exitoso
2. Comprobar que las tablas estén en el esquema "public"
3. Ejecutar script de prueba `test_db.py`

---

## ✅ Lista de Verificación Final

### Antes de Desplegar:
- [ ] Archivo `requirements.txt` completo
- [ ] `config.py` configurado para producción
- [ ] Variables de entorno en `.env` local
- [ ] `.gitignore` incluye `.env`
- [ ] `Procfile`, `start.sh`, `nixpacks.toml` creados
- [ ] Repositorio en GitHub actualizado

### En Railway:
- [ ] Proyecto creado y conectado a GitHub
- [ ] PostgreSQL agregado al proyecto
- [ ] Variables de entorno configuradas:
  - [ ] `DATABASE_URL = ${{Postgres.DATABASE_PUBLIC_URL}}`
  - [ ] `SECRET_KEY = clave-secreta-aqui`
  - [ ] `FLASK_ENV = production`

### Migración de Base de Datos:
- [ ] Backup de base de datos local creado
- [ ] pgAdmin conectado a Railway PostgreSQL
- [ ] Datos restaurados en base de datos "railway"
- [ ] Script de prueba ejecutado exitosamente

### Verificación Final:
- [ ] Aplicación carga correctamente
- [ ] Login funciona
- [ ] Base de datos responde
- [ ] Todas las funcionalidades operativas

---

## 🎯 Comandos Útiles

### Git
```bash
git add .
git commit -m "Configurar despliegue en Railway"
git push origin main
```

### Railway CLI (Opcional)
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Ver logs
railway logs

# Ver variables
railway variables
```

### Generar SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📝 Notas Importantes

1. **Nunca subas archivos `.env` a Git**
2. **Usa `DATABASE_PUBLIC_URL` para conexiones externas**
3. **El script `start.sh` resuelve problemas de psycopg2**
4. **Railway redespliega automáticamente con cada push**
5. **Siempre prueba localmente antes de desplegar**

---

## 🆘 Contacto de Emergencia

Si algo falla durante el despliegue:
1. Revisar logs en Railway
2. Ejecutar `test_db.py` para verificar conexión
3. Verificar variables de entorno
4. Comprobar que todas las dependencias estén en `requirements.txt`

---

**¡Éxito en tus futuros despliegues! 🚀**