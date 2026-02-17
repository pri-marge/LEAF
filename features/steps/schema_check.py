import pandas as pd
import psycopg2
from behave import given, then
from pathlib import Path
import yaml

@given('the table "{table_name}" is available')
def step_table_available(context, table_name):
    conn = context.conn
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """, (table_name,))
    exists = cursor.fetchone()[0]
    if not exists:
        raise AssertionError(f"Table '{table_name}' does not exist in database.")

    context.table_name = table_name

    # Fetch table structure
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
    """
    context.db_schema = pd.read_sql(query, conn, params=[table_name])

@then("the schema should match the expected definition")
def step_validate_schema(context):
    table_name = context.table_name
    expected_schema = context.config_data["schema"][table_name]

    db_columns = dict(zip(context.db_schema.column_name, context.db_schema.data_type))

    # --- Missing columns ---
    missing_columns = [col for col in expected_schema if col not in db_columns]
    if missing_columns:
        raise AssertionError(f"Missing columns in {table_name}: {missing_columns}")

    # --- Extra columns ---
    extra_columns = [col for col in db_columns if col not in expected_schema]
    if extra_columns:
        raise AssertionError(f"Unexpected columns in {table_name}: {extra_columns}")

    # --- Type check ---
    TYPE_MAPPING = {
    "string": ["text", "varchar","double precision"],  # All text columns
    "float": ["numeric", "real", "double precision", "bigint"],  # Numeric + bigint
    "integer": ["integer", "bigint", "smallint"],  # INT + BIGINT
    "datetime": ["date", "timestamp without time zone", "timestamp with time zone", "text"]  # Dates stored as text included
    }


    type_mismatches = []
    for col, expected_type in expected_schema.items():
        actual_type = db_columns.get(col)
        if actual_type not in TYPE_MAPPING.get(expected_type, []):
            type_mismatches.append(f"{col}: expected {expected_type}, found {actual_type}")

    if type_mismatches:
        raise AssertionError(f"Data type mismatches in {table_name}: {type_mismatches}")

    # --- Column order warning ---
    db_column_order = list(context.db_schema.column_name)
    if db_column_order != list(expected_schema.keys()):
        print(f"Warning: Column order mismatch in {table_name}")
