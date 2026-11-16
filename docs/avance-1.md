# Avance 1 del TP Final

## Diagrama de Clases

## Diagrama de Estados de la Clase Aviso

---
## Tarjetas CRC

|      Clase     | Responsabilidades | Colaboradores |
| :------------: | ----------------- | :-----------: |
|    **Aviso**   | Conservar información de un aviso, cambiar de estado                      | Nota, Estado, Reportante, Operador |
|    **Nota**    | Conservar información de una nota                                         | Aviso |
|   **Estado**   | Permitir/bloquear agregación de notas, devolver resultado de transiciones | Aviso |
| **Reportante** | Generar avisos, agregar notas a avisos                                    | Aviso |
|  **Operador**  | Aceptar avisos, descartar avisos                                          | Aviso |

---
## Pregunta Teórica
La consigna dice que puede agregar notas su reportante
¿Quién verifica eso, el aviso o la capa que recibe al usuario autenticado?

La verificación debería realizarla la capa que recibe al usuario autenticado.

----------