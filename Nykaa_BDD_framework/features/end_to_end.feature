Feature: Nykaa End to End Checkout

  Scenario: Guest user completes full checkout flow
    Given user opens Nykaa website
    When user searches for "shampoo"
    And user selects first product
    And user adds product to bag
    And user opens cart
    And user proceeds to checkout
    And user continues as guest user
    And user fills address details
    Then user should reach payment or checkout page

