
from Fase4 import Servicio


class ReservaSala(Servicio):

    def validar_parametros(self, duracion):

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ValueError(
                "La duracion de la reserva debe ser mayor que cero."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):

        self.validar_parametros(duracion)

        if not 0 <= descuento <= 1 or impuesto < 0:
            raise ValueError("Descuento o impuesto no valido.")

        costo_base = self.precio * duracion
        return costo_base * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Reserva de sala: {self.nombre}. "
            f"Tarifa por hora: ${self.precio:,.0f}"
        )


class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion):

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ValueError(
                "Los dias de alquiler deben ser mayores que cero."
            )

    def calcular_costo(
        self, duracion, impuesto=0.0, descuento=0.0, *, cantidad=1
    ):

        self.validar_parametros(duracion)

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ValueError("Cantidad de equipos no valida.")

        if not 0 <= descuento <= 1 or impuesto < 0:
            raise ValueError("Descuento o impuesto no valido.")

        costo_base = self.precio * duracion * cantidad
        return costo_base * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Alquiler de equipos: {self.nombre}. "
            f"Tarifa diaria: ${self.precio:,.0f}"
        )


class AsesoriaEspecializada(Servicio):

    def validar_parametros(self, duracion):

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ValueError(
                "Las horas de asesoria deben ser mayores que cero."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):

        self.validar_parametros(duracion)

        if not 0 <= descuento <= 1 or impuesto < 0:
            raise ValueError("Descuento o impuesto no valido.")

        costo_base = self.precio * duracion
        return costo_base * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Asesoria especializada: {self.nombre}. "
            f"Tarifa por hora: ${self.precio:,.0f}"
        )
