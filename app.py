from flask import Flask, session, render_template, request, g, redirect, url_for, flash
import boto3
from rich import print
import json
import ast
import html

app = Flask(__name__)
app.secret_key = "this_is_a_secret_key"


@app.route("/", methods=["POST", "GET"])
def index():
    session["all_items"] = get_db()
    flash("Data refreshed successfully!")
    list = ['Hello', 'this', 'what']
    
    return render_template("index.html", all_items=session["all_items"])


@app.route("/refresh", methods=["GET"])
def refresh():
    session["all_items"] = get_db()
    flash("Data refreshed successfully!")
    return redirect(url_for("index"))


@app.route("/remove_items", methods=["post"])
def remove_items():
    checked_boxes = clean_data(request.form.getlist("check"))

    # TODO: Add code to remove logs from DB
    response = delete_items(checked_boxes)
    print(response)
    if response.get("UnprocessedItems"):
        print("Unprocessed items detected:")
        print(response["UnprocessedItems"])
    else:
        to_delete_items = [log["log_id"]["S"] for log in checked_boxes]
        session["all_items"] = [
            log
            for log in session["all_items"]
            if log["log_id"]["S"] not in to_delete_items
        ]
    
    if (session["all_items"]):
        return render_template("index.html", all_items=session["all_items"])
    else:
        return redirect(url_for("refresh"))


@app.template_filter('json_formater')
def json_formater(s):
    formatted_json = json.dumps(s, indent=4)
    escaped_json = html.escape(formatted_json)
    
    html_template = f"""<td class="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{escaped_json}
            </td>
    """
    
    
    return html_template

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = boto3.client("dynamodb")
        all_data = db.scan(TableName="LogsTable", Limit=12)
        data = all_data["Items"]
    return data


def delete_items(items_to_delete):
    dynamodb = boto3.client("dynamodb")
    table_name = "LogsTable"
    # Prepare the batch delete request
    delete_requests = [{"DeleteRequest": {"Key": item}} for item in items_to_delete]

    try:
        response = dynamodb.batch_write_item(RequestItems={table_name: delete_requests})
        return response
    except Exception as e:
        print(e)


def clean_data(data):
    cleaned_data = []
    for entry in data:
        # Parse JSON string into a dictionary
        parsed_entry = json.loads(entry)

        # Manually evaluate the nested dictionary-like strings
        parsed_entry["log_id"] = ast.literal_eval(parsed_entry["log_id"])
        parsed_entry["timestamp"] = ast.literal_eval(parsed_entry["timestamp"])

        # Append the formatted dictionary to the cleaned data
        cleaned_data.append(
            {"log_id": parsed_entry["log_id"], "timestamp": parsed_entry["timestamp"]}
        )

    # Resulting list of proper dictionaries
    return cleaned_data


if __name__ == "__main__":
    app.run()
