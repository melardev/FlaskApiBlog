from flask import jsonify

from blog_api.factory import app


@app.route("/routes")
def site_map():
    links = []
    # for rule in app.url_map.iter_rules():
    for rule in app.url_map._rules:
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        links.append({'ulr': rule.rule, 'view': rule.endpoint})
    return jsonify(links), 200
