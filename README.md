# EJERCICIO COLABORATIVO - Software FJ
Curso Programación (213023) - UNAD. Fase 4: Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Sistema orientado a objetos en Python, sin bases de datos. Solo se usan listas internas y un archivo `logs.txt` para eventos y errores.

## Estructura
| Archivo | Integrante | Contenido |
|---|---|---|
| `entidad_base.py` | 5 | Clase abstracta `Entidad`; Cliente, Servicio y Reserva se registran como entidades desde el main |
| `integrante1_clientes.py` | 1 | Clase `Cliente`, validaciones, `ClienteInvalidoError`, `registrar_log` |
| `integrante2_servicio.py` | 2 | Clase abstracta `Servicio`, `ServicioInvalidoError` |
| `integrante3_servicios_especializados.py` | 3 | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `integrante4_reservas.py` | 4 | Clase `Reserva`, estados, excepciones de reserva |
| `integrante5_main.py` | 5 | `GestorSoftwareFJ`, `Simulador` y simulación de 25 operaciones |

## Ejecución
```
python integrante5_main.py
```
Genera `logs.txt` en la misma carpeta. Cada archivo de integrante también se puede ejecutar por separado para ver sus pruebas.

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` (ABC con métodos abstractos).
- **Herencia y polimorfismo:** tres servicios sobrescriben `calcular_costo`, `describir` y `validar_parametros`.
- **Encapsulación:** atributos privados con getters/properties.
- **Sobrecarga:** `calcular_costo(duracion, impuesto, descuento, **opciones)` y `estimar_costo` con parámetros opcionales.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from`).
- **Logs:** cada error y evento relevante queda en `logs.txt`.
