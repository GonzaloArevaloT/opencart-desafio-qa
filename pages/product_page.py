"""Page Object del detalle de un producto."""
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Pagina de detalle del producto con accion Add to Cart."""

    # ---- Selectores ----
    NOMBRE_PRODUCTO = "#content h1"
    INPUT_CANTIDAD = "#input-quantity"
    BOTON_ADD_TO_CART = "#button-cart"
    ALERTA_EXITO = ".alert-success"
    LINK_VER_CARRITO = ".alert-success a:has-text('shopping cart')"
    # Contador de items del carrito en el header (texto "0 item(s) - $0.00").
    # Sirve como indicador estable de que el AJAX de "add to cart" termino,
    # ya que el .alert-success se auto-dismisses tras unos segundos.
    HEADER_CART_TOTAL = "#cart-total"

    def obtener_nombre(self) -> str:
        """Devuelve el nombre del producto mostrado en la pagina."""
        return self.obtener_texto(self.NOMBRE_PRODUCTO)

    def agregar_al_carrito(self, cantidad: int = 1) -> None:
        """Define la cantidad y agrega el producto al carrito.

        El sitio publico (opencart.abstracta.us) es flaky: a veces el click
        no dispara el POST de add-to-cart. Hacemos hasta 2 intentos esperando
        explicitamente la response AJAX antes de dar el paso por completo.
        """
        from playwright._impl._errors import TimeoutError as PWTimeoutError

        self.escribir(self.INPUT_CANTIDAD, str(cantidad))
        ultimo_error: Exception | None = None
        for _ in range(2):
            try:
                with self.page.expect_response(
                    lambda r: "checkout/cart/add" in r.url, timeout=10000
                ):
                    self.click(self.BOTON_ADD_TO_CART)
                return
            except PWTimeoutError as exc:
                ultimo_error = exc
        raise ultimo_error  # type: ignore[misc]

    def ir_al_carrito_desde_alerta(self) -> None:
        """Sigue el enlace 'shopping cart' del mensaje de confirmacion."""
        self.click(self.LINK_VER_CARRITO)
