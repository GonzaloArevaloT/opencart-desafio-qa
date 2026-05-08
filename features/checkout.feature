@checkout
Feature: Checkout como invitado
  Como cliente invitado
  Quiero completar una compra sin crear una cuenta
  Para poder comprar productos rápidamente

  @smoke
  Scenario: Completar una compra como invitado
    Given el usuario está en la home de OpenCart
    When el usuario busca "iPhone"
    And el usuario abre el primer producto de los resultados
    And el usuario agrega el producto al carrito
    And el usuario procede al checkout
    And el usuario selecciona checkout como invitado
    And el usuario completa los datos de facturación
    And el usuario confirma el método de envío
    And el usuario confirma el método de pago
    And el usuario finaliza la orden
    Then la orden se crea exitosamente
