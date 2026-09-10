import json
from wsgiref.simple_server import make_server
tareas = {}
siguiente_id = 1

def mi_app_wsgi(environ, start_response):
    global siguiente_id
    
    metodo = environ.get('REQUEST_METHOD', 'GET')
    ruta = environ.get('PATH_INFO', '/')
    
    def leer_cuerpo():
        tamano = int(environ.get('CONTENT_LENGTH', 0))
        cuerpo_bytes = environ['wsgi.input'].read(tamano)
        return json.loads(cuerpo_bytes.decode('utf-8'))

    def responder(estado, datos):
        headers = [('Content-type', 'application/json')]
        start_response(estado, headers)
        return [json.dumps(datos).encode('utf-8')]

    partes_ruta = ruta.strip('/').split('/')

    
    if len(partes_ruta) == 1 and partes_ruta[0] == 'tasks':
        
        if metodo == 'GET':
            return responder('200 OK', list(tareas.values()))
            
        elif metodo == 'POST':
            nueva_tarea = leer_cuerpo()
            nueva_tarea['id'] = siguiente_id
            tareas[siguiente_id] = nueva_tarea
            siguiente_id += 1
            return responder('201 Created', nueva_tarea)
            
        else:
            return responder('405 Method Not Allowed', {"error": "Verbo no soportado"})

    elif len(partes_ruta) == 2 and partes_ruta[0] == 'tasks':
        try:
            id_tarea = int(partes_ruta[1])
        except ValueError:
            return responder('400 Bad Request', {"error": "El ID debe ser un numero"})

        if id_tarea not in tareas:
            return responder('404 Not Found', {"error": "Tarea no encontrada"})

        if metodo == 'GET':
            return responder('200 OK', tareas[id_tarea])

        elif metodo == 'PATCH':
            datos_actualizar = leer_cuerpo()
            tareas[id_tarea].update(datos_actualizar)
            return responder('200 OK', tareas[id_tarea])

        elif metodo == 'DELETE':
            del tareas[id_tarea]
            return responder('200 OK', {"mensaje": "Tarea eliminada"})

        else:
            return responder('405 Method Not Allowed', {"error": "Verbo no soportado"})

    else:
        return responder('404 Not Found', {"error": "Ruta no encontrada"})


if __name__ == '__main__':
    host = 'localhost'
    puerto = 9292
    servidor = make_server(host, puerto, mi_app_wsgi)
    print(f"Servidor API REST en http://{host}:{puerto}")
    servidor.serve_forever()