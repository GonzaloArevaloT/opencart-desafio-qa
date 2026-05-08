"""Pagina base con utilidades compartidas por todos los Page Objects.

Encapsula acciones comunes (navegar, click, escribir, esperar) sobre
la instancia de Page de Playwright, abstrayendo a los page objects
hijos del API directo del framework.
"""
from playwright.sync_api import Page, expect

from utils.config import Config


class BasePage:
    """Clase base de la que heredan todos los page objects."""

    def __init__(self, page: Page) -> None:
        # Instancia de Page de Playwright inyectada desde environment
        self.page = page
        # Aplica el timeout por defecto definido en la configuracion
        self.page.set_default_timeout(Config.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Navegacion
    # ------------------------------------------------------------------
    def navegar_a(self, ruta: str = "") -> None:
        """Navega a una ruta relativa a la URL base del sitio."""
        url = Config.BASE_URL.rstrip("/") + "/" + ruta.lstrip("/")
        self.page.goto(url)

    # ------------------------------------------------------------------
    # Acciones basicas
    # ------------------------------------------------------------------
    def click(self, selector: str) -> None:
        """Hace click en el elemento indicado por el selector."""
        self.page.locator(selector).click()

    def escribir(self, selector: str, texto: str) -> None:
        """Escribe un texto en el campo indicado, limpiandolo previamente."""
        elemento = self.page.locator(selector)
        elemento.fill(texto)

    def seleccionar_opcion(self, selector: str, etiqueta: str) -> None:
        """Selecciona una opcion de un <select> por su etiqueta visible."""
        self.page.locator(selector).select_option(label=etiqueta)

    def obtener_texto(self, selector: str) -> str:
        """Devuelve el texto visible del primer elemento que matchee."""
        return self.page.locator(selector).first.inner_text()

    # ------------------------------------------------------------------
    # Esperas y aserciones
    # ------------------------------------------------------------------
    def esperar_visible(self, selector: str) -> None:
        """Espera a que el elemento sea visible (auto-wait de Playwright)."""
        expect(self.page.locator(selector).first).to_be_visible(
            timeout=Config.DEFAULT_TIMEOUT
        )

    def esperar_url_contiene(self, fragmento: str) -> None:
        """Espera a que la URL actual contenga el fragmento dado."""
        expect(self.page).to_have_url(
            self._a_regex_url(fragmento), timeout=Config.DEFAULT_TIMEOUT
        )

    @staticmethod
    def _a_regex_url(fragmento: str):
        """Convierte un fragmento simple en una expresion regular permisiva."""
        import re

        return re.compile(re.escape(fragmento))
