Diferencia entre `GET`, `POST`, `PATCH` y `DELETE`, y por qué `POST` no es idempotente:

1)El verbo GET te permite leer o obtener elementos del servidor, mientras que el POST crea un elemento cada vez que se usa en el server , el PATCH que modifica los datos de dichos elementos del server y el DELETE que elimina un elemento del server que sí exista.

2) POST no es idempotente basicamente porque cada ve que se ejecuta da un resultado distinto por como funciona post a la hora de crear elementos.
