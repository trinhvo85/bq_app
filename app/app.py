import json

import newrelic.agent
from flask import Flask, Response, request
from helper import *

newrelic.agent.initialize("../newrelic.ini")

app = Flask(__name__)
application = newrelic.agent.WSGIApplicationWrapper(app)


@app.route("/healthz", methods=["GET", "POST"])
def healthz():
    return "OK"


@app.route("/conversion_attempt", methods=["GET"])
def get_conversion_attempt():
    args = request.args

    conversion_attempt_key = args.get("key", "").strip().strip("'\"")

    status = 200

    if is_valid_conversion_attempt_key(conversion_attempt_key):
        sql = """
            SELECT * FROM `tjbigquery.risk.ml_prediction` WHERE conversion_attempt_key = '{}'
            """

        query_job = BQ_CLIENT.query(sql.format(conversion_attempt_key))

        results = query_job.result()  # Wait for the job to complete.

        response = []
        for row in results:
            response.append(
                {
                    "experiment": row.experiment,
                    "item_type": row.item_type,
                    "resolution": row.resolution,
                    "rule_block_name": row.rule_block_name,
                    "stats_date": row.stats_date,
                }
            )
    else:
        response = {"error": "Invalid conversion attempt key"}
        status = 406

    return Response(
        json.dumps(response, sort_keys=True, default=str),
        status=status,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app = newrelic.agent.wsgi_application()(app)
    app.run(host="0.0.0.0", port=APP_PORT, debug=True)
