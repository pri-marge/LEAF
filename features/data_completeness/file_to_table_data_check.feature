Feature: Record Data Validation

  Scenario Outline: Validate all coulmn data matches between source file and target table
    Given the table "<table_name>" is loaded
    And the expected dataset "<file_name>" is available
    Then all records should match expected dataset using join columns "<join_columns>"

    Examples:
      | table_name | file_name      | join_columns |
      | agreements | agreements.csv | account_key  |
      | contact    | contact.csv    | customer_key |
