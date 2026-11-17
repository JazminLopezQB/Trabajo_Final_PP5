from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# --- Excepciones de dominio ---
 
class AvisoError(Exception):
    """Error base del dominio de avisos."""
 
class DatoInvalidoError(AvisoError):
    """Un dato no cumple las condiciones para crear u operar un objeto."""
 
class AvisoNoPendienteError(AvisoError):
    """La operación solo se admite sobre un aviso pendiente."""
 
# --- Funciones de Verificación ---
 
def verificarTexto(texto):
    if (not isinstance(texto, str)) or (not texto.strip()):
        raise DatoInvalidoError("No pueden haber textos invalidos o vacios.")
    return texto
 
def verificarFecha(fecha):
    if not isinstance(fecha, datetime):
        raise DatoInvalidoError("Debe asignarse una fecha valida")
    return fecha

# --- Participantes ---
"""
NOTA: Los participantes se integrarán por completo más adelante, en este
avance solo se incluyeron para ejemplificar su relación con los avisos.
"""
class Reportante():
    def __init__(self, nombre):
        self._nombre = verificarTexto(nombre)
 
    @property
    def nombre(self):
        return self._nombre

    def generarAviso(self):
        pass
    def agregarNota(self, nota, aviso):
        pass
    def consultarEmergencia(self, emergencia):
        pass

class Operador():
    def __init__(self):
        pass
    def aceptarAviso(self, emergencia, aviso):
        pass
    def descartarAviso(self, aviso, fecha, justificacion):
        pass
    def atenderEmergencia(self, emergencia):
        pass

# --- Catalogos ---

class Situacion(Enum):
    Inundacion = 1
    Incendio = 2
    Accidente = 3
 
class Gravedad(Enum):
    Baja = 1
    Media = 2
    Alta = 3

# --- Avisos ---

class Aviso():

    def __init__(self, reportante, ubicacion, situacion, gravedad, descripcion, fecha):
        
        if not isinstance(reportante, Reportante):
            raise DatoInvalidoError("El aviso necesita un reportante valido")
        if not isinstance(situacion, Situacion):
            raise DatoInvalidoError("La situacion debe estar dentro del catalogo permitido")
        if not isinstance(gravedad, Gravedad):
            raise DatoInvalidoError("La gravedad debe estar dentro del catalogo permitido")
        
        self._ubicacion = verificarTexto(ubicacion)
        self._descripcion = verificarTexto(descripcion)
        self._fechaRegistro = verificarFecha(fecha)
        self._reportante = reportante
        self._situacion = situacion
        self._gravedadEstimada = gravedad
        self._notas = []
        self._estado = Pendiente()
    
    @property
    def reportante(self):
        return self._reportante

    @property
    def ubicacion(self):
        return self._ubicacion

    
    @property
    def situacion(self):
        return self._situacion

    @property
    def gravedadEstimada(self):
        return self._gravedadEstimada

    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def fechaRegistro(self):
        return self._fechaRegistro

    @property
    def notas(self):
        return tuple(self._notas)

    @property
    def estado(self):
        return self._estado
        
    def descartar(self, fecha, justificacion):
        self._estado = self.estado.descarte(fecha, justificacion)

    def aceptar(self, emergencia):
        self._estado = self.estado.aceptacion(emergencia)

    def nuevaNota(self, nota):
        self.estado.anotar() # Verificación de si el estado permite o no agregar notas
        if not (isinstance(nota, Nota)):
            raise DatoInvalidoError("Solo se pueden agregar notas a los avisos")
        self._notas.append(nota)

# --- Componentes de Avisos ---

class Nota():

    def __init__(self, autor, fecha, contenido):
        self._autor = verificarTexto(autor)
        self._fechaCreacion = verificarFecha(fecha)
        self._contenido = verificarTexto(contenido)

    @property
    def autor(self):
        return self._autor

    @property
    def fechaCreacion(self):
        return self._fechaCreacion

    @property
    def contenido(self):
        return self._contenido

class Estado(ABC):
    
    def anotar(self):
        raise AvisoNoPendienteError("Solo se pueden agregar notas a los avisos pendientes")
    
    @abstractmethod
    def aceptacion(self, emergencia):
        pass

    @abstractmethod
    def descarte(self, fecha, justificacion):
        pass
 
class Pendiente(Estado):
    def anotar(self): pass

    def aceptacion(self, emergencia):
        return Aceptado(emergencia)

    def descarte(self, fecha, justificacion):
        return Descartado(fecha, justificacion)

class Aceptado(Estado):

    def __init__(self, emergencia):
        pass

    """ # Las emergencias se implementarán a futuro
        self.emergencia = emergencia

    @property
    def emergencia(self):
        return self._emergencia

    @emergencia.setter
    def emergencia(self, emergencia):
        if not (isinstance(emergencia, Emergencia)):
            raise TypeError("Para aceptar un aviso se necesita asignar una emergencia valida")
        self._emergencia = emergencia
    """

    def aceptacion(self, emergencia):
        raise AvisoNoPendienteError("No se puede aceptar otra vez un aviso aceptado")

    def descarte(self, fecha, justificacion):
        raise AvisoNoPendienteError("No se puede descartar un aviso aceptado")

class Descartado(Estado):

    def __init__(self, fecha, justificacion):
        self._fechaDescarte = verificarFecha(fecha)
        self._justificacion = verificarTexto(justificacion)

    @property
    def fechaDescarte(self):
        return self._fechaDescarte

    @property
    def justificacion(self):
        return self._justificacion

    def aceptacion(self, emergencia):
        raise AvisoNoPendienteError("No se puede aceptar un aviso descartado")

    def descarte(self, fecha, justificacion):
        raise AvisoNoPendienteError("No se puede descartar otra vez un aviso descartado")

