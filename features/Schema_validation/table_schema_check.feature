Feature:Table Schema Validation

@schema_check
Scenario Outline: Validate table schema matches expected definition
  Given the table "<table_name>" is available
  Then the schema should match the expected definition

Examples:
  | table_name |
  | agreements |
  | contact    |
