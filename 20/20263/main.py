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
