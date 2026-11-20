
from integrante1_clientes import Cliente
from integrante2_servicio import (
    Servicio,
    ServicioInvalidoError,
    registrar_log
)

# --------------------------------------------------
# INTEGRANTE 4: EXCEPCIONES PERSONALIZADAS DE RESERVAS
# Se usan cuando una reserva no cumple las reglas
# del sistema 
# --------------------------------------------------

class ReservaInvalidaError(Exception):
    pass


class EstadoReservaError(ReservaInvalidaError):
    # Se lanza cuando la operacion no es permitida
    # para el estado actual de la reserva.
    pass


class ServicioNoDisponibleError(ReservaInvalidaError):
    # Se lanza cuando se intenta reservar o confirmar
    # un servicio que no esta disponible.
    pass


# --------------------------------------------------
# CLASE RESERVA
# Integra un cliente, un servicio, la duracion y el
# estado de la reserva. Permite confirmar, cancelar
# y procesar la reserva con manejo de excepciones.
# --------------------------------------------------

class Reserva:

    # Estados posibles de una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    # Contador para generar codigos de reserva unicos
    _contador = 0

    def __init__(self, cliente, servicio, duracion):

        try:
            # VALIDAR CLIENTE
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError(
                    "La reserva requiere un cliente valido."
                )

            # VALIDAR SERVICIO
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError(
                    "La reserva requiere un servicio valido."
                )

            # VALIDAR DISPONIBILIDAD DEL SERVICIO
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {servicio.nombre} no esta disponible."
                )

            # VALIDAR DURACION usando el metodo de cada servicio
            # (polimorfismo). Si falla, se encadena la excepcion
            # original con la excepcion propia de la reserva.
            try:
                servicio.validar_parametros(duracion)

            except (ValueError, ServicioInvalidoError) as error:
                raise ReservaInvalidaError(
                    "La duracion de la reserva no es valida."
                ) from error

        except ReservaInvalidaError as error:
            # Se registra el error y se relanza para que lo
            # maneje quien intento crear la reserva.
            registrar_log("ERROR", f"Reserva rechazada: {error}")
            raise

        # GENERAR CODIGO UNICO
        Reserva._contador += 1

        # ATRIBUTOS DE LA RESERVA
        self._codigo = f"R{Reserva._contador:03d}"
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = Reserva.PENDIENTE
        self._costo_total = None

        registrar_log(
            "EVENTO",
            f"Reserva {self._codigo} creada para el servicio "
            f"{servicio.nombre}."
        )

    # ----------------------------------------------
    # METODOS GET PARA CONSULTAR LOS ATRIBUTOS
    # ----------------------------------------------

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # ----------------------------------------------
    # METODO PARA CALCULAR EL COSTO (SOBRECARGA)
    # ----------------------------------------------

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **opciones):

        try:
            return self._servicio.calcular_costo(
                self._duracion,
                impuesto,
                descuento,
                **opciones
            )

        except (ValueError, TypeError, ServicioInvalidoError) as error:
            raise ReservaInvalidaError(
                "No se pudo calcular el costo de la reserva."
            ) from error

    # ----------------------------------------------
    # METODO PARA CONFIRMAR LA RESERVA
    # Solo se puede confirmar una reserva pendiente
    # y con el servicio disponible.
    # ----------------------------------------------

    def confirmar(self):

        try:
            if self._estado != Reserva.PENDIENTE:
                raise EstadoReservaError(
                    f"No se puede confirmar la reserva {self._codigo} "
                    f"porque esta {self._estado}."
                )

            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {self._servicio.nombre} "
                    f"ya no esta disponible."
                )

        except ReservaInvalidaError as error:
            registrar_log("ERROR", str(error))
            raise

        else:
            self._estado = Reserva.CONFIRMADA
            registrar_log(
                "EVENTO",
                f"Reserva {self._codigo} confirmada correctamente."
            )

    # ----------------------------------------------
    # METODO PARA CANCELAR LA RESERVA
    # No se puede cancelar una reserva ya cancelada
    # o ya procesada.
    # ----------------------------------------------

    def cancelar(self):

        try:
            if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):
                raise EstadoReservaError(
                    f"No se puede cancelar la reserva {self._codigo} "
                    f"porque esta {self._estado}."
                )

        except EstadoReservaError as error:
            registrar_log("ERROR", str(error))
            raise

        else:
            self._estado = Reserva.CANCELADA
            registrar_log(
                "EVENTO",
                f"Reserva {self._codigo} cancelada correctamente."
            )

    # ----------------------------------------------
    # METODO PARA PROCESAR LA RESERVA
    # Calcula el costo final y la deja como PROCESADA.
    # Solo se procesa una reserva confirmada.
    # ----------------------------------------------

    def procesar(self, impuesto=0.0, descuento=0.0, **opciones):

        try:
            if self._estado != Reserva.CONFIRMADA:
                raise EstadoReservaError(
                    f"No se puede procesar la reserva {self._codigo} "
                    f"porque esta {self._estado}."
                )

            costo = self.calcular_costo(impuesto, descuento, **opciones)

            if costo <= 0:
                raise ReservaInvalidaError(
                    "El costo calculado es inconsistente."
                )

        except ReservaInvalidaError as error:
            registrar_log("ERROR", str(error))
            raise

        else:
            self._costo_total = costo
            self._estado = Reserva.PROCESADA
            registrar_log(
                "EVENTO",
                f"Reserva {self._codigo} procesada. "
                f"Costo total: ${costo:,.0f}"
            )
            return costo

        finally:
            registrar_log(
                "EVENTO",
                f"Finalizo el intento de procesar la reserva "
                f"{self._codigo}. Estado actual: {self._estado}."
            )

    # ----------------------------------------------
    # METODO PARA MOSTRAR LA INFORMACION DE LA RESERVA
    # ----------------------------------------------

    def obtener_datos(self):

        costo = (
            f"${self._costo_total:,.0f}"
            if self._costo_total is not None
            else "Sin calcular"
        )

        return (
            f"Reserva: {self._codigo}\n"
            f"Cliente: {self._cliente.get_nombre()}\n"
            f"{self._servicio.describir()}\n"
            f"Duracion: {self._duracion}\n"
            f"Estado: {self._estado}\n"
            f"Costo total: {costo}"
        )


