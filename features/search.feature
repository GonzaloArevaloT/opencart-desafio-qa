@search
Feature: Búsqueda de productos y agregado al carrito
  Como cliente
  Quiero buscar productos y agregarlos al carrito
  Para luego proceder con su compra

  @smoke
  Scenario Outline: Buscar un producto y agregarlo al carrito
    Given el usuario está en la home de OpenCart
    When el usuario busca "<producto>"
    Then la búsqueda devuelve al menos un resultado
    When el usuario abre el primer producto de los resultados
    And el usuario agrega el producto al carrito
    Then el carrito contiene el producto seleccionado

    Examples:
      | producto |
      | iPhone   |
      | MacBook  |
