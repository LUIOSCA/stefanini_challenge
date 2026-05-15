import logging
import sys

def setup_logging():
    # Obtenemos el logger principal de la aplicación
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Creamos un formato profesional: Fecha/Hora - Módulo - Nivel - Mensaje
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configuramos para que imprima en la consola (crucial para Docker y Google Cloud)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Evitamos que se dupliquen los logs si se llama varias veces
    if not logger.handlers:
        logger.addHandler(stream_handler)

    return logger