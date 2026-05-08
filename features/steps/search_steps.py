"""Steps relacionados a busqueda de productos y agregado al carrito."""
from behave import when, then

from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@when('el usuario busca "{termino}"')
def step_buscar_producto(context, termino):
    """Realiza la busqueda del termino indicado desde la home."""
    context.termino_busqueda = termino
    context.home.buscar_producto(termino)
    context.search_results = SearchResultsPage(context.page)


@then("la búsqueda devuelve al menos un resultado")
def step_validar_resultados(context):
    """Verifica que la busqueda haya devuelto al menos un producto."""
    assert context.search_results.hay_resultados(), (
        f"La busqueda de '{context.termino_busqueda}' no devolvio resultados."
    )


@when("el usuario abre el primer producto de los resultados")
def step_abrir_primer_producto(context):
    """Abre el detalle del primer producto del listado de resultados."""
    context.search_results.abrir_primer_producto()
    context.product_page = ProductPage(context.page)
    # Se guarda el nombre del producto para validaciones posteriores
    context.nombre_producto = context.product_page.obtener_nombre()


@when("el usuario agrega el producto al carrito")
def step_agregar_al_carrito(context):
    """Agrega el producto al carrito desde la pagina de detalle."""
    context.product_page.agregar_al_carrito(cantidad=1)


@then("el carrito contiene el producto seleccionado")
def step_validar_producto_en_carrito(context):
    """Navega al carrito y valida que el producto agregado este presente."""
    # Acceso directo al carrito por ruta para evitar dependencias del menu
    context.page.goto(
        Config.BASE_URL.rstrip("/") + "/index.php?route=checkout/cart"
    )
    cart = CartPage(context.page)
    assert cart.cantidad_items() > 0, "El carrito esta vacio."
    assert cart.contiene_producto(context.nombre_producto), (
        f"El producto '{context.nombre_producto}' no se encuentra en el carrito."
    )
    # Se guarda en el contexto para reutilizar en checkout
    context.cart_page = cart
