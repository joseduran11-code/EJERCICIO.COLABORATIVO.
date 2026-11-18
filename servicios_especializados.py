from servicio import servicio
from excepciones import ParametroServicioError

class ReservaSala(servicio):
  def validar_parametros(self,duracion):
    if duracion <= 0:
      raise ParametroServicioError(
        "La duracion de la reserva debe ser mayor que cero."
      )

def calcular_costo(
  self, duracion, descuento=0.0, impuesto=0.0
):
  self.validar_parametros(duracion)
  
  if not 0 <= descuento <=1 or impuesto < 0:
    raise ParametroServicioError(
      "El descuento o impesto no es valido."
    )
  costo_base = self.tarifa_base * duracion
  costo_con_descuento = costo_base *(1 - descuento)
  costo_final = costo_con_descuento * (1 + impuesto)

  return costo_final

def describir_servicio(self):
  return(
    f"Reserva de sala: {self.nombre}."
    f"Tarifa por hora: ${self.tarifa_:,.0f}"
  )

class AlquilerEquipo(servicio):
  def validar_parametros(self, duracion):
    if duracion <= 0:
      raise ParametroServicioError(
        "los dias de alquiler deben ser mayores que cero."
      )

def calcular_costo(
  self,
  duracion,
  descuento=0.0,
  impuesto=0.0,
  *,
  cantidad=1
):
  self.validar_parametros(duracion)

  if cantidad <= 0:
    raise ParametroServicioError(
      "La cantidad de equipos debe ser mayor que cero."
    )
  if not 0 <= descuento <= 1 or impuesto < 0:
    raise ParametroServicioError(
      "El Descuento o Impuesto no es Valido."
    )
  costo_base = self.tarifa_base * duracion * cantidad
  costo_con_descuento = costo_base * (1 - descuento)
  costo_final = costo_con_descuento * (1 + impuesto)

  return costo_final

def describir_servicio(self):
  return(
  f"Alquiler de Equipos: {self.nombre}. "
  f"Tarifa diaria: ${self.tarifa_base:,.0f}"
)

class AsesoriaEspecializada(servicio):

  def validar_parametros(self, duracion):
    if duracion <= 0:
      raise ParametroServicioError(
        "Las horas de asesoria deben ser mayores que cero."
      )

def calcular_costo(
  self, duracion, descuento=0.0, impuesto=0.0
):
  self.validar_parametros(duracion)

  if not 0 <= descuento <= 1 or impuesto < 0:
    raise ParametroServicioError(
      "EL descuento no es valido."
    )
  costo_base = self.tarifa_base * duracion
  costo_con_descuento = costo_base * (1 - descuento)
  costo_final = costo_con_descuento * (1 + impuesto)

  return costo_final


def describir_servicio(self):
  return (
  f"Asesoria especializada: {self.nombre}. "
  f"Tarifa por hora: ${self.tarifa_base:,.0f}"
)