# #definir variables 

# nombre_producto = "Llantas Pirelli"
precio = 43000
# stock = 12
# activo = True 

# print(f"producto{nombre_producto} | Precio : {precio}")

# # 2. condiciones 

# if stock > 0 and activo:
#     print("producto disponible para la venta")
# elif stock == 0:
#     print("producto agotado")
# else:
#     print("producto inactivo")

categorias = ["Lubricantes", "Repuestos", "Accesorios"]

for categoria in categorias:
    print(f"Revisando categoria: {categoria}")

# usamos "def" en lugar de "funtion" 0 "() =>"
def calcular_descuento(precio_base, porcentaje):
    descuento = precio_base * (porcentaje / 100)
    return precio_base - descuento

precio_final = calcular_descuento(precio, 10)
print(f"precio con decuento: ${precio_final}")