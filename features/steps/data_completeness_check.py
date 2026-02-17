import pandas as pd
import datacompy
from behave import given, then

@given('the table "{table_name}" is loaded')
def step_load_table(context, table_name):
    sql_query = f"""
    SELECT *
    FROM {table_name}
    WHERE project_key = %s
    """
    context.current_df = pd.read_sql(sql_query, context.conn,params=[context.project_key])

@given('the expected dataset "{file_name}" is available')
def step_load_expected_dataset(context, file_name):
    context.expected_df = pd.read_csv(f"data/{file_name}")

@then('the row count should match')
def step_row_count(context):
    actual = len(context.current_df)
    expected = len(context.expected_df)
    assert actual == expected, f"Row count mismatch: Table={actual}, File={expected}"

@then('all records should match expected dataset using join columns "{join_columns}"')
def step_all_records_match(context, join_columns):
    join_cols = [col.strip() for col in join_columns.split(",")]
    compare = datacompy.Compare(
        context.current_df,
        context.expected_df,
        join_columns=join_cols,
        abs_tol=0,
        rel_tol=0
    )
    assert compare.matches(), f"Records mismatch:\n{compare.report()}"

