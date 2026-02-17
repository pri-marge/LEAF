Feature: Agreements Data Quality
  Ensure that all critical data columns in the agreements table meet business rules and data quality standards.

  Background:
    Given the agreements checkpoint is ready

  @smoke_test
  Scenario: Validate account keys
    When I run agreements checkpoint
    Then "account_key" in agreements table should be valid

  @smoke_test
  Scenario: Validate project keys
    When I run agreements checkpoint
    Then "project_key" in agreements table should be valid

  Scenario: Validate capital outstanding
    When I run agreements checkpoint
    Then "captial_outstanding" in agreements table should be valid

   Scenario: Validate arrears
    When I run agreements checkpoint   
    Then "arrears" in agreements table should be valid

  Scenario: Validate payment fields
    When I run agreements checkpoint
    Then "payment_freq" in agreements table should be valid

  Scenario: Validate payment fields
    When I run agreements checkpoint
    Then "payment_method" in agreements table should be valid

  Scenario: Validate start date and maturity date
    When I run agreements checkpoint
    Then "start_date" in agreements table should be valid

  Scenario: Validate maturity date 
    When I run agreements checkpoint
    Then "maturity_date" in agreements table should be valid

