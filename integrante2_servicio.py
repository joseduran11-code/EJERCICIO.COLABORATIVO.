from abc import ABC, abstractmethod
from datetime import datetime
import os


# --------------------------------------------------
# FUNCIÓN: registrar_log
# Permite registrar eventos y errores dentro
# del archivo logs.txt junto con fecha y hora.
# --------------------------------------------------

def registrar_log(tipo, mensaje):

    ruta_log = os.path.join(
        os.path.dirname(__file__),
        "logs.txt"
    )

    with open(
        ruta_log,
        "a",
        encoding="utf-8"
    ) as archivo:

        fecha_hora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        archivo.write(
            "\n" + "=" * 50 + "\n"
        )

        archivo.write(
            f"Fecha: {fecha_hora}\n\n"
        )

        archivo.write(
            f"{tipo}:\n{mensaje}\n"
        )

        archivo.write(
            "=" * 50 + "\n"
        )

# --------------------------------------------------
# EXCEPCIÓN PERSONALIZADA
# Se utiliza cuando los datos del servicio
# no cumplen las validaciones establecidas.
# --------------------------------------------------

class ServicioInvalidoError(Exception):
    pass

# --------------------------------------------------
# CLASE ABSTRACTA: SERVICIO
# Define la estructura general para todos los
# servicios que ofrece la empresa Software FJ.
#
# Esta clase implementa:
# - Encapsulación
# - Validaciones robustas
# - Métodos abstractos
# - Preparación para herencia y polimorfismo
# --------------------------------------------------

class Servicio(ABC):

    def __init__(
        self,
        codigo,
        nombre,
        precio,
        disponible=True
    ):

        # Validación de código

        if not isinstance(codigo, str) or not codigo.strip():

            raise ServicioInvalidoError(
                "El codigo del servicio es obligatorio."
            )

        # Validación de nombre

        if not isinstance(nombre, str) or not nombre.strip():

            raise ServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        # Validación de precio

        if (
            not isinstance(precio, (int, float))
            or isinstance(precio, bool)
            or precio <= 0
        ):

            raise ServicioInvalidoError(
                "El precio debe ser un numero mayor que cero."
            )

        # Validación de disponibilidad

        if not isinstance(disponible, bool):

            raise ServicioInvalidoError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        # Atributos privados

        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._disponible = disponible

    # --------------------------------------------------
    # Métodos GET para acceso controlado
    # a los atributos del servicio.
    # --------------------------------------------------

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def disponible(self):
        return self._disponible

    # --------------------------------------------------
    # Permite cambiar la disponibilidad del servicio.
    # --------------------------------------------------

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):

            raise ServicioInvalidoError(
                "El estado debe ser verdadero o falso."
            )

        self._disponible = estado

        registrar_log(
            "EVENTO",
            f"Disponibilidad actualizada para el servicio {self._nombre}"
        )

    # --------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # Las clases hijas deben implementar estos métodos.
    # --------------------------------------------------

    @abstractmethod
    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(
        self,
        parametro
    ):
        pass

# --------------------------------------------------
# PRUEBA 1
# Verificación de clase abstracta.
# --------------------------------------------------

print(
    "\nPRUEBA 1: CLASE ABSTRACTA SERVICIO\n"
)

try:

    servicio1 = Servicio(
        "S01",
        "Sala de reuniones",
        40000
    )

except TypeError:

    print(
        "No se puede crear directamente un objeto de Servicio."
    )

    registrar_log(
        "EVENTO",
        "Prueba correcta de clase abstracta Servicio."
    )

# --------------------------------------------------
# PRUEBA 2
# Validación de datos inválidos.
# --------------------------------------------------

print(
    "\nPRUEBA 2: VALIDACION DE DATOS\n"
)

try:

    servicio2 = Servicio(
        "",
        "",
        -5000
    )

except Exception as error:

    print(
        f"ERROR: {error}"
    )

    registrar_log(
        "ERROR",
        str(error)
    )
