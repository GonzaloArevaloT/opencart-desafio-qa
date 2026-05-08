"""Steps relacionados al flujo de checkout como invitado."""
from behave import when, then

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import Config
from utils.data_factory import DataFactory


@when("el usuario procede al checkout")
def step_ir_a_checkout(context):
    """Avanza desde el carrito al checkout."""
    # Si no se llego al carrito en pasos previos, se accede directamente
    if not hasattr(context, "cart_page"):
        context.page.goto(
            Config.BASE_URL.rstrip("/") + "/index.php?route=checkout/cart"
        )
        context.cart_page = CartPage(context.page)
    context.cart_page.ir_a_checkout()
    context.checkout_page = CheckoutPage(context.page)


@when("el usuario selecciona checkout como invitado")
def step_seleccionar_guest(context):
    """Selecciona la modalidad Guest Checkout."""
    context.checkout_page.seleccionar_guest_checkout()


@when("el usuario completa los datos de facturación")
def step_completar_billing(context):
    """Genera y carga datos dinamicos en los campos de facturacion."""
    context.direccion = DataFactory.generar_direccion_checkout()
    context.checkout_page.completar_billing(context.direccion)


@when("el usuario confirma el método de envío")
def step_confirmar_envio(context):
    """Confirma el metodo de envio predeterminado."""
    context.checkout_page.confirmar_metodo_envio()


@when("el usuario confirma el método de pago")
def step_confirmar_pago(context):
    """Acepta los terminos y confirma el metodo de pago."""
    context.checkout_page.confirmar_metodo_pago()


@when("el usuario finaliza la orden")
def step_confirmar_orden(context):
    """Realiza la confirmacion final de la orden."""
    context.checkout_page.confirmar_orden()


@then("la orden se crea exitosamente")
def step_validar_orden_exitosa(context):
    """Valida que la orden se haya creado correctamente."""
    assert context.checkout_page.orden_fue_exitosa(), (
        "No se confirmo la creacion de la orden."
    )
