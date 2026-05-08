"""Configuracion de logging estructurado para el framework.

Provee un logger con formato consistente para toda la suite de pruebas.
"""
import logging
import sys


def obtener_logger(nombre: str = "opencart_qa") -> logging.Logger:
    """Devuelve un logger configurado con formato estandar.

    Si el logger ya tiene handlers, no agrega duplicados.
    """
    logger = logging.getLogger(nombre)

    if logger.handlers:
        # Evita registrar handlers duplicados al ser invocado multiples veces
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formato = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formato)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
