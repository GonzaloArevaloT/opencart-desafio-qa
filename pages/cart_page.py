"""Page Object del carrito de compras."""
from pages.base_page import BasePage


class CartPage(BasePage):
    """Pagina del carrito: lista de productos y acceso al checkout."""

    # ---- Selectores ----
    TITULO_CARRITO = "#content h1"
    FILAS_PRODUCTOS = "#content table.table tbody tr"
    NOMBRE_PRODUCTO_EN_FILA = "td.text-left a"
    BOTON_CHECKOUT = "#content a.btn-primary:has-text('Checkout')"

    def cantidad_items(self) -> int:
        """Cantidad de filas de productos presentes en el carrito."""
        return self.page.locator(self.FILAS_PRODUCTOS).count()

    def contiene_producto(self, nombre: str) -> bool:
        """Indica si el carrito contiene un producto con el nombre dado."""
        textos = self.page.locator(self.NOMBRE_PRODUCTO_EN_FILA).all_inner_texts()
        return any(nombre.lower() in t.lower() for t in textos)

    def ir_a_checkout(self) -> None:
        """Avanza desde el carrito hacia la pagina de checkout."""
        self.click(self.BOTON_CHECKOUT)
