import os

from google.cloud import bigquery

APP_PORT = os.getenv("APP_PORT", "5050")
BQ_PROJECT = os.getenv("BQ_PROJECT", "tjbigquery-dev")

ENV = os.getenv("FLASKENV", "localdev")

if (ENV == "localdev") and (os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "") == ""):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        os.path.expanduser("~") + "/.config/gcloud/application_default_credentials.json"
    )

BQ_CLIENT = bigquery.Client(project=BQ_PROJECT)


def is_valid_conversion_attempt_key(key: str):
    if key is None:
        return False

    key = key.strip().strip("'\"")

    if key == "":
        return False

    return True
