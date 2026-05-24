Feature: Nykaa Hair End To End Flow

  As a Nykaa user
  I want to search and purchase beauty products
  So that I can complete checkout successfully


   Scenario: Verify product can be added to cart

    Given the user launches the Nykaa website
    When the user searches for "shampoo"
    And the user opens the first product
    And the user adds the product to the cart
    Then the product should be added successfully


  Scenario: Verify user can open cart

    Given the user launches the Nykaa website
    When the user searches for "conditioner"
    And the user opens the first product
    And the user adds the product to the cart
    And the user opens the shopping cart
    Then the cart page should be displayed


  Scenario: Verify guest checkout flow

    Given the user launches the Nykaa website
    When the user searches for "hair oil"
    And the user opens the first product
    And the user adds the product to the cart
    And the user opens the shopping cart
    And the user proceeds to checkout
    And the user continues as guest
    Then the checkout page should open


  Scenario: Verify address form submission

    Given the user launches the Nykaa website
    When the user searches for "shampoo"
    And the user opens the first product
    And the user adds the product to the cart
    And the user opens the shopping cart
    And the user proceeds to checkout
    And the user continues as guest
    And the user fills the address form
    Then the shipping button should be visible


  Scenario: Verify invalid pincode validation

    Given the user launches the Nykaa website
    When the user searches for "shampoo"
    And the user opens the first product
    And the user adds the product to the cart
    And the user opens the shopping cart
    And the user proceeds to checkout
    And the user continues as guest
    And the user enters invalid pincode
    Then the user should remain on address page

  Scenario: Empty Address Validation

    Given the user launches the Nykaa website
    When the user searches for "shampoo"
    And the user opens the first product
    And the user adds the product to the cart
    And the user opens the shopping cart
    And the user proceeds to checkout
    And the user continues as guest
    And the user tries checkout with empty address fields
    Then address validation errors should be displayed
