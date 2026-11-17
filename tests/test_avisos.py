import pytest
from trabajo_final_pp5 import *

REGISTRO = datetime(2026, 11, 20, 10, 30)
FECHA_NOTA = datetime(2026, 11, 20, 11, 0)
DESCARTE = datetime(2026, 11, 20, 12, 0)

@pytest.fixture
def aviso_pendiente():
    return Aviso(Reportante("Ana"), "Ruta 5 km 32", Situacion.Inundacion, Gravedad.Media, "Agua sobre la calzada", REGISTRO)

@pytest.fixture
def aviso_descartado(aviso_pendiente):
    aviso_pendiente.descartar(DESCARTE, "Duplicado de otro aviso")
    return aviso_pendiente

@pytest.fixture
def aviso_aceptado(aviso_pendiente):
    aviso_pendiente.aceptar(object()) # No hay emergencias, es solo para avanzar el test
    return aviso_pendiente

@pytest.fixture
def nota():
    return Nota("Ana", FECHA_NOTA, "Se suma una familia aislada")

# Un aviso recién registrado está pendiente, no tiene notas y no tiene descarte

def test_aviso_nuevo_esta_pendiente_sin_notas(aviso_pendiente):
    assert isinstance(aviso_pendiente.estado, Pendiente)
    assert aviso_pendiente.notas == ()

def test_aviso_contiene_datos(aviso_pendiente):
    assert aviso_pendiente.reportante.nombre == "Ana"
    assert aviso_pendiente.ubicacion == "Ruta 5 km 32"
    assert aviso_pendiente.situacion == Situacion.Inundacion
    assert aviso_pendiente.gravedadEstimada == Gravedad.Media
    assert aviso_pendiente.descripcion == "Agua sobre la calzada"
    assert aviso_pendiente.fechaRegistro == REGISTRO

def test_situacion_fuera_del_catalogo():
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", "Incendio", Gravedad.Baja, "Fuego", REGISTRO)
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", None, Gravedad.Baja, "Fuego", REGISTRO)

def test_r1_gravedad_fuera_del_catalogo():
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", Situacion.Incendio, "Alta", "Fuego", REGISTRO)
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", Situacion.Incendio, 99999, "Fuego", REGISTRO)

def test_datos_de_registro_invalidos():
    with pytest.raises(DatoInvalidoError):
        Aviso("Ana", "Ruta 5", Situacion.Incendio, Gravedad.Baja, "Fuego", REGISTRO)
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "   ", Situacion.Incendio, Gravedad.Baja, "Fuego", REGISTRO)
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", Situacion.Incendio, Gravedad.Baja, "", REGISTRO)
    with pytest.raises(DatoInvalidoError):
        Aviso(Reportante("Ana"), "Ruta 5", Situacion.Incendio, Gravedad.Baja, "Fuego", "ayer")

#  Se agrega una nota a un aviso pendiente y la nota conserva autor, fecha y hora

def test_aviso_pendiente_acepta_nota(aviso_pendiente, nota):
    aviso_pendiente.nuevaNota(nota)

    assert aviso_pendiente.notas == (nota,)
    assert nota.autor == "Ana"
    assert nota.fechaCreacion == FECHA_NOTA
    assert nota.contenido == "Se suma una familia aislada"
    assert isinstance(aviso_pendiente.estado, Pendiente)

# Se agregan dos notas y se conservan las dos, en el orden en que llegaron. 

def test_notas_conservadas_en_orden_de_llegada(aviso_pendiente):
    primera = Nota("Ana", FECHA_NOTA, "Primera")
    segunda = Nota("Ana", FECHA_NOTA, "Segunda")
    aviso_pendiente.nuevaNota(primera)
    aviso_pendiente.nuevaNota(segunda)

    assert aviso_pendiente.notas == (primera, segunda)

@pytest.mark.parametrize("autor, contenido", [
    ("", "texto"),
    ("   ", "texto"),
    (None, "texto"),
    ("Ana", ""),
    ("Ana", "   "),
    ("Ana", None),
])
def test_nota_invalida(autor, contenido):
    with pytest.raises(DatoInvalidoError):
        Nota(autor, FECHA_NOTA, contenido)

def test_agregar_nota_invalida(aviso_pendiente):
    with pytest.raises(DatoInvalidoError):
        aviso_pendiente.nuevaNota("random random")
    assert aviso_pendiente.notas == ()

#  Después de agregar una nota, la ubicación, el tipo, la gravedad estimada y la descripción siguen iguales

def test_agregar_nota_no_cambia_datos(aviso_pendiente, nota):
    reportante = aviso_pendiente.reportante
    aviso_pendiente.nuevaNota(nota)

    assert aviso_pendiente.reportante is reportante
    assert aviso_pendiente.ubicacion == "Ruta 5 km 32"
    assert aviso_pendiente.situacion == Situacion.Inundacion
    assert aviso_pendiente.gravedadEstimada == Gravedad.Media
    assert aviso_pendiente.descripcion == "Agua sobre la calzada"
    assert aviso_pendiente.fechaRegistro == REGISTRO

#  Se descarta un aviso pendiente con justificación: queda descartado y conserva la justificación y la fecha.

def test_descarte_conserva_justificacion_y_fecha(aviso_pendiente):
    aviso_pendiente.descartar(DESCARTE, "Duplicado de otro aviso")

    assert isinstance(aviso_pendiente.estado, Descartado)
    assert aviso_pendiente.estado.justificacion == "Duplicado de otro aviso"
    assert aviso_pendiente.estado.fechaDescarte == DESCARTE

#  Se intenta descartar con una justificación vacía o con solo espacios. La operación se rechaza y el aviso sigue pendiente

@pytest.mark.parametrize("justificacion", ["", "   ", "\t\n", None])
def test_rechazo_de_justificacion_vacia(aviso_pendiente, justificacion):
    estado_previo = aviso_pendiente.estado

    with pytest.raises(DatoInvalidoError):
        aviso_pendiente.descartar(DESCARTE, justificacion)

    assert aviso_pendiente.estado is estado_previo
    assert isinstance(aviso_pendiente.estado, Pendiente)

def test_rechazo_de_fecha_de_descarte_invalida(aviso_pendiente):
    estado_previo = aviso_pendiente.estado

    with pytest.raises(DatoInvalidoError):
        aviso_pendiente.descartar("hoy", "Duplicado")

    assert aviso_pendiente.estado is estado_previo

# Se intenta agregar una nota a un aviso descartado. La operación se rechaza y las notas no cambian.

def test_rechazo_de_nota_en_aviso_descartado(aviso_descartado, nota):
    with pytest.raises(AvisoNoPendienteError):
        aviso_descartado.nuevaNota(nota)

    assert aviso_descartado.notas == ()

#  Se intenta descartar por segunda vez. La operación se rechaza y se conserva la justificación original

def test_rechazo_de_segundo_descarte(aviso_descartado):
    estado_previo = aviso_descartado.estado

    with pytest.raises(AvisoNoPendienteError):
        aviso_descartado.descartar(datetime(2026, 11, 21), "Otra justificación")

    assert aviso_descartado.estado is estado_previo
    assert aviso_descartado.estado.justificacion == "Duplicado de otro aviso"
    assert aviso_descartado.estado.fechaDescarte == DESCARTE

def test_rechazo_de_aceptacion_en_aviso_descartado(aviso_descartado):
    estado_previo = aviso_descartado.estado

    with pytest.raises(AvisoNoPendienteError):
        aviso_descartado.aceptar(object())

    assert aviso_descartado.estado is estado_previo
    assert isinstance(aviso_descartado.estado, Descartado)

def test_aviso_pendiente_pasa_a_aceptado(aviso_pendiente):
    aviso_pendiente.aceptar(object())

    assert isinstance(aviso_pendiente.estado, Aceptado)

#  Se intenta agregar una nota a un aviso aceptado. La operación se rechaza.

def test_rechazo_de_nota_en_aviso_aceptado(aviso_aceptado, nota):
    with pytest.raises(AvisoNoPendienteError):
        aviso_aceptado.nuevaNota(nota)

    assert aviso_aceptado.notas == ()

def test_rechazo_de_descarte_y_segunda_aceptacion_en_aviso_aceptado(aviso_aceptado):
    estado_previo = aviso_aceptado.estado

    with pytest.raises(AvisoNoPendienteError):
        aviso_aceptado.descartar(DESCARTE, "Ya no corresponde")
    with pytest.raises(AvisoNoPendienteError):
        aviso_aceptado.aceptar(object())

    assert aviso_aceptado.estado is estado_previo
    assert isinstance(aviso_aceptado.estado, Aceptado)