import os
import flask
from flask import request, jsonify

from backend.annomathtex.settings.common import PROJECT_ROOT
from backend.api.helper_classes.annomathtex_evaluation_handler import AnnoMathTexEvaluationHandler
from backend.api.helper_classes.index_evaluation_handler import IndexEvaluationHandler

import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.annomathtex.settings.development")

app = flask.Flask(__name__)
# app.config['DEBUG'] = True
app.config['DEBUG'] = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def home():
    return '''<h1>MathWikiLink</h1>
<p>An Entity Linking System for Mathematical Formulae.</p>'''


@app.route('/api/v1/identifier_names', methods=['GET'])
def get_identifier_names():
    """
    HTTP GET API endpoint providing recommendations for requested identifier names from local index in /index
    or inbuilt AnnoMathTex Instance with live SPARQGL retrieval from wikidata /backend/annomathtex.

    :argument identifier: identifier name for which recommendations will be returned
    :argument source: source from which recommendation will be returned (default: index, others: annomathtex)
    :argument limit: number of returned recommendations per source
    :return via HTTP: JSON formatted recommendations dictionary
    """

    # Limit to specific number (of identifier name recommendations)
    try:
        limit = int(request.args['limit'])
    except:
        limit=5

    # Check if retrieval source argument is given
    if 'source' in request.args:
        # check if source is provided as part of the URL
        if request.args['source'] == 'annomathtex':
            source = 'annomathtex'
        elif request.args['source'] == 'index':
            source = 'index'
        else:
            return 'Error: Retrieval source ' + request.args['source'] + ' is unknown.'
    else:
        source = 'index'

    # Check if identifier name argument is given
    if 'identifier' in request.args:
        # Check if an identifier was provided as part of the URL.
        identifier = request.args['identifier']
    else:
        return 'Error: No identifier attribute provided. Please specify an identifier.'

    # Retrieve recommendation results from IndexEvaluationHandler Class
    if source == 'index':
        results = IndexEvaluationHandler('identifier').check_identifier_index(symbol=identifier, limit=limit)
        # Convert dict to json
        return jsonify(results)

    # Retrieve recommendation results from AnnoMathTexEvaluationHandler Class
    elif source == 'annomathtex':
        results = AnnoMathTexEvaluationHandler('identifier', identifier).annomathtex_retrieval(limit)
        # Convert dict to json
        return jsonify(results)

    return 'Error in get_identifier_names()'


@app.route('/api/v1/formula_names', methods=['GET'])
def get_formula_names():
    """
    HTTP GET API endpoint providing recommendations for requested formulae from local index in /index
    or inbuilt AnnoMathTex Instance with live SPARQGL retrieval from wikidata /backend/annomathtex.

    :argument formula: formula for which recommendations will be returned, formatting example: c^2=b^2+c^2
    :argument source: source from which recommendation will be returned (default: index, others: annomathtex)
    :argument limit: number of returned recommendations per source
    :return via HTTP: JSON formatted recommendations dictionary
    """
    # Limit to specific number (of identifier name recommendations)
    try:
        limit = int(request.args['limit'])
    except:
        limit=5

    # Check if retrieval source argument is given
    if 'source' in request.args:
        # check if source is provided as part of the URL
        if request.args['source'] == 'annomathtex':
            source = 'annomathtex'
        elif request.args['source'] == 'index':
            source = 'index'
        else:
            return 'Error: Retrieval source ' + request.args['source'] + ' is unknown.'
    else:
        source = 'index'

    # Check if formula argument is given
    if 'formula' in request.args:
        # Check if a formula was provided as part of the URL.
        formula = request.args['formula']
    else:
        return 'Error: No formula attribute provided. Please specify a formula.'

    # Retrieve recommendation results from IndexEvaluationHandler Class
    if source == 'index':
        results = IndexEvaluationHandler('formula').check_formula_index(formula=formula, limit=limit)
        # Convert dict to json
        return jsonify(results)

    # Retrieve recommendation results from AnnoMathTexEvaluationHandler Class
    elif source == 'annomathtex':
        results = AnnoMathTexEvaluationHandler('formula', formula).annomathtex_retrieval(limit)
        # Convert dict to json
        return jsonify(results)

    return 'Error in get_formula_names()'


app.run()
