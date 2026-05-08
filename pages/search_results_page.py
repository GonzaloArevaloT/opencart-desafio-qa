"""Page Object de la pagina de resultados de busqueda."""
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Resultados de busqueda y acceso al detalle de producto."""

    # ---- Selectores ----
    TITULO_BUSQUEDA = "#content h1"
    LISTA_PRODUCTOS = ".product-thumb"
    NOMBRE_PRODUCTO = ".product-thumb .caption h4 a"
    MENSAJE_SIN_RESULTADOS = "#content p:has-text('There is no product')"

    def cantidad_resultados(self) -> int:
        """Cantidad de productos encontrados en la busqueda."""
        return self.page.locator(self.LISTA_PRODUCTOS).count()

    def hay_resultados(self) -> bool:
        """Devuelve True si la busqueda devolvio al menos un producto."""
        return self.cantidad_resultados() > 0

    def abrir_primer_producto(self) -> None:
        """Hace click en el nombre del primer producto del listado."""
        self.page.locator(self.NOMBRE_PRODUCTO).first.click()
