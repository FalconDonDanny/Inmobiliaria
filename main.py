from datetime import datetime
from pymongo import MongoClient

# Conexión directa sin manejo avanzado de excepciones
client = MongoClient("mongodb://localhost:27017/")
db = client["inmobiliaria_db"]
coleccion = db["propiedades"]

def precargar_datos():
    if coleccion.count_documents({}) == 0:
        # Precarga de 8 propiedades corregida (sin ceros a la izquierda en datetime)
        propiedades = [
            {"codigo": "P01", "tipo": "Departamento", "precio": 4500, "fecha_publicacion": datetime(2026, 1, 10), "ubicacion": {"comuna": "Puente Alto", "calle": "Concha y Toro"}, "historial_visitas": [{"visitante": "Andres", "interesado": True}]},
            {"codigo": "P02", "tipo": "Casa", "precio": 8500, "fecha_publicacion": datetime(2026, 2, 12), "ubicacion": {"comuna": "La Florida", "calle": "Vicuna Mackenna"}, "historial_visitas": []},
            {"codigo": "P03", "tipo": "Departamento", "precio": 3200, "fecha_publicacion": datetime(2026, 3, 5), "ubicacion": {"comuna": "Santiago Centro", "calle": "Alameda"}, "historial_visitas": [{"visitante": "Beatriz", "interesado": False}]},
            {"codigo": "P04", "tipo": "Casa", "precio": 12000, "fecha_publicacion": datetime(2026, 3, 22), "ubicacion": {"comuna": "Pirque", "calle": "Ramon Subercaseaux"}, "historial_visitas": [{"visitante": "Carlos", "interesado": True}, {"visitante": "Daniela", "interesado": True}]},
            {"codigo": "P05", "tipo": "Departamento", "precio": 5200, "fecha_publicacion": datetime(2026, 4, 15), "ubicacion": {"comuna": "San Miguel", "calle": "Gran Avenida"}, "historial_visitas": [{"visitante": "Eduardo", "interesado": False}]},
            {"codigo": "P06", "tipo": "Casa", "precio": 9500, "fecha_publicacion": datetime(2026, 5, 1), "ubicacion": {"comuna": "Puente Alto", "calle": "San Carlos"}, "historial_visitas": []},
            {"codigo": "P07", "tipo": "Departamento", "precio": 2900, "fecha_publicacion": datetime(2026, 5, 18), "ubicacion": {"comuna": "Estacion Central", "calle": "Ecuador"}, "historial_visitas": [{"visitante": "Felipe", "interesado": True}]},
            {"codigo": "P08", "tipo": "Casa", "precio": 11000, "fecha_publicacion": datetime(2026, 6, 2), "ubicacion": {"comuna": "Macul", "calle": "Macul"}, "historial_visitas": [{"visitante": "Gabriela", "interesado": False}]}
        ]
        coleccion.insert_many(propiedades)
        print("[+] 8 Propiedades inmobiliarias cargadas exitosamente.")

def crear_documento():
    codigo = input("Codigo: ")
    tipo = input("Tipo (Casa/Departamento): ")
    precio = float(input("Precio (UF): "))
    fecha = datetime.strptime(input("Fecha de publicacion (YYYY-MM-DD): "), "%Y-%m-%d")
    comuna = input("Comuna: ")
    calle = input("Calle: ")
    
    visitas = []
    if input("¿Desea registrar una visita inicial? (s/n): ") == "s":
        visitante = input("Nombre visitante: ")
        interesado = input("¿Esta interesado? (s/n): ") == "s"
        visitas.append({"visitante": visitante, "interesado": interesado})
        
    doc = {
        "codigo": codigo, "tipo": tipo, "precio": precio, 
        "fecha_publicacion": fecha, "ubicacion": {"comuna": comuna, "calle": calle}, 
        "historial_visitas": visitas
    }
    coleccion.insert_one(doc)
    print("Propiedad guardada.")

def listar_documentos():
    for doc in coleccion.find({}, {"codigo": 1, "tipo": 1, "precio": 1, "ubicacion.comuna": 1, "_id": 0}):
        print(doc)

def buscar_operador():
    max_precio = float(input("Buscar propiedades con precio UF menor o igual a ($lte): "))
    for doc in coleccion.find({"precio": {"$lte": max_precio}}):
        print(doc)

def buscar_regex():
    comuna_buscar = input("Comuna a buscar con Regex: ")
    for doc in coleccion.find({"ubicacion.comuna": {"$regex": comuna_buscar, "$options": "i"}}):
        print(doc)

def buscar_fechas():
    f1 = datetime.strptime(input("Desde (YYYY-MM-DD): "), "%Y-%m-%d")
    f2 = datetime.strptime(input("Hasta (YYYY-MM-DD): "), "%Y-%m-%d")
    for doc in coleccion.find({"fecha_publicacion": {"$gte": f1, "$lte": f2}}):
        print(doc)

def buscar_subdocumento_array():
    nombre_visitante = input("Nombre del visitante en el historial a buscar: ")
    for doc in coleccion.find({"historial_visitas.visitante": nombre_visitante}):
        print(doc)

def actualizar_raiz():
    codigo = input("Codigo de propiedad a modificar: ")
    nuevo_precio = float(input("Nuevo precio (UF): "))
    coleccion.update_one({"codigo": codigo}, {"$set": {"precio": nuevo_precio}})
    print("Precio actualizado en la raiz.")

def actualizar_sub_array():
    codigo = input("Codigo de propiedad: ")
    nueva_calle = input("Nueva calle en el subdocumento: ")
    coleccion.update_one({"codigo": codigo}, {"$set": {"ubicacion.calle": nueva_calle}})
    print("Calle del subdocumento actualizada.")

def eliminar_documento():
    codigo = input("Codigo de la propiedad a eliminar: ")
    coleccion.delete_one({"codigo": codigo})
    print("Documento eliminado.")

def pipeline_agregacion():
    pipeline = [
        {"$match": {"tipo": "Departamento"}},
        {"$group": {"_id": "$ubicacion.comuna", "precio_promedio": {"$avg": "$precio"}}}
    ]
    for res in coleccion.aggregate(pipeline):
        print(f"Comuna: {res['_id']} | Promedio UF Departamentos: {res['precio_promedio']}")

def menu():
    precargar_datos()
    while True:
        print("\n--- SISTEMA DE GESTION INMOBILIARIA ---")
        print("1. Agregar Propiedad\n2. Listar Propiedades\n3. Buscar por Precio Max ($lte)\n4. Buscar Comuna por Regex\n5. Buscar por Rango Fechas\n6. Buscar Visitante\n7. Modificar Precio\n8. Modificar Calle\n9. Eliminar Propiedad\n10. Reporte Promedio Departamentos\n11. Salir")
        op = input("Seleccione opcion: ")
        if op == "1": crear_documento()
        elif op == "2": listar_documentos()
        elif op == "3": buscar_operador()
        elif op == "4": buscar_regex()
        elif op == "5": buscar_fechas()
        elif op == "6": buscar_subdocumento_array()
        elif op == "7": actualizar_raiz()
        elif op == "8": actualizar_sub_array()
        elif op == "9": eliminar_documento()
        elif op == "10": pipeline_agregacion()
        elif op == "11": break

if _name_ == "_main_":
    menu()
