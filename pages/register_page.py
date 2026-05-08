"""Page Object del formulario de registro de cuenta."""
from pages.base_page import BasePage
from utils.data_factory import UsuarioRegistro


class RegisterPage(BasePage):
    """Encapsula el formulario de registro y sus interacciones."""

    # ---- Selectores del formulario de registro ----
    INPUT_FIRSTNAME = "#input-firstname"
    INPUT_LASTNAME = "#input-lastname"
    INPUT_EMAIL = "#input-email"
    INPUT_TELEPHONE = "#input-telephone"
    INPUT_PASSWORD = "#input-password"
    INPUT_CONFIRM = "#input-confirm"
    CHECKBOX_PRIVACY = "input[name='agree']"
    BOTON_CONTINUE = "input[value='Continue']"
    TITULO_PAGINA = "#content h1"

    def esta_visible(self) -> None:
        """Valida que la pagina de registro este cargada."""
        self.esperar_visible(self.INPUT_FIRSTNAME)

    def completar_formulario(self, usuario: UsuarioRegistro) -> None:
        """Rellena todos los campos requeridos del formulario."""
        self.escribir(self.INPUT_FIRSTNAME, usuario.first_name)
        self.escribir(self.INPUT_LASTNAME, usuario.last_name)
        self.escribir(self.INPUT_EMAIL, usuario.email)
        self.escribir(self.INPUT_TELEPHONE, usuario.telephone)
        self.escribir(self.INPUT_PASSWORD, usuario.password)
        self.escribir(self.INPUT_CONFIRM, usuario.password)

    def aceptar_politica_privacidad(self) -> None:
        """Marca el checkbox de aceptacion de la politica de privacidad."""
        self.page.locator(self.CHECKBOX_PRIVACY).check()

    def enviar(self) -> None:
        """Envia el formulario haciendo click en Continue."""
        self.click(self.BOTON_CONTINUE)
        # Espera a que la URL cambie a la pagina de exito antes de seguir
        self.esperar_url_contiene("route=account/success")
