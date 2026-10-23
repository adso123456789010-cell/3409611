inventario_tienda = [
    {"nombre": "Llanta Trasera Voge 300 DS", "categoria": "Repuestos", "precio": 280000, "stock": 4},
    {"nombre": "Kit Arrastre Suzuki Gixxer 150", "categoria": "Repuestos", "precio": 120000, "stock": 15},
    {"nombre": "Exploradoras LED Dominar 400", "categoria": "Accesorios", "precio": 150000, "stock": 8},
    {"nombre": "Pastillas Freno Gixxer 150", "categoria": "Repuestos", "precio": 45000, "stock": 0},
    {"nombre": "Soporte Celular Aluminio", "categoria": "Accesorios", "precio": 60000, "stock": 3}
]

def procesar_inventario(productos):
    for producto in productos:
        if producto["stock"] <= 5:
          print(f"Alerta:{producto["nombre"]}")
        
        
        if producto["categoria"] == "Accesorios":
            producto["precio"] = producto["precio"] * 0.9
            print(f"El precio actualizado es {producto["precio"]}")

        elif producto["stock"] == 0:
            print(f"Producto agotado: {producto['nombre']}")
    
        

procesar_inventario(inventario_tienda)