from great_expectations.data_context import DataContext

# Single shared DataContext
ge_context = DataContext()

def get_agreements_validator():
    """
    Returns a validator for the 'agreements' table.
    Uses the fluent datasource and builds a batch request automatically.
    """
    suite_name = "agreements_suite"

    # Ensure expectation suite exists
    try:
        ge_context.get_expectation_suite(suite_name)
    except Exception:
        ge_context.add_or_update_expectation_suite(suite_name)

    datasource = ge_context.get_datasource("demo_db")
    asset = datasource.get_asset("agreements")
    batch_request = asset.build_batch_request()

    validator = ge_context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    return validator

def get_contact_validator():
    """
    Returns a validator for the 'contact' table.
    Ensures the suite exists before returning the validator.
    """
    suite_name = "contact_suite"

    # Ensure expectation suite exists
    try:
        ge_context.get_expectation_suite(suite_name)
    except Exception:
        ge_context.add_or_update_expectation_suite(suite_name)

    datasource = ge_context.get_datasource("demo_db")
    asset = datasource.get_asset("contact")
    batch_request = asset.build_batch_request()

    validator = ge_context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    return validator
