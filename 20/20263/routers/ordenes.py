from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from schemas import OrdenCreate, OrdenPatch, OrdenUpdate
from database import leer_base_datos, guardar_base_datos
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import json


router = APIRouter(prefix="/ordenes", tags=["Gestionar ordenes"])


@router.get("/")
async def obtener_ordenes(estado: Optional[str] = None):
    datos = await leer_base_datos()

    # Si el cliente envia un estado:
    if estado: # Si el estado contiene algo va a ser true, sino va a ser false
        datos_filtrados = [orden for orden in datos if orden["estado"].lower() == estado.lower()]
        return {"total_ordenes": len(datos_filtrados), "ordenes": datos_filtrados}
    
    return {"total_ordenes": len(datos), "ordenes": datos}

@router.post("/", status_code=201)
async def crear_orden(orden: OrdenCreate):
    datos = await leer_base_datos()
    
    # Regla de Negocio: Validar que la placa no esté ya en el taller
    for item in datos:
        if item["placa"] == orden.placa and item["estado"] != "Entregada":
            raise HTTPException(
                status_code=400, 
                detail=f"La moto con placa {orden.placa} ya se encuentra en el taller ({item['estado']})."
            )
            
    nueva_orden = orden.model_dump()
    nueva_orden["estado"] = "En diagnóstico"
    nueva_orden["costo_reparacion"] = 0.0
    
    datos.routerend(nueva_orden)
    await guardar_base_datos(datos)
    
    return {"mensaje": "Orden creada exitosamente", "orden": nueva_orden}


@router.get("/paginadas")
async def obtener_ordenes_paginadas(
    skip: int = Query(0, description="Cuantos registros saltar"),
    limit: int = Query(10, description="Limite de registros a devolver")
):
    datos = await leer_base_datos()

    # Slicing
    datos_paginados = datos[skip: skip + limit]

    return {
        "mostrando": len(datos_paginados),
        "total_bd": len(datos),
        "skip": skip,
        "limit": limit,
        "ordenes": datos_paginados
    }

@router.put("/{placa}")
async def actualizar_orden(placa: str, orden_update: OrdenUpdate):
        
    datos = await leer_base_datos()
    
    for i, item in enumerate(datos):
        if item["placa"] == placa:
            
            datos[i]["estado"] = orden_update.nuevo_estado
            datos[i]["costo_reparacion"] = orden_update.costo_reparacion
            
            await guardar_base_datos(datos)
            return {"mensaje": "Orden actualizada correctamente", "orden": datos[i]}
            
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.delete("/{placa}", status_code=204)
async def eliminar_orden(placa: str):
    datos = await leer_base_datos()

    # for orden in datos:
    #     if orden["placa"] != placa:
    #         datos_filtrados.routerend(orden)

    datos_filtrados = [orden for orden in datos if orden["placa"] != placa]

    if len(datos) == len(datos_filtrados):
        raise HTTPException(status_code=404, detail="La orden no existe.")

    await guardar_base_datos(datos_filtrados)

    return None

@router.patch("/{placa}")
async def actualizacion_parcial(placa: str, orden_patch: OrdenPatch):
    datos = await leer_base_datos()

    for i, orden in enumerate(datos):
        if orden["placa"] == placa:
            datos_a_actualizar = orden_patch.model_dump(exclude_unset=True)

            # Actualizamos solo con los datos que llegaron
            datos[i].update(datos_a_actualizar)

            await guardar_base_datos(datos)
            return {"mesaje": "La orden ha sido actualizada con los siguientes datos", "orden": datos[i]}

    raise HTTPException(status_code=404, detail="La orden no existe.")

class OrdenResponse(BaseModel):
    id: Optional[int] = None
    estado: str
    modelo: str
    costo_reparacion: float

JSON_FILE = "inventario.json"

def leer_json():
    with open(JSON_FILE, "r") as file:
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def escribir_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@router.get("/", response_model=List[dict])
def obtener_ordenes():
    return leer_json()

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_orden(orden: OrdenResponse):
    datos = leer_json()
    orden.id = len(datos) + 1
    datos.append(orden.dict())
    escribir_json(datos)
    return {"mensaje": "Orden creada exitosamente", "orden": orden.dict}

@router.put("/{orden_id}", response_model=OrdenResponse)
def actualizar_orden(orden_id: int, orden_update: OrdenUpdate):
    datos = leer_json()
    for i, orden in enumerate(datos):
        if orden["id"] == orden_id:
            datos[i]["estado"] = orden_update.nuevo_estado
            datos[i]["costo_reparacion"] = orden_update.costo_reparacion
            escribir_json(datos)
            return {"mensaje": "Orden actualizada correctamente", "orden": datos[i]}
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.delete("/{orden_id}", status_code=204)
def eliminar_orden(orden_id: int):
    datos = leer_json()
    datos_filtrados = [orden for orden in datos if orden["id"] != orden_id]

    if len(datos) == len(datos_filtrados):
        raise HTTPException(status_code=404, detail="La orden no existe.")

    escribir_json(datos_filtrados)
    return None

@router.get("/")
def filtrar_ordenes(
    estado: Optional[str] = None,
    modelo: Optional[str] = None,
    costo_reparacion: Optional[float] = None,
):
    ordenes = leer_json()
    resultado = ordenes

    if estado:
        resultado = [o for o in resultado if o["estado"].lower() == estado.lower()]
    
    if modelo:
        resultado = [o for o in resultado if o["modelo"].lower() == modelo.lower()]

    if costo_reparacion is not None:
        resultado = [o for o in resultado if o["costo_reparacion"] == costo_reparacion]

    return{
        "cantidad_encontrada": len(resultado),
        "ordenes": resultado
    }