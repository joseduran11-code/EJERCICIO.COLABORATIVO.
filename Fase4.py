from datetime import datetime
import os
from abc import ABC, abstractmethod

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
# Se utiliza cuando los datos del cliente
# no cumplen las validaciones establecidas.
# --------------------------------------------------

class ClienteInvalidoError(Exception):
    pass

# --------------------------------------------------
# CLASE CLIENTE
# Gestiona la información de los clientes
# aplicando encapsulación y validaciones robustas.
# --------------------------------------------------

class Cliente:

    def __init__(
        self,
        nombre,
        documento,
        correo,
        telefono
    ):

        self.validar_nombre(nombre)
        self.validar_documento(documento)
        self.validar_correo(correo)
        self.validar_telefono(telefono)

        self._nombre = nombre
        self._documento = documento
        self._correo = correo
        self._telefono = telefono

    # ----------------------------------------------
    # Validación del nombre.
    # ----------------------------------------------

    def validar_nombre(self, nombre):

        if not nombre:

            raise ClienteInvalidoError(
                "El nombre no puede estar vacío."
            )

        if len(nombre.strip()) < 3:

            raise ClienteInvalidoError(
                "El nombre debe tener al menos 3 caracteres."
            )

    # ----------------------------------------------
    # Validación del documento.
    # ----------------------------------------------

    def validar_documento(self, documento):

        if not documento.isdigit():

            raise ClienteInvalidoError(
                "El documento debe contener solo números."
            )

        if len(documento) < 5:

            raise ClienteInvalidoError(
                "Documento inválido."
            )

    # ----------------------------------------------
    # Validación del correo.
    # ----------------------------------------------

    def validar_correo(self, correo):

        if "@" not in correo or "." not in correo:

            raise ClienteInvalidoError(
                "Correo electrónico inválido."
            )

    # ----------------------------------------------
    # Validación del teléfono.
    # ----------------------------------------------

    def validar_telefono(self, telefono):

        if not telefono.isdigit():

            raise ClienteInvalidoError(
                "El teléfono debe contener solo números."
            )

        if len(telefono) < 7:

            raise ClienteInvalidoError(
                "Número telefónico inválido."
            )

    # ----------------------------------------------
    # Métodos GET para acceder a los atributos.
    # ----------------------------------------------

    def get_nombre(self):
        return self._nombre

    def get_documento(self):
        return self._documento

    def get_correo(self):
        return self._correo

    def get_telefono(self):
        return self._telefono

    # ----------------------------------------------
    # Actualiza el correo validando previamente.
    # ----------------------------------------------

    def actualizar_correo(self, nuevo_correo):

        self.validar_correo(
            nuevo_correo
        )

        self._correo = nuevo_correo

        registrar_log(
            "EVENTO",
            f"Correo actualizado para {self._nombre}"
        )

    # ----------------------------------------------
    # Actualiza el teléfono validando previamente.
    # ----------------------------------------------

    def actualizar_telefono(self, nuevo_telefono):

        self.validar_telefono(
            nuevo_telefono
        )

        self._telefono = nuevo_telefono

        registrar_log(
            "EVENTO",
            f"Teléfono actualizado para {self._nombre}"
        )

    # ----------------------------------------------
    # Retorna toda la información del cliente.
    # ----------------------------------------------

    def obtener_datos(self):

        return (
            f"Nombre: {self._nombre}\n"
            f"Documento: {self._documento}\n"
            f"Correo: {self._correo}\n"
            f"Teléfono: {self._telefono}"
        )

# -----------------------------------------------------
# INTEGRANTE 2: EXCEPCION PERSONALIZADA DE SERVICIOS
# -----------------------------------------------------

class ServicioInvalidoError(Exception):
    pass
    
# ----------------------------------------------
# CLASE ABSTRACTA SERVICIO
# se define la estructura general de los 
# servicios que ofrece la empresa 
# ----------------------------------------------

class Servicio(ABC):

    def __init__(self, codigo, nombre, precio, disponible=True):

        # VALIDAR CODIGO
        if not isinstance(codigo, str) or not codigo.strip():
            raise ServicioInvalidoError(
                "El codigo del servicio es obligatorio."
            )

        # VALIDAR NOMBRE
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        # VALIDAR PRECIO
        if (
            not isinstance(precio, (int, float))
            or isinstance(precio, bool)
            or precio <= 0
        ):
            raise ServicioInvalidoError(
                "El precio debe ser un numero mayor que cero."
            )

        # VALIDAR DISPONIBILIDAD
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        # ATRIBUTOS DEL SERVICIO
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._disponible = disponible

    # ----------------------------------------------
    # METODOS GET PARA CONSULTAR LOS ATRIBUTOS
    # ----------------------------------------------
    
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

    # ----------------------------------------------
    # METODO PARA CAMBIAR LA DISPONIBILIDAD
    # ----------------------------------------------
    
    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise ServicioInvalidoError(
                "El estado debe ser verdadero o falso."
            )

        self._disponible = estado

    # ----------------------------------------------
    # METODOS ABSTRACTOS
    # Las clases hijas deben implementarlos para 
    # que pueda operarse.
    # ----------------------------------------------
    
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, parametro):
        pass

# --------------------------------------------------
# PRUEBAS
# --------------------------------------------------


# PRUEBA 1: REGISTRO DE CLIENTE

print("\n   PRUEBA 1: REGISTRO DE CLIENTE   ")

try:
    cliente1 = Cliente(
        "Angel Mendoza",
        "10422457",
        "angel@gmail.com",
        "3012323232"
    )

    print("Cliente registrado correctamente.")
    print(cliente1.obtener_datos())

    registrar_log("EVENTO", "Cliente registrado correctamente.")

except ClienteInvalidoError as error:
    print("Error:", error)
    registrar_log("ERROR", str(error))


# PRUEBA 2: ACTUALIZAR DATOS

print("\n   PRUEBA 2: ACTUALIZAR DATOS   ")

try:
    cliente1.actualizar_correo("angel.men@gmail.com")
    cliente1.actualizar_telefono("3019898989")

    print("Datos actualizados correctamente.")
    print(cliente1.obtener_datos())

except ClienteInvalidoError as error:
    print("Error:", error)
    registrar_log("ERROR", str(error))


# PRUEBA 3: CLIENTE INVALIDO

print("\n   PRUEBA 3: CLIENTE INVALIDO   ")

try:
    cliente2 = Cliente("", "ABC", "correoinvalido", "123")

    print("Cliente creado correctamente.")

except ClienteInvalidoError as error:
    print("Excepcion detectada:", error)
    registrar_log("ERROR", str(error))


# PRUEBA 4: CLASE ABSTRACTA SERVICIO

print("\n   PRUEBA 4: CLASE ABSTRACTA SERVICIO   ")

try:
    servicio1 = Servicio("S01", "Sala de reuniones", 40000)

except TypeError:
    print("No se puede crear directamente un objeto de Servicio.")
