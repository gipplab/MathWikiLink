import flask
from flask import request, jsonify

import json

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>MathWikiLink</h1>
<p>An Entity Linking System for Mathematical Formulae.</p>'''

@app.route('/api/v1/identifier_names', methods=['GET'])
def get_identifier_names(limit=5):

    # Check if an identifier was provided as part of the URL.
    if 'identifier' in request.args:
        identifier = request.args['identifier']
    else:
        return 'Error: No identifier attribute provided. Please specify an identifier.'

    # Open sources/identifier_name_recommendations
    source_path = 'sources/'
    sources = ['Wikidata', 'Wikipedia', 'arXiv']
    source_dicts = {}
    for source in sources:
        with open(source_path + '/' + 'identifier_name_recommendations_' + source + '.json', 'r') as f:
            source_dicts[source] = json.load(f)

    # Get identifier name recommendations for input identifier
    results = {}

    # limit to specific number (of identifier name recommendations)
    try:
        limit = int(request.args['limit'])
    except:
        pass

    def get_results(source,attribute,limit):
        if attribute == '':
            return source_dicts[source][identifier][:limit]
        else:
            return [recommendation[attribute]
             for recommendation in source_dicts[source][identifier][:limit]]

    for source in sources:
        if source == 'arXiv':
            attribute = ''
        if source == 'Wikipedia':
            attribute = 'description'
        if source == 'Wikidata':
            attribute = 'name'
        try:
            results[source] = get_results(source,attribute,limit)
        except:
            results[source] = []

    # Convert dict to json
    return jsonify(results)

app.run()