from flask import render_template_string
import base64
import json
from google.cloud import spanner

INDEX_TEMPLATE = """
<!DOCTYPE html>
<head>
  <title>Account Balances</title>
</head>
<body>
  {% for place in places %}
  Results, <b>{{ place }}!</b><br>
  {% endfor %}
</body>
"""

def query_data(instance_id, database_id):
    """Queries sample data from the database using SQL."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "Select AccountId, Balance from Account Where AccountId=FROM_BASE64('MLcHnG6cTY2PAm8ICdjdPA==')"
        )

    data = []
    for row in results:
      data.append(str("Account {} Balance: {}".format(row[0],row[1])))

    return data



def render(request):
    return render_template_string(
        INDEX_TEMPLATE, places=query_data("bitfoon-dev","finance")
    )
