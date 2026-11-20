from abc import ABC, abstractmethod

# --------------------------------------------------
# CLASE ABSTRACTA: ENTIDAD
# Representa cualquier entidad general del sistema
# de Software FJ (clientes, servicios y reservas).
#
# Todas las entidades deben saber describirse a si
# mismas mediante obtener_datos(), lo que permite
# tratarlas de forma polimorfica.
# --------------------------------------------------

class Entidad(ABC):

    @abstractmethod
    def obtener_datos(self):
        # Cada entidad retorna su informacion como texto.
        pass

    def __str__(self):
        # Permite usar print(entidad) en cualquier entidad.
        return self.obtener_datos()
