"""Page Object del flujo de checkout (compra como invitado)."""
from pages.base_page import BasePage
from utils.data_factory import DireccionCheckout


class CheckoutPage(BasePage):
    """Encapsula los pasos del checkout en una sola pagina (one-page)."""

    # ---- Paso 1: opcion de cuenta ----
    RADIO_GUEST = "input[name='account'][value='guest']"
    BOTON_CONTINUE_PASO1 = "#button-account"

    # ---- Paso 2: datos de facturacion (Billing Details) ----
    INPUT_FIRSTNAME = "#input-payment-firstname"
    INPUT_LASTNAME = "#input-payment-lastname"
    INPUT_EMAIL = "#input-payment-email"
    INPUT_TELEPHONE = "#input-payment-telephone"
    INPUT_ADDRESS_1 = "#input-payment-address-1"
    INPUT_CITY = "#input-payment-city"
    INPUT_POSTCODE = "#input-payment-postcode"
    SELECT_COUNTRY = "#input-payment-country"
    SELECT_REGION = "#input-payment-zone"
    BOTON_CONTINUE_PASO2 = "#button-guest"

    # ---- Paso 3: metodo de envio ----
    TEXTAREA_COMENTARIO_ENVIO = "textarea[name='comment']"
    BOTON_CONTINUE_PASO3 = "#button-shipping-method"

    # ---- Paso 4: metodo de pago ----
    CHECKBOX_TERMS = "input[name='agree']"
    BOTON_CONTINUE_PASO4 = "#button-payment-method"

    # ---- Paso 5: confirmar pedido ----
    BOTON_CONFIRMAR_ORDEN = "#button-confirm"

    # ---- Selectores de la pagina de exito ----
    TITULO_ORDEN_EXITOSA = "#content h1"
    TEXTO_ORDEN_EXITOSA = "Your order has been placed!"

    def seleccionar_guest_checkout(self) -> None:
        """Marca la opcion 'Guest Checkout' y avanza al paso siguiente."""
        self.page.locator(self.RADIO_GUEST).check()
        self.click(self.BOTON_CONTINUE_PASO1)
        # El paso 2 (billing) se expande via AJAX: esperamos al primer input.
        self.esperar_visible(self.INPUT_FIRSTNAME)

    def completar_billing(self, direccion: DireccionCheckout) -> None:
        """Completa los datos de facturacion del comprador invitado."""
        self.escribir(self.INPUT_FIRSTNAME, direccion.first_name)
        self.escribir(self.INPUT_LASTNAME, direccion.last_name)
        self.escribir(self.INPUT_EMAIL, direccion.email)
        self.escribir(self.INPUT_TELEPHONE, direccion.telephone)
        self.escribir(self.INPUT_ADDRESS_1, direccion.address_1)
        self.escribir(self.INPUT_CITY, direccion.city)
        self.escribir(self.INPUT_POSTCODE, direccion.post_code)
        self.seleccionar_opcion(self.SELECT_COUNTRY, direccion.country)
        # La region se carga via AJAX al elegir pais; esperamos a que la
        # opcion deseada exista en el <select> antes de seleccionarla.
        from playwright.sync_api import expect

        from utils.config import Config

        expect(
            self.page.locator(f"{self.SELECT_REGION} option", has_text=direccion.region)
        ).to_have_count(1, timeout=Config.DEFAULT_TIMEOUT)
        self.seleccionar_opcion(self.SELECT_REGION, direccion.region)
        self.click(self.BOTON_CONTINUE_PASO2)

    def confirmar_metodo_envio(self) -> None:
        """Confirma el metodo de envio (acepta el predeterminado)."""
        self.click(self.BOTON_CONTINUE_PASO3)

    def confirmar_metodo_pago(self) -> None:
        """Acepta los terminos y confirma el metodo de pago."""
        self.page.locator(self.CHECKBOX_TERMS).check()
        self.click(self.BOTON_CONTINUE_PASO4)

    def confirmar_orden(self) -> None:
        """Realiza la confirmacion final de la orden."""
        self.click(self.BOTON_CONFIRMAR_ORDEN)
        # El click dispara un POST AJAX y luego redirige a la pagina de exito.
        self.esperar_url_contiene("route=checkout/success")

    def orden_fue_exitosa(self) -> bool:
        """Verifica que la orden se haya creado correctamente."""
        titulo = self.obtener_texto(self.TITULO_ORDEN_EXITOSA)
        return self.TEXTO_ORDEN_EXITOSA.lower() in titulo.lower()
