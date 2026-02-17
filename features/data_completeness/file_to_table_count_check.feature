Feature: Row Count Validation

  @smoke_test
  Scenario Outline: Validate record count matches between source file and target table
    Given the table "<table_name>" is loaded
    And the expected dataset "<file_name>" is available
    Then the row count should match

    Examples:
      | table_name | file_name      |
      | agreements | agreements.csv |
      | contact    | contact.csv    |
