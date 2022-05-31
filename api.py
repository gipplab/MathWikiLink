import os
import flask
from flask import request, jsonify
from backend.annomathtex.views.helper_classes.token_clicked_handler import TokenClickedHandler

import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.annomathtex.settings.development")

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>MathWikiLink</h1>
<p>An Entity Linking System for Mathematical Formulae.</p>'''


@app.route('/api/v1/identifier_names', methods=['GET'])
def get_identifier_names():

    if 'identifier' in request.args:
        # Check if an identifier was provided as part of the URL.
        identifier = request.args['identifier']
    else:
        return 'Error: No identifier attribute provided. Please specify an identifier.'

    annomathtex_item = {
        'action': {'getRecommendations': ''},
        'searchString': {identifier: ''},
        'tokenType': {'Identifier': ''},
        'uniqueId': {'0---0': ''},
        'mathEnv': {'dummy': 'dummy'},
        'annotations': 'none'
    }

    response, source_dicts = TokenClickedHandler(annomathtex_item).get_recommendations()

    # Get identifier name recommendations for input identifier
    results = {}

    # Limit to specific number (of identifier name recommendations)
    try:
        limit = int(request.args['limit'])
    except:
        limit=5

    def get_results(source, attribute, limit):
        results_prepared = []
        for recommendation in source_dicts[source][:limit]:
            try:
                results_prepared.append(recommendation[attribute])
            except KeyError as e:
                if e.args[0] == 'qid':
                    results_prepared.append('')
                else:
                    return 'KeyError in get_results'
        return results_prepared

    for source in source_dicts:
        name_attribute = 'name'
        qid_attribute = 'qid'
        try:
            results[source] = {'name': get_results(source, name_attribute, limit), 'qid': get_results(source, qid_attribute, limit)}
        except:
            return 'Error in results conversion'
            # results[source] = []

    # Convert dict to json
    return jsonify(results)


@app.route('/api/v1/formula_names', methods=['GET'])
def get_formula_names():

    if 'formula' in request.args:
        # Check if an identifier was provided as part of the URL.
        formula = request.args['formula']
    else:
        return 'Error: No identifier attribute provided. Please specify an identifier.'

    # splitting the formula at '='
    try:
        formula_identifier_explained = formula.split('=', 1)[0]
        formula_identifier_explaining = formula.split('=', 1)[1]
    except:
        return 'Error: No formula provided'

    annomathtex_item = {
        'action': {'getRecommendations': ''},
        'searchString': {formula_identifier_explained: formula_identifier_explaining},
        'tokenType': {'Formula': ''},
        'uniqueId': {'0---0': ''},
        'mathEnv': {'dummy': formula},
        'annotations': 'none'
    }

    response, source_dicts = TokenClickedHandler(annomathtex_item).get_recommendations()

    # Get formula name recommendations for input formula string
    results = {}

    # Limit to specific number (of identifier name recommendations)
    try:
        limit = int(request.args['limit'])
    except:
        limit=5

    def get_results(source, attribute, limit):
        results_prepared = []
        for recommendation in source_dicts[source][:limit]:
            try:
                results_prepared.append(recommendation[attribute])
            except KeyError as e:
                if e.args[0] == 'qid':
                    results_prepared.append('')
                else:
                    return 'KeyError in get_results'
        return results_prepared

    for source in source_dicts:
        name_attribute = 'name'
        qid_attribute = 'qid'
        try:
            results[source] = {'name': get_results(source, name_attribute, limit), 'qid': get_results(source, qid_attribute, limit)}
        except:
            return 'Error in results conversion'
            # results[source] = []

    # Convert dict to json
    return jsonify(results)

#todo: consolidate common parts of identifier and formula_name retrieval into one helper function if possible/useful

app.run()
