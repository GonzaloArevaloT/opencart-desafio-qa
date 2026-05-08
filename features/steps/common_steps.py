"""Steps comunes reutilizados por varios features."""
from behave import given

from pages.home_page import HomePage


@given("el usuario está en la home de OpenCart")
def step_abrir_home(context):
    """Inicializa el page object de Home y abre la URL base."""
    context.home = HomePage(context.page)
    context.home.abrir()
