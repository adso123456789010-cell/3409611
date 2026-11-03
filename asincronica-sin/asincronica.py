import random
import asyncio
import time

async def descargar_factura(numero_factura):
    espera = random.randint(1,3)
    print(f"[{time.strftime('%X')}]) Factura {numero_factura}:Iniciando descarga... (espera: {espera}s)")
    await asyncio.sleep(espera)
    print(f"[{time.strftime('%X')}]) Factura {numero_factura}: Descarga Finalizada")
    return f"Factura{numero_factura} lista"

async def main():
    print("INICIO DEL PROGRAMA ASISCRONICO")
    inicio = time.time()

    tareas = [
        descargar_factura(1),
        descargar_factura(2),
        descargar_factura(3),
        descargar_factura(4),
        descargar_factura(5),
    ]

    await asyncio.gather(*tareas)

    fin = time.time()
    print("FIN DEL PROGRAMA")
    print(f"Tiempo Total: {fin- inicio:.1f} segundos")

asyncio.run(main())