import yaml
import psycopg2
from pathlib import Path
import logging
import warnings
warnings.filterwarnings("ignore")

def before_all(context):
    logging.getLogger("great_expectations").setLevel(logging.CRITICAL)
    logging.getLogger("datacompy").setLevel(logging.CRITICAL)

    # Load config file
    config_path = Path(__file__).parent.parent / "config/config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    context.config_data = config

    context.project_key = config['project']['key']

    db_config = config['database']

    # Create DB connection
    context.conn = psycopg2.connect(
        host=db_config['host'],
        database=db_config['name'],
        user=db_config['user'],
        password=db_config['password']
    )

def after_all(context):
    context.conn.close()
