from behave import given, when, then
from gx_helper import get_contact_validator, ge_context
import time

@given("the contact checkpoint is ready")
def step_setup_contact(context):
    context.validator = get_contact_validator()
    v = context.validator

    # --- Add column expectations ---
    v.expect_column_values_to_not_be_null("project_key")
    v.expect_column_values_to_not_be_null("customer_key")
    v.expect_column_values_to_not_be_null("contact_type")
    v.expect_column_values_to_not_be_null("first_name")
    v.expect_column_values_to_not_be_null("last_name")
    
    # Unique constraints
    v.expect_column_values_to_be_unique("customer_key")

    # Save the suite
    v.save_expectation_suite()

@when("I run contact checkpoint")
def step_run_contact_checkpoint(context):
    # Use shared ge_context instead of context.data_context
    context.checkpoint_result = ge_context.run_checkpoint(
        checkpoint_name="contact_checkpoint",
        run_name=f"contact_run_{int(time.time())}"
    )

@then('"{column_name}" in contact table should be valid')
def step_column_valid_contact(context, column_name):
    run_results = context.checkpoint_result["run_results"]
    for run in run_results.values():
        for result in run["validation_result"]["results"]:
            kwargs = result["expectation_config"]["kwargs"]
            checked_column = kwargs.get("column") or kwargs.get("column_A") or kwargs.get("column_B")
            if checked_column == column_name and not result["success"]:
                raise AssertionError(f"Validation failed for column '{column_name}'")
