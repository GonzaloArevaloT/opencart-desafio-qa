"""Hooks de ciclo de vida de Behave.

Maneja el inicio y cierre del navegador Playwright, la inyeccion de la
Page en el contexto de Behave, y la captura de screenshots cuando un
escenario falla.
"""
import os
import re
from datetime import datetime

from playwright.sync_api import sync_playwright

from utils.config import Config
from utils.logger import obtener_logger


_logger = obtener_logger()


def before_all(context):
    """Inicializa Playwright una sola vez para toda la suite."""
    Config.validar_browser()
    _logger.info("Iniciando Playwright | navegador=%s | headless=%s",
                 Config.BROWSER, Config.HEADLESS)
    # Se guarda la instancia de Playwright en el contexto global
    context.playwright = sync_playwright().start()

    # Asegura que la carpeta de screenshots exista
    os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)


def before_scenario(context, scenario):
    """Lanza un navegador y una pagina nueva por cada escenario.

    El aislamiento por escenario garantiza independencia y evita
    contaminacion de estado (cookies, sesion, carrito) entre tests.
    """
    _logger.info("Inicio escenario: %s", scenario.name)

    # Selecciona el navegador segun la variable de entorno BROWSER
    tipo_navegador = getattr(context.playwright, Config.BROWSER)
    context.browser = tipo_navegador.launch(headless=Config.HEADLESS)

    # Crea un contexto aislado por escenario con viewport configurado
    context.browser_context = context.browser.new_context(
        viewport={
            "width": Config.VIEWPORT_WIDTH,
            "height": Config.VIEWPORT_HEIGHT,
        }
    )
    context.page = context.browser_context.new_page()


def after_scenario(context, scenario):
    """Cierra el navegador y captura screenshot si el escenario fallo."""
    if scenario.status == "failed":
        _capturar_screenshot(context, scenario)

    # Cierre ordenado: pagina -> contexto -> navegador
    try:
        context.page.close()
        context.browser_context.close()
        context.browser.close()
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Error al cerrar el navegador: %s", exc)

    _logger.info("Fin escenario: %s | estado=%s", scenario.name, scenario.status)


def after_all(context):
    """Detiene Playwright al finalizar toda la suite."""
    try:
        context.playwright.stop()
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Error al detener Playwright: %s", exc)


def _capturar_screenshot(context, scenario) -> None:
    """Genera un PNG con el estado actual de la pagina al fallar."""
    # Sanitiza el nombre del escenario para usarlo como nombre de archivo
    nombre_seguro = re.sub(r"[^A-Za-z0-9_-]+", "_", scenario.name)[:80]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(
        Config.SCREENSHOTS_DIR, f"{nombre_seguro}_{timestamp}.png"
    )
    try:
        context.page.screenshot(path=ruta, full_page=True)
        _logger.error("Screenshot guardado en: %s", ruta)
    except Exception as exc:  # noqa: BLE001
        _logger.warning("No se pudo capturar screenshot: %s", exc)
