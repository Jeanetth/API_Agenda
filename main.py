from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

# Conectar a la base de datos MongoDB
client = MongoClient("mongodb+srv://root:Elcieloesrojo98@agenda.wavhw.mongodb.net/?retryWrites=true&w=majority&appName=Agenda")  # Cambia la URL si tu base de datos está en otro servidor
db = client['agenda']  # Nombre de la base de datos
tareas_collection = db['datos']  # Nombre de la colección

# Modelo de Tarea usando Pydantic
class Tarea(BaseModel):
    titulo: str
    descripcion: str
    completada: bool = False

# Ruta para obtener todas las tareas (Read)
@app.get("/tareas", response_model=List[dict])
def obtener_tareas():
    tareas = list(tareas_collection.find())  # Obtener todas las tareas de la colección
    for tarea in tareas:
        tarea['_id'] = str(tarea['_id'])  # Convertir ObjectId a string para poder enviarlo en JSON
    return tareas

# Ruta para agregar una nueva tarea (Create)
@app.post("/tareas", response_model=dict)
def agregar_tarea(tarea: Tarea):
    resultado = tareas_collection.insert_one(tarea.dict())  # Insertar la nueva tarea en la colección
    return {"mensaje": "Tarea agregada correctamente", "id": str(resultado.inserted_id)}

# Ruta para actualizar una tarea (Update)
@app.put("/tareas/{id}", response_model=dict)
def actualizar_tarea(id: str, tarea_actualizada: Tarea):
    resultado = tareas_collection.update_one({'_id': ObjectId(id)}, {'$set': tarea_actualizada.dict()})
    if resultado.matched_count:
        return {"mensaje": "Tarea actualizada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Ruta para eliminar una tarea (Delete)
@app.delete("/tareas/{id}", response_model=dict)
def eliminar_tarea(id: str):
    resultado = tareas_collection.delete_one({'_id': ObjectId(id)})
    if resultado.deleted_count:
        return {"mensaje": "Tarea eliminada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Ruta principal (opcional)
@app.get("/")
def inicio():
    return {"mensaje": "API de Cosas por hacer con MongoDB y FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)