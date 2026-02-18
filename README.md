# LEAF - Lloyds Engineering Automation Framework

LEAF is a Python-based BDD automation framework for validating data quality, completeness, and schema consistency in Postgres tables using **Behave** and **Great Expectations**.

---

### Setup Instructions

### 1. Create Virtual Environment

From the project root, run:

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
```

Then install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---
### 2. Ensure Database is Running

Make sure your Postgres instance is up and accessible.

---
### 3. Update Database Configuration

Edit `config/config.yml` and update your Postgres database connection details:

```yaml
database:
  host: localhost
  port: 5432
  name: your_db_name
  user: your_user
  password: your_password
```
---

### 4. Setup Test Data

Create tables and load CSV data for testing:

```bash
python setup_db.py
```

---

### 5. Run Behave Tests

```bash
# Run BDD scenarios
behave --format=pretty 

# Run BDDonly smoke test scenarios
behave --tags=smoke_test
```

---

### 6. Generate Allure Report

```bash
# Run tests with Allure formatter
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Open report in browser
allure open reports/allure-report
```

---


