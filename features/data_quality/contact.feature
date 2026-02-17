Feature: Contact Data Quality 
  Ensure that all critical data columns in the contact table meet business rules and data quality standards.

  Background:
    Given the contact checkpoint is ready
    When I run contact checkpoint

  @smoke_test
  Scenario: Validate project keys
    Then "project_key" in contact table should be valid

  @smoke_test
  Scenario: Validate customer_key 
    Then "customer_key" in contact table should be valid

  Scenario: Validate name 
    Then "first_name" in contact table should be valid
    and "last_name" in contact table should be valid

