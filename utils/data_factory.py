"""Fabrica de datos dinamicos para los escenarios de prueba.

Utiliza Faker para generar datos unicos por ejecucion (emails,
nombres, direcciones), garantizando idempotencia entre corridas.
"""
import time
from dataclasses import dataclass

from faker import Faker


# Instancia unica de Faker en locale en_US para datos consistentes
_fake = Faker("en_US")


@dataclass
class UsuarioRegistro:
    """Estructura con los datos necesarios para registrar un usuario."""

    first_name: str
    last_name: str
    email: str
    telephone: str
    password: str


@dataclass
class DireccionCheckout:
    """Estructura con los datos de direccion para el checkout como invitado."""

    first_name: str
    last_name: str
    email: str
    telephone: str
    address_1: str
    city: str
    post_code: str
    country: str
    region: str


class DataFactory:
    """Provee datos dinamicos para los distintos escenarios de prueba."""

    @staticmethod
    def generar_usuario() -> UsuarioRegistro:
        """Genera un usuario nuevo con email unico basado en timestamp."""
        # Sufijo en milisegundos para evitar colisiones entre corridas
        sufijo = str(int(time.time() * 1000))
        return UsuarioRegistro(
            first_name=_fake.first_name(),
            last_name=_fake.last_name(),
            email=f"qa.tester.{sufijo}@example.com",
            telephone=_fake.numerify("9########"),
            password="Test1234!",
        )

    @staticmethod
    def generar_direccion_checkout() -> DireccionCheckout:
        """Genera datos completos de direccion para checkout como invitado."""
        sufijo = str(int(time.time() * 1000))
        return DireccionCheckout(
            first_name=_fake.first_name(),
            last_name=_fake.last_name(),
            email=f"qa.guest.{sufijo}@example.com",
            telephone=_fake.numerify("9########"),
            address_1=_fake.street_address(),
            city=_fake.city(),
            post_code=_fake.numerify("######"),
            # Pais y region fijos para garantizar disponibilidad en el dropdown
            country="United States",
            region="California",
        )
