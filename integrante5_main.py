import contextlib
import io
import os

from entidad_base import Entidad

# --------------------------------------------------
# IMPORTACION SILENCIOSA DE LOS MODULOS DE LOS DEMAS
# INTEGRANTES.
# Los archivos de los integrantes 1 y 2 ejecutan sus
# propias pruebas al importarse. Para que no ensucien
# la salida ni el archivo logs.txt de esta simulacion,
# se silencia la consola durante la importacion y se
# devuelve logs.txt al tamano que tenia antes.
# --------------------------------------------------

_RUTA_LOG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "logs.txt"
)
_LOG_EXISTIA = os.path.exists(_RUTA_LOG)
_TAMANO_LOG = os.path.getsize(_RUTA_LOG) if _LOG_EXISTIA else 0

with contextlib.redirect_stdout(io.StringIO()):
    from integrante1_clientes import Cliente, ClienteInvalidoError
    from integrante2_servicio import (
        Servicio,
        ServicioInvalidoError,
        registrar_log
    )
    from integrante3_servicios_especializados import (
        ReservaSala,
        AlquilerEquipo,
        AsesoriaEspecializada
    )
    from integrante4_reservas import (
        Reserva,
        ReservaInvalidaError,
        EstadoReservaError,
        ServicioNoDisponibleError
    )

# Se descartan los registros generados por las pruebas importadas
if os.path.exists(_RUTA_LOG):
    if _LOG_EXISTIA:
        with open(_RUTA_LOG, "r+", encoding="utf-8") as _archivo:
            _archivo.truncate(_TAMANO_LOG)
    else:
        os.remove(_RUTA_LOG)

# --------------------------------------------------
# REGISTRO DE LAS CLASES EXISTENTES COMO ENTIDADES
# Cliente, Servicio y Reserva se declaran subclases
# virtuales de la clase abstracta Entidad, sin tener
# que modificar los archivos de los demas integrantes.
# --------------------------------------------------

Entidad.register(Cliente)
Entidad.register(Servicio)
Entidad.register(Reserva)


# --------------------------------------------------
# INTEGRANTE 5: INTEGRACION DEL SISTEMA Y SIMULACION
# Este archivo une las clases de los integrantes 1, 2,
# 3 y 4 en un gestor central (Software FJ) y ejecuta
# la simulacion de operaciones validas e invalidas.
# El programa nunca se detiene ante un error: cada
# fallo se captura, se muestra y se guarda en logs.txt
# --------------------------------------------------


# --------------------------------------------------
# EXCEPCION PERSONALIZADA DEL SISTEMA
# Se usa para errores propios del gestor (duplicados,
# tipos desconocidos, elementos no encontrados, etc.)
# y para encadenar errores de las capas inferiores.
# --------------------------------------------------

class SistemaError(Exception):
    pass


# --------------------------------------------------
# CLASE GESTOR SOFTWARE FJ
# Administra las listas internas de clientes,
# servicios y reservas (no se usan bases de datos).
# --------------------------------------------------

def datos_de(entidad):
    # Retorna la informacion de cualquier entidad del sistema
    # (polimorfismo): usa obtener_datos() o, en los servicios,
    # describir().
    if not isinstance(entidad, Entidad):
        raise SistemaError("El objeto no es una entidad del sistema.")

    if hasattr(entidad, "obtener_datos"):
        return entidad.obtener_datos()

    return entidad.describir()


class GestorSoftwareFJ:

    # Tipos de servicio disponibles (clase hija por tipo)
    TIPOS_SERVICIO = {
        "SALA": ReservaSala,
        "EQUIPO": AlquilerEquipo,
        "ASESORIA": AsesoriaEspecializada
    }

    def __init__(self):

        # Listas internas encapsuladas
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # ----------------------------------------------
    # CLIENTES
    # ----------------------------------------------

    def buscar_cliente(self, documento):

        # Retorna el cliente con ese documento o lanza error.
        for cliente in self._clientes:
            if cliente.get_documento() == documento:
                return cliente

        raise SistemaError(
            f"No existe un cliente con documento {documento}."
        )

    def registrar_cliente(self, nombre, documento, correo, telefono):

        try:
            # Evita documentos duplicados
            for cliente in self._clientes:
                if cliente.get_documento() == documento:
                    raise SistemaError(
                        f"El documento {documento} ya esta registrado."
                    )

            cliente = Cliente(nombre, documento, correo, telefono)

        except ClienteInvalidoError as error:
            # Encadenamiento: se conserva la causa original
            raise SistemaError(
                "No se pudo registrar el cliente."
            ) from error

        except (TypeError, AttributeError) as error:
            # Datos faltantes o de tipo incorrecto (por ejemplo None)
            raise SistemaError(
                "Los datos del cliente estan incompletos o son de "
                "un tipo incorrecto."
            ) from error

        else:
            self._clientes.append(cliente)
            registrar_log(
                "EVENTO",
                f"Cliente {cliente.get_nombre()} registrado en el sistema."
            )
            return cliente

        finally:
            registrar_log(
                "EVENTO",
                f"Finalizo el intento de registrar al cliente "
                f"con documento {documento}."
            )

    # ----------------------------------------------
    # SERVICIOS
    # ----------------------------------------------

    def buscar_servicio(self, codigo):

        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio

        raise SistemaError(
            f"No existe un servicio con codigo {codigo}."
        )

    def crear_servicio(self, tipo, codigo, nombre, precio, disponible=True):

        try:
            clase = self.TIPOS_SERVICIO.get(str(tipo).upper())

            if clase is None:
                raise SistemaError(
                    f"El tipo de servicio '{tipo}' no existe."
                )

            for servicio in self._servicios:
                if servicio.codigo == codigo:
                    raise SistemaError(
                        f"El codigo de servicio {codigo} ya existe."
                    )

            servicio = clase(codigo, nombre, precio, disponible)

        except ServicioInvalidoError as error:
            raise SistemaError(
                "No se pudo crear el servicio."
            ) from error

        else:
            self._servicios.append(servicio)
            registrar_log(
                "EVENTO",
                f"Servicio {servicio.nombre} creado correctamente."
            )
            return servicio

        finally:
            registrar_log(
                "EVENTO",
                f"Finalizo el intento de crear el servicio {codigo}."
            )

    # ----------------------------------------------
    # RESERVAS
    # ----------------------------------------------

    def crear_reserva(self, documento, codigo_servicio, duracion):

        cliente = self.buscar_cliente(documento)
        servicio = self.buscar_servicio(codigo_servicio)

        reserva = Reserva(cliente, servicio, duracion)
        self._reservas.append(reserva)

        return reserva

    # ----------------------------------------------
    # CALCULO DE COSTOS (METODO SOBRECARGADO)
    # Admite parametros opcionales: impuesto, descuento
    # y opciones extra (por ejemplo cantidad de equipos).
    # ----------------------------------------------

    def estimar_costo(
        self,
        codigo_servicio,
        duracion,
        impuesto=0.0,
        descuento=0.0,
        **opciones
    ):

        servicio = self.buscar_servicio(codigo_servicio)

        try:
            return servicio.calcular_costo(
                duracion,
                impuesto,
                descuento,
                **opciones
            )

        except (ValueError, TypeError, ServicioInvalidoError) as error:
            raise SistemaError(
                "El calculo del costo es inconsistente."
            ) from error

    # ----------------------------------------------
    # REPORTES
    # ----------------------------------------------

    def promedio_costo_por_estado(self, estado):

        # Promedio de costo de reservas en un estado dado.
        # Si no hay reservas se produce ZeroDivisionError,
        # que se convierte en un error controlado del sistema.
        costos = [
            r.costo_total for r in self._reservas
            if r.estado == estado and r.costo_total is not None
        ]

        try:
            return sum(costos) / len(costos)

        except ZeroDivisionError as error:
            raise SistemaError(
                f"No hay reservas con costo en estado {estado}."
            ) from error

    def resumen(self):

        estados = {}

        for reserva in self._reservas:
            estados[reserva.estado] = estados.get(reserva.estado, 0) + 1

        lineas = [
            f"Clientes registrados: {len(self._clientes)}",
            f"Servicios creados:    {len(self._servicios)}",
            f"Reservas creadas:     {len(self._reservas)}"
        ]

        for estado, cantidad in estados.items():
            lineas.append(f"  - {estado}: {cantidad}")

        return "\n".join(lineas)

    def listar_reservas(self):
        return list(self._reservas)


# --------------------------------------------------
# EJECUTOR DE OPERACIONES
# Corre cada operacion dentro de try/except para que
# ningun error detenga el programa. Cualquier
# excepcion (incluso inesperada) queda en logs.txt.
# --------------------------------------------------

class Simulador:

    def __init__(self):
        self.exitosas = 0
        self.fallidas = 0
        self._numero = 0

    def ejecutar(self, descripcion, operacion):

        self._numero += 1
        print(f"\n--- OPERACION {self._numero}: {descripcion} ---")

        try:
            resultado = operacion()

        except SistemaError as error:
            self.fallidas += 1
            print(f"  [ERROR CONTROLADO] {error}")

            # Si hay una causa encadenada, tambien se muestra
            if error.__cause__ is not None:
                print(f"  Causa original: {error.__cause__}")

            registrar_log(
                "ERROR",
                f"Operacion {self._numero} ({descripcion}): {error}. "
                f"Causa: {error.__cause__}"
            )

        except (ReservaInvalidaError, ServicioInvalidoError,
                ClienteInvalidoError) as error:
            self.fallidas += 1
            print(f"  [ERROR CONTROLADO] {error}")

            if error.__cause__ is not None:
                print(f"  Causa original: {error.__cause__}")

            registrar_log(
                "ERROR",
                f"Operacion {self._numero} ({descripcion}): {error}"
            )

        except Exception as error:
            # Red de seguridad para errores inesperados
            self.fallidas += 1
            print(f"  [ERROR INESPERADO] {type(error).__name__}: {error}")

            registrar_log(
                "ERROR CRITICO",
                f"Operacion {self._numero} ({descripcion}): "
                f"{type(error).__name__}: {error}"
            )

        else:
            self.exitosas += 1
            print("  [OK]", resultado if resultado is not None else "")

        finally:
            registrar_log(
                "EVENTO",
                f"Operacion {self._numero} finalizada: {descripcion}."
            )


# --------------------------------------------------
# FUNCION PRINCIPAL: SIMULACION DE OPERACIONES
# --------------------------------------------------

def main():

    registrar_log("EVENTO", "===== INICIO DE LA SIMULACION SOFTWARE FJ =====")

    gestor = GestorSoftwareFJ()
    sim = Simulador()

    # Guarda reservas para operaciones posteriores
    reservas = {}

    # -------- CLIENTES --------

    sim.ejecutar(
        "Registro valido de cliente (Ana Torres)",
        lambda: gestor.registrar_cliente(
            "Ana Torres", "1043567890", "ana@correo.com", "3001112233"
        ).get_nombre()
    )

    sim.ejecutar(
        "Registro valido de cliente (Luis Perez)",
        lambda: gestor.registrar_cliente(
            "Luis Perez", "72456123", "luis@correo.com", "3105556677"
        ).get_nombre()
    )

    sim.ejecutar(
        "Registro INVALIDO: nombre vacio, documento y correo incorrectos",
        lambda: gestor.registrar_cliente("", "ABC", "correo-malo", "123")
    )

    sim.ejecutar(
        "Registro INVALIDO: datos faltantes (None)",
        lambda: gestor.registrar_cliente("Pedro Gomez", None, None, None)
    )

    sim.ejecutar(
        "Registro INVALIDO: documento duplicado",
        lambda: gestor.registrar_cliente(
            "Ana Duplicada", "1043567890", "otra@correo.com", "3009998877"
        )
    )

    # -------- SERVICIOS --------

    sim.ejecutar(
        "Creacion valida de servicio: sala de reuniones",
        lambda: gestor.crear_servicio(
            "SALA", "S01", "Sala de reuniones", 40000
        ).describir()
    )

    sim.ejecutar(
        "Creacion valida de servicio: alquiler de portatil",
        lambda: gestor.crear_servicio(
            "EQUIPO", "E01", "Portatil", 25000
        ).describir()
    )

    sim.ejecutar(
        "Creacion valida de servicio: asesoria en Python",
        lambda: gestor.crear_servicio(
            "ASESORIA", "A01", "Asesoria en Python", 80000
        ).describir()
    )

    sim.ejecutar(
        "Creacion valida de servicio NO disponible: asesoria en redes",
        lambda: gestor.crear_servicio(
            "ASESORIA", "A02", "Asesoria en redes", 90000, False
        ).describir()
    )

    sim.ejecutar(
        "Creacion INVALIDA de servicio: precio negativo y nombre vacio",
        lambda: gestor.crear_servicio("SALA", "S02", "", -5000)
    )

    sim.ejecutar(
        "Creacion INVALIDA de servicio: tipo inexistente",
        lambda: gestor.crear_servicio("GIMNASIO", "G01", "Gimnasio", 10000)
    )

    # -------- RESERVAS EXITOSAS --------

    def reserva_sala_completa():
        r = gestor.crear_reserva("1043567890", "S01", 3)
        r.confirmar()
        total = r.procesar(impuesto=0.19, descuento=0.10)
        reservas["sala"] = r
        return f"Reserva {r.codigo} procesada. Total: ${total:,.0f}"

    sim.ejecutar(
        "Reserva exitosa de sala (3 horas, IVA 19% y 10% descuento)",
        reserva_sala_completa
    )

    def reserva_equipo_completa():
        r = gestor.crear_reserva("72456123", "E01", 2)
        r.confirmar()
        total = r.procesar(impuesto=0.19, cantidad=3)
        reservas["equipo"] = r
        return f"Reserva {r.codigo} procesada. Total: ${total:,.0f}"

    sim.ejecutar(
        "Reserva exitosa de equipos (2 dias, 3 unidades)",
        reserva_equipo_completa
    )

    # -------- RESERVAS FALLIDAS --------

    sim.ejecutar(
        "Reserva FALLIDA: duracion negativa (excepcion encadenada)",
        lambda: gestor.crear_reserva("1043567890", "S01", -2)
    )

    sim.ejecutar(
        "Reserva FALLIDA: servicio no disponible",
        lambda: gestor.crear_reserva("72456123", "A02", 2)
    )

    sim.ejecutar(
        "Reserva FALLIDA: cliente inexistente",
        lambda: gestor.crear_reserva("99999999", "S01", 2)
    )

    def procesar_sin_confirmar():
        r = gestor.crear_reserva("72456123", "A01", 1)
        reservas["asesoria"] = r
        r.procesar()

    sim.ejecutar(
        "Reserva FALLIDA: procesar sin confirmar",
        procesar_sin_confirmar
    )

    def cancelar_dos_veces():
        r = reservas["asesoria"]
        r.cancelar()
        print("  Estado tras primera cancelacion:", r.estado)
        r.cancelar()

    sim.ejecutar(
        "Reserva FALLIDA: cancelar una reserva ya cancelada",
        cancelar_dos_veces
    )

    sim.ejecutar(
        "Reserva FALLIDA: cancelar una reserva ya procesada",
        lambda: reservas["sala"].cancelar()
    )

    def servicio_deja_de_estar_disponible():
        r = gestor.crear_reserva("1043567890", "A01", 2)
        reservas["asesoria2"] = r
        gestor.buscar_servicio("A01").cambiar_disponibilidad(False)
        r.confirmar()

    sim.ejecutar(
        "Reserva FALLIDA: el servicio se deshabilita antes de confirmar",
        servicio_deja_de_estar_disponible
    )

    # -------- CALCULOS Y REPORTES --------

    sim.ejecutar(
        "Calculo de costo con descuento inconsistente (150%)",
        lambda: gestor.estimar_costo("S01", 2, descuento=1.5)
    )

    sim.ejecutar(
        "Calculo de costo valido (sobrecarga: solo duracion)",
        lambda: f"${gestor.estimar_costo('S01', 2):,.0f}"
    )

    sim.ejecutar(
        "Calculo de costo valido (sobrecarga: con impuesto y cantidad)",
        lambda: f"${gestor.estimar_costo('E01', 2, 0.19, cantidad=2):,.0f}"
    )

    sim.ejecutar(
        "Promedio de reservas PROCESADAS (hay datos)",
        lambda: f"${gestor.promedio_costo_por_estado('PROCESADA'):,.0f}"
    )

    sim.ejecutar(
        "Promedio de reservas CANCELADAS (division por cero controlada)",
        lambda: gestor.promedio_costo_por_estado("CANCELADA")
    )

    # -------- RESUMEN FINAL --------

    print("\n" + "=" * 50)
    print("RESUMEN FINAL DE LA SIMULACION")
    print("=" * 50)
    print(f"Operaciones exitosas: {sim.exitosas}")
    print(f"Operaciones fallidas (controladas): {sim.fallidas}")
    print(gestor.resumen())

    print("\nDetalle de reservas (entidades del sistema):")
    for reserva in gestor.listar_reservas():
        print("-" * 30)
        print(datos_de(reserva))

    registrar_log(
        "EVENTO",
        f"===== FIN DE LA SIMULACION: {sim.exitosas} exitosas, "
        f"{sim.fallidas} fallidas ====="
    )

    print("\nEl programa finalizo sin interrupciones. "
          "Revise el archivo logs.txt.")


if __name__ == "__main__":
    main()
