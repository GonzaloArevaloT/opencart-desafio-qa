"""Page Object de la pagina de confirmacion de creacion de cuenta."""
from pages.base_page import BasePage


class AccountSuccessPage(BasePage):
    """Pagina mostrada despues de un registro exitoso."""

    # ---- Selectores ----
    # En esta version de OpenCart el h1 dice "Account" y el mensaje de
    # confirmacion vive en un parrafo del cuerpo.
    TITULO_EXITO = "#content h1"
    MENSAJE_EXITO = "#content p:has-text('successfully created')"
    MENSAJE_EXITO_TEXTO = "successfully created"

    def obtener_titulo(self) -> str:
        """Devuelve el titulo principal de la pagina."""
        return self.obtener_texto(self.TITULO_EXITO)

    def fue_exitoso(self) -> bool:
        """Indica si la creacion de cuenta termino correctamente."""
        try:
            self.esperar_visible(self.MENSAJE_EXITO)
            return True
        except Exception:
            return False
