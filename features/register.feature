@register
Feature: Registro de usuario
  Como nuevo visitante de la tienda OpenCart
  Quiero crear una cuenta nueva
  Para poder acceder a funcionalidades exclusivas

  @smoke
  Scenario: Registro exitoso de nuevo usuario
    Given el usuario está en la home de OpenCart
    When el usuario abre el formulario de registro
    And el usuario completa el formulario con datos válidos
    And el usuario acepta la política de privacidad
    And el usuario envía el formulario de registro
    Then la cuenta se crea exitosamente
