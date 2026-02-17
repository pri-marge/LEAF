import pandas as pd
import yaml
from sqlalchemy import create_engine, text
from pathlib import Path


config_path = Path(__file__).parent / "config/config.yml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

db_config = config['database']

DB_USER = db_config['user']
DB_PASS = db_config['password']
DB_HOST = db_config['host']
DB_PORT = db_config['port']
DB_NAME =db_config['name']

# Sample CSV paths 
AGREEMENTS_CSV = "data/agreements.csv"
CONTACT_CSV = "data/contact.csv"

# -----------------------------
# CREATE ENGINE
# -----------------------------
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------
# CREATE TABLES
# -----------------------------
table_statements = [
    """
  CREATE TABLE IF NOT EXISTS agreements (
    project_key TEXT,
    account_key TEXT PRIMARY KEY,
    customer_key TEXT,
    portfolio_id TEXT,
    capital_outstanding NUMERIC,
    arrears NUMERIC,
    term INT,
    start_date DATE,
    maturity_date DATE,
    payment_freq TEXT,
    payment_method TEXT
);

-- Contact table
CREATE TABLE IF NOT EXISTS contact (
    project_key TEXT,
    customer_key TEXT,
    contact_type TEXT,
    title TEXT,
    first_name TEXT,
    last_name TEXT,
    company_name TEXT,
    home_phone TEXT,
    mobile NUMERIC,
    email TEXT,
    address_line_1 TEXT,
    address_line_2 TEXT,
    address_line_3 TEXT,
    postcode TEXT,
    gender TEXT,
    date_of_birth DATE,
    date_of_death DATE
);
    """
]

with engine.connect() as conn:
    for stmt in table_statements:
        conn.execute(text(stmt))
    print("Tables created or already exist.")

# -----------------------------
# LOAD CSVs
# -----------------------------
csv_mapping = {
    "agreements": AGREEMENTS_CSV,
    "contact": CONTACT_CSV,
}

for table, path in csv_mapping.items():
    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"{len(df)} rows loaded into table '{table}' from '{path}'.")

# -----------------------------
# VERIFY ROWS
# -----------------------------
with engine.connect() as conn:
    for table in csv_mapping.keys():
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"Table '{table}' has {count} rows.")
