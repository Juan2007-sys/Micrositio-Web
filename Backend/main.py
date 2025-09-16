from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from openai import OpenAI
from fastapi import Form
import sqlite3
from proyecto import Proyecto
from contacto import Contacto
from ubicacion import Ubicacion
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "Hi Class!"}

app = FastAPI()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Reemplaza con tu clave de API real
)

#Add Function
@app.get("/create-db/")
def create_db():
    #funcion para crear la base de datos en sqlite con campos id, nombre, precio
    conn = sqlite3.connect('miwebsite.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            url TEXT,
            imagen TEXT,
            video TEXT              
        )
    ''')
    conn.commit()
    conn.close()
    return {"message": "Database created successfully"}, status.HTTP_201_CREATED


@app.post("/proyectos/")
def crear_proyecto(proyecto: Proyecto):
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO proyectos (nombre, descripcion, url, imagen, video)
        VALUES (?, ?, ?, ?, ?)
    """, (proyecto.nombre, proyecto.descripcion, str(proyecto.url) if proyecto.url else None,
          str(proyecto.imagen) if proyecto.imagen else None,
          str(proyecto.video) if proyecto.video else None))
    conn.commit()
    conn.close()
    return {"message": "Proyecto agregado", "data": proyecto.dict()}



@app.get("/proyectos/")
def obtener_proyectos():
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proyectos")
    rows = cursor.fetchall()
    conn.close()

    proyectos = []
    for r in rows:
        proyectos.append({
            "id": r[0],
            "nombre": r[1],
            "descripcion": r[2],
            "url": r[3],
            "imagen": r[4],
            "video": r[5]
        })

    return {"data": proyectos}


# Endpoint para obtener un solo proyecto por su id
@app.get("/proyectos/{proyecto_id}")
def obtener_proyecto(proyecto_id: int):
    # Conectar a la base de datos
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    # Buscar el proyecto por id
    cursor.execute("SELECT * FROM proyectos WHERE id = ?", (proyecto_id,))
    r = cursor.fetchone()
    conn.close()
    # Si existe, devolver los datos como diccionario
    if r:
        proyecto = {
            "id": r[0],
            "nombre": r[1],
            "descripcion": r[2],
            "url": r[3],
            "imagen": r[4],
            "video": r[5]
        }
        return proyecto
    else:
        # Si no existe, lanzar error 404
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    

@app.put("/proyectos/{proyecto_id}")
def actualizar_proyecto(proyecto_id: int, proyecto: Proyecto):
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proyectos WHERE id = ?", (proyecto_id,))
    existente = cursor.fetchone()
    if not existente:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    cursor.execute("""
        UPDATE proyectos
        SET nombre = ?, descripcion = ?, url = ?, imagen = ?, video = ?
        WHERE id = ?
    """, (
        proyecto.nombre,
        proyecto.descripcion,
        str(proyecto.url) if proyecto.url else None,
        str(proyecto.imagen) if proyecto.imagen else None,
        str(proyecto.video) if proyecto.video else None,
        proyecto_id
    ))
    conn.commit()
    conn.close()
    return {"message": f"Proyecto {proyecto_id} actualizado correctamente"}


#------------------------------ Contacto -------------------------------------------------------------- #

@app.get("/create-contacto-db/")
def create_contacto_db():
    conn = sqlite3.connect('miwebsite.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return {"message": "Tabla de contacto creada exitosamente"}, status.HTTP_201_CREATED



@app.post("/contacto/")
def recibir_contacto(contacto: Contacto):
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()

    #crear tabla contacto si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            telefono TEXT
        )
    ''')

    #insertar datos en la tabla contacto
    cursor.execute("""
        INSERT INTO contacto (nombre, email, mensaje, telefono)
        VALUES (?, ?, ?, ?)
    """, (contacto.nombre, contacto.email, contacto.mensaje, contacto.telefono))

    conn.commit()
    conn.close()

    return {"message": "Contacto recibido", "data": contacto.dict()}

@app.delete("/contacto/{contacto_id}")
def eliminar_contacto(contacto_id: int):
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacto WHERE id = ?", (contacto_id,))
    existente = cursor.fetchone()
    if not existente:
        conn.close()
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    cursor.execute("DELETE FROM contacto WHERE id = ?", (contacto_id,))
    conn.commit()
    conn.close()
    return {"message": f"Contacto {contacto_id} eliminado correctamente"}
 
 #------------------------------------------------   AI  -------------------------------------------------------------- #


# Nuevo endpoint de chat simple
@app.post("/significado-nombre/")
async def obtener_significado(nombre: str = Form(...)):
    try:
        respuesta = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "", # Optional. Site title for rankings on openrouter.ai.
            },
            model="gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "Eres un experto en etimología de nombres."},
                {"role": "user", "content": f"¿Cuál es el significado del nombre {nombre}?"}
            ]
        )

        significado = respuesta.choices[0].message.content.strip()
        return JSONResponse(content={
            "nombre": nombre,
            "significado": significado
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# Endpoint para análisis de sentimiento
@app.post("/analizar-sentimiento/")
async def analizar_sentimiento(mensaje: str = Form(...)):
    try:
        respuesta = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "",
                "X-Title": "",
            },
            model="gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de sentimientos. Analiza el siguiente mensaje y responde únicamente con una de estas etiquetas: positivo, negativo o neutro."},
                {"role": "user", "content": f"Analiza el sentimiento del siguiente mensaje: '{mensaje}'"}
            ]
        )
        sentimiento = respuesta.choices[0].message.content.strip().lower()
        if sentimiento not in ["positivo", "negativo", "neutro"]:
            sentimiento = "neutro"
        return JSONResponse(content={
            "mensaje": mensaje,
            "sentimiento": sentimiento
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint para chat general
@app.post("/chat-simple/")
async def chat_simple(mensaje: str = Form(...)):
    try:
        respuesta = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "",
                "X-Title": "",
            },
            model="gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "Eres un asistente útil y amigable."},
                {"role": "user", "content": mensaje}
            ]
        )
        respuesta_ia = respuesta.choices[0].message.content.strip()
        return JSONResponse(content={
            "mensaje": mensaje,
            "respuesta": respuesta_ia
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

    #------------------------------------------------------------------------------   MAPA  -------------------------------------------------------------- #

# Crear tabla ubicaciones en SQLite
@app.get("/create-ubicacion-db/")
def create_ubicacion_db():
    conn = sqlite3.connect('miwebsite.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL,
            direccion TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return {"message": "Tabla de ubicaciones creada exitosamente"}, status.HTTP_201_CREATED

# Endpoint para agregar una ubicación
@app.post("/ubicaciones/")
def agregar_ubicacion(ubicacion: Ubicacion):
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ubicaciones (nombre, descripcion, latitud, longitud, direccion)
        VALUES (?, ?, ?, ?, ?)
    """, (
        ubicacion.nombre,
        ubicacion.descripcion,
        ubicacion.latitud,
        ubicacion.longitud,
        ubicacion.direccion
    ))
    conn.commit()
    conn.close()
    return {"message": "Ubicación agregada", "data": ubicacion.dict()}

# Endpoint para obtener todas las ubicaciones
@app.get("/ubicaciones/")
def obtener_ubicaciones():
    conn = sqlite3.connect("miwebsite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ubicaciones")
    rows = cursor.fetchall()
    conn.close()
    ubicaciones = []
    for r in rows:
        ubicaciones.append({
            "id": r[0],
            "nombre": r[1],
            "descripcion": r[2],
            "latitud": r[3],
            "longitud": r[4],
            "direccion": r[5]
        })
    return {"data": ubicaciones}

# 🔥 Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (en producción puedes restringir)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos: GET, POST, PUT, DELETE
    allow_headers=["*"],  # Permitir todas las cabeceras
)