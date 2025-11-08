import psycopg2
import os

# URL de conexión de Railway
DATABASE_URL = "postgresql://postgres:hfZytYMLAFKDItjcTOsatfjdHSqcbgOk@tramway.proxy.rlwy.net:33215/railway"

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
    
    # Verificar algunos datos de ejemplo
    if tablas:
        try:
            cur.execute('SELECT COUNT(*) FROM "User"')
            users_count = cur.fetchone()[0]
            print(f"\n👥 Usuarios en tabla User: {users_count}")
            
            cur.execute('SELECT COUNT(*) FROM "People"')
            people_count = cur.fetchone()[0]
            print(f"👤 Personas en tabla People: {people_count}")
            
            cur.execute('SELECT COUNT(*) FROM "Status_People"')
            status_count = cur.fetchone()[0]
            print(f"📊 Estados en tabla Status_People: {status_count}")
            
        except Exception as e:
            print(f"⚠️  Error consultando datos: {e}")
    
    cur.close()
    conn.close()
    print("\n✅ Test completado exitosamente!")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")