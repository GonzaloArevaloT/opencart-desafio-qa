"""Modulo de configuracion centralizada del proyecto.

Lee variables de entorno del sistema operativo (sin dotenv) y expone
constantes utilizadas por el resto de los modulos.
"""
import os


class Config:
    """Contenedor de configuracion global del framework de pruebas."""

    # URL base del sitio bajo prueba
    BASE_URL: str = os.getenv("BASE_URL", "https://opencart.abstracta.us/")

    # Navegador a utilizar: chromium (default), firefox o webkit
    BROWSER: str = os.getenv("BROWSER", "chromium").lower()

    # Modo headless del navegador (true por defecto en CI, configurable)
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")

    # Timeout por defecto en milisegundos para acciones de Playwright
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "15000"))

    # Resolucion del viewport
    VIEWPORT_WIDTH: int = 1366
    VIEWPORT_HEIGHT: int = 768

    # Carpeta donde se guardan las capturas de pantalla en caso de fallos
    SCREENSHOTS_DIR: str = os.path.join("reports", "screenshots")

    @classmethod
    def validar_browser(cls) -> str:
        """Valida que el navegador solicitado sea uno de los soportados.

        Devuelve el nombre normalizado o lanza un error si no es valido.
        """
        navegadores_validos = {"chromium", "firefox", "webkit"}
        if cls.BROWSER not in navegadores_validos:
            raise ValueError(
                f"BROWSER='{cls.BROWSER}' no es valido. "
                f"Opciones permitidas: {', '.join(sorted(navegadores_validos))}"
            )
        return cls.BROWSER
