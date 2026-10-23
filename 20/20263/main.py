from fastapi import FastAPI, HTTPException
from database import leer_base_datos, obtener_producto,  guardar_base_datos
from shemas import Product

apiRest = FastAPI(
    title="API inventarios SENA",
    description="Mi primera API",
    version="1.0.0"
)

@apiRest.get("/")
async def ruta_principal():
    return {"mensaje": "¡Bienvenido a mi primera API Rest!"}

@apiRest.get("/estado")
async def estado_servidor():
    return {"status": "En linea", "servicios": "operativos"}

@apiRest.get("/suma")
async def suma_dos_numeros():
    suma = 130 + 70
    return {"la suma de 130 y 70 es": suma}

@apiRest.get("/productos")
async def lista_productos():
    datos = await leer_base_datos()
    return {"cantidad": len(datos), "productos": datos}

@apiRest.get("/productos/{codigo_producto}")
async def buscar_un_producto(codigo_producto: str):
    try:
        producto = await obtener_producto(codigo_producto)
        return producto
    except KeyError:
        raise HTTPException(status_code=404, detail="El producto solicitado no existe en la BD.")

@apiRest.get("/categorias")
async def obtener_categorias():
    datos = await leer_base_datos()
    categorias = set()
    for producto in datos:
        categorias.add(producto["categoria"])
    return {"categorias": sorted(list(categorias))}

@apiRest.get("/alertas/stock")
async def stock_critico():
    datos = await leer_base_datos()
    productos_alerta = []
    for producto in datos:
        if producto["stock"] <= 3:
            productos_alerta.append(producto)
    return {"productos_alerta": productos_alerta}

@apiRest.get("/productos/buscar/{palabra_clave}")
async def buscar_producto(palabra_clave: str):
    datos = await leer_base_datos()
    resultados = []
    clave = palabra_clave.lower()
    for producto in datos:
        if clave in producto["nombre"].lower():
            resultados.append(producto)
    return {"palabra_buscada": palabra_clave, "resultados": resultados}


@apiRest.post("/productos", status_code=201)
async def registrar_nuevo_producto(producto: Product):
    datos = await leer_base_datos()
    for dato in datos:
        if dato["codigo"] == producto.codigo:
            raise HTTPException(status_code=400, detail="El producto ya existe en la BD.")
    nuevo_producto = producto.model_dump()
    datos.append(nuevo_producto)
    await guardar_base_datos(datos)
    
    return {"mensaje": "Producto registrado exitosamente", "producto": nuevo_producto}

@apiRest.put("/productos/{codigo_producto}")
async def actualizar_producto(codigo_producto: str, producto_actualizado: Product):
    datos = await leer_base_datos()
    for posicion, dato in enumerate(datos):
        if dato["codigo"] == codigo_producto:
            datos[posicion] = producto_actualizado.model_dump() # Mantener el código original
            
            await guardar_base_datos(datos)
            return {"mensaje": "Producto actualizado exitosamente", "producto": datos[posicion]}
    raise HTTPException(status_code=404, detail="El producto solicitado no existe en la BD.")

from fastapi import FastAPI, HTTPException
from schemas import OrdenCreate, OrdenUpdate
from database import leer_base_datos, guardar_base_datos

apiRest = FastAPI(
    title="Sistema de Órdenes de Servicio - Taller Mecánico",
    description="API para recepción y seguimiento de motocicletas en taller",
    version="1.0.0"
)

# Endpoint 1: Crear orden de ingreso
@apiRest.post("/ordenes", status_code=201, summary="Crear nueva orden de ingreso")
async def crear_orden(orden: OrdenCreate):
    datos = await leer_base_datos()
    
    # Verificar si la placa ya existe con estado distinto de "Entregada"
    for orden_actual in datos:
        if orden_actual["placa"] == orden.placa:
            if orden_actual["estado"] != "Entregada":
                raise HTTPException(
                    status_code=400,
                    detail="La moto ya se encuentra en el taller"
                )
    
    # Crear nueva orden con valores por defecto
    nueva_orden = {
        "placa": orden.placa,
        "modelo": orden.modelo,
        "falla_reportada": orden.falla_reportada,
        "estado": "En diagnóstico",
        "costo_reparacion": 0
    }
    
    datos.append(nueva_orden)
    await guardar_base_datos(datos)
    return nueva_orden

# Endpoint 2: Consultar todas las órdenes
@apiRest.get("/ordenes", summary="Consultar todas las órdenes de servicio")
async def listar_ordenes():
    datos = await leer_base_datos()
    return datos

# Endpoint 3: Actualizar diagnóstico y facturación
@apiRest.put("/ordenes/{placa}", summary="Actualizar estado y costo de reparación")
async def actualizar_orden(placa: str, actualizacion: OrdenUpdate):
    datos = await leer_base_datos()
    
    # Buscar la orden por placa
    indice_encontrado = None
    for indice, orden in enumerate(datos):
        if orden["placa"] == placa:
            indice_encontrado = indice
            break
    
    # Regla 1: Placa no existe
    if indice_encontrado is None:
        raise HTTPException(status_code=404, detail="Placa no encontrada")
    
    # Regla 2: Validar costo si se marca como Reparada
    if actualizacion.nuevo_estado == "Reparada":
        if actualizacion.costo_reparacion <= 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede marcar como reparada sin asignar un costo de reparación"
            )
    
    # Regla 3: Actualizar datos
    datos[indice_encontrado]["estado"] = actualizacion.nuevo_estado
    datos[indice_encontrado]["costo_reparacion"] = actualizacion.costo_reparacion
    
    await guardar_base_datos(datos)
    return datos[indice_encontrado]