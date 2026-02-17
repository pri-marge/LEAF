from behave import given, when, then
from great_expectations.data_context import DataContext
import time
from gx_helper import get_agreements_validator,ge_context

@given("the agreements checkpoint is ready")
def step_setup(context):
    """
    Initialize data context and add all expectations before running checkpoint
    """
    context.validator = get_agreements_validator()
    v = context.validator

    # --- Add all expectations here ---
    v.expect_column_values_to_not_be_null("account_key")
    v.expect_column_values_to_be_unique("account_key")
    v.expect_column_values_to_not_be_null("project_key")
    v.expect_column_values_to_be_in_set("payment_method", ["DD", "CARD", "CASH"])
    v.expect_column_values_to_be_in_set("payment_freq", ["MONTHLY", "QUARTERLY", "ANNUAL"])
    v.expect_column_values_to_not_be_null("arrears")
    v.expect_column_values_to_not_be_null("capital_outstanding")    
    v.expect_column_values_to_be_between("arrears", min_value=0)
    v.expect_column_values_to_be_between("capital_outstanding", min_value=0)
    v.expect_column_values_to_not_be_null("start_date")
    v.expect_column_values_to_not_be_null("maturity_date")

    # Save expectation suite to JSON
    v.save_expectation_suite()

@when("I run agreements checkpoint")
def step_run_checkpoint(context):
    context.checkpoint_result = ge_context.run_checkpoint(
        checkpoint_name="agreements_checkpoint",
        result_format={"result_format": "SUMMARY"},
        run_name=f"agreements_run_{int(time.time())}"
    )

@then('"{column_name}" in agreements table should be valid')
def step_column_should_be_valid(context, column_name):
    """
    Assert the column validations passed.
    """
    run_results = context.checkpoint_result["run_results"]

    # Iterate through results and raise AssertionError if any expectation fails
    for run in run_results.values():
        for result in run["validation_result"]["results"]:
            kwargs = result["expectation_config"]["kwargs"]
            checked_column = kwargs.get("column") or kwargs.get("column_A") or kwargs.get("column_B")

            if checked_column == column_name and not result["success"]:
                raise AssertionError(f"Validation failed for column '{column_name}'")

@then("maturity_date should be after start_date")
def step_maturity_after_start(context):
    """
    Assert that maturity_date > start_date using checkpoint results
    """
    run_results = context.checkpoint_result["run_results"]
    for run in run_results.values():
        for result in run["validation_result"]["results"]:
            expectation_type = result["expectation_config"]["expectation_type"]
            col_a = result["expectation_config"]["kwargs"].get("column_A")
            col_b = result["expectation_config"]["kwargs"].get("column_B")
            
            # Only check the specific column pair
            if expectation_type == "expect_column_pair_values_a_to_be_greater_than_b" and \
               col_a == "maturity_date" and col_b == "start_date":
                
                if not result["success"]:
                    raise AssertionError(
                        "Validation failed: some maturity_date values are not greater than start_date"
                    )
