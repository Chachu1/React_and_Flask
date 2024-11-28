import json
import html


def generate_html_with_tailwind(json_data):
    """
    Generate an HTML page that displays a formatted JSON string with Tailwind CSS.

    Args:
        json_data (dict): The JSON data to format and display.

    Returns:
        str: HTML string with formatted JSON using Tailwind CSS.
    """
    # Pretty print the JSON
    formatted_json = json.dumps(json_data, indent=4)
    # Escape special HTML characters
    escaped_json = html.escape(formatted_json)

    # HTML structure with Tailwind CSS
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Formatted JSON</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
            <h1 class="text-2xl font-bold text-gray-800 mb-4">Formatted JSON</h1>
            <pre class="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{escaped_json}
            </pre>
        </div>
    </body>
    </html>
    """
    return html_template


# Example Usage
json_input = {
    "level": {"S": "ERROR"},
    "log_id": {
        "S": "2024/11/25/Scrapper_Eureka_KW[$LATEST]eba56d5d8dd64fcb8e4141a6703cb3f7"
    },
    "logger": {"S": "Scrapper_Eureka_KW"},
    "message": {
        "S": "Request error for URL('https://www.eureka.com.kw/list/getlistingitems?Brands=&Category=&Classes=&Flag=browse&OnlyAvailableItems=false&PageNumber=0&RootCategory=travel-bags&RowsPerPage=1000&SortOrder=pricel2h'): "
    },
    "requestId": {"S": "0c69337b-d3f6-453c-8050-82a28946bd44"},
    "taskName": {"S": "Task-15"},
    "timestamp": {"S": "2024-11-25T00:01:29Z"},
}

# Generate the HTML
html_output = generate_html_with_tailwind(json_input)

# Save to a file or print
with open("formatted_json_tailwind.html", "w") as file:
    file.write(html_output)
