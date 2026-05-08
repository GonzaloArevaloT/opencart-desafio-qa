"""Steps relacionados al flujo de registro de usuario."""
from behave import when, then

from pages.account_success_page import AccountSuccessPage
from pages.register_page import RegisterPage
from utils.data_factory import DataFactory


@when("el usuario abre el formulario de registro")
def step_abrir_formulario_registro(context):
    """Navega desde la home hacia la pagina de registro."""
    context.home.ir_a_registro()
    context.register_page = RegisterPage(context.page)
    context.register_page.esta_visible()


@when("el usuario completa el formulario con datos válidos")
def step_completar_registro(context):
    """Genera datos dinamicos y los carga en el formulario."""
    context.usuario = DataFactory.generar_usuario()
    context.register_page.completar_formulario(context.usuario)


@when("el usuario acepta la política de privacidad")
def step_aceptar_privacidad(context):
    """Marca el checkbox de aceptacion de la politica."""
    context.register_page.aceptar_politica_privacidad()


@when("el usuario envía el formulario de registro")
def step_enviar_formulario(context):
    """Envia el formulario de registro."""
    context.register_page.enviar()


@then("la cuenta se crea exitosamente")
def step_validar_registro_exitoso(context):
    """Valida que la pagina muestre la confirmacion de creacion de cuenta."""
    pagina_exito = AccountSuccessPage(context.page)
    assert pagina_exito.fue_exitoso(), (
        f"No se confirmo la creacion de cuenta. "
        f"Titulo recibido: '{pagina_exito.obtener_titulo()}'"
    )
