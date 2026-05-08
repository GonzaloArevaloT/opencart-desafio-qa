"""Page Object de la pagina de inicio (Home) de OpenCart."""
from pages.base_page import BasePage


class HomePage(BasePage):
    """Acciones disponibles desde la home: busqueda y menu de cuenta."""

    # ---- Selectores propios de la home ----
    INPUT_BUSQUEDA = "input[name='search']"
    BOTON_BUSCAR = "#search button"
    LINK_MY_ACCOUNT = "a[title='My Account']"
    LINK_REGISTER = "a:has-text('Register')"

    def abrir(self) -> None:
        """Navega a la URL base del sitio."""
        self.navegar_a("/")

    def buscar_producto(self, termino: str) -> None:
        """Escribe el termino y dispara la busqueda."""
        self.escribir(self.INPUT_BUSQUEDA, termino)
        self.click(self.BOTON_BUSCAR)

    def ir_a_registro(self) -> None:
        """Abre el menu My Account y selecciona Register."""
        self.click(self.LINK_MY_ACCOUNT)
        self.click(self.LINK_REGISTER)
