import re
import json
import rapidfuzz

import SPARQLWrapper

SPARQL_URL_PREFIX = 'https://query.wikidata.org/sparql'


# HELPER FUNCTIONS

# get sparql results for sparql query string
def get_sparql_results(sparql_query_string):
    sparql = SPARQLWrapper.SPARQLWrapper(SPARQL_URL_PREFIX)
    sparql.setQuery(sparql_query_string)
    try:
        # stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        sparql.setReturnFormat(SPARQLWrapper.JSON)
        result = sparql.query().convert()
    except:
        result = None
    return result


# MAIN FUNCTIONS

def create_index():

    formula_index = {}
    qid_index = {}

    sparql_query_string = """# find all items with defining formula
    SELECT ?formula ?item WHERE {
        ?item wdt:P2534 ?formula.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }"""

    sparql_results = get_sparql_results(sparql_query_string)['results']['bindings']

    nr_results = len(sparql_results)

    result_nr = 1
    nr_successful = 0
    for result in sparql_results:
        # get formula tex
        formula_string = result['formula']['value']
        try:
            formula_tex_string = re.search('%s(.*)%s' % ('alttext="', '">'),
                                        formula_string).group(1)
            print(formula_tex_string)
            # populate index with formula and qid
            formula_qid = result['item']['value'].split('/')[-1]
            formula_index[formula_tex_string] = formula_qid
            qid_index[formula_qid] = formula_tex_string
            nr_successful += 1
        except:
            print('failed')

        # display progress
        print('Processed: ' + str(result_nr / nr_results * 100) + '%')
        print('Successful: ' + str(nr_successful / result_nr * 100) + '%')

        result_nr += 1

    # # save formula index
    # with open('formula_index.json', 'w') as f:
    #    json.dump(formula_index, f)
    # # save qid index
    # with open('qid_index.json', 'w') as f:
    #    json.dump(qid_index, f)

    return formula_index, qid_index


def employ_index(formula_index, qid_index, formula_input_string, result_limit):

    # # load formula index
    # with open('formula_index.json','r') as f:
    #    formula_index = json.load(f)
    # # load qid index
    # with open('qid_index.json','r') as f:
    #    qid_index = json.load(f)

    match_candidates = {}

    for formula_index_string in formula_index:
        formula_qid = formula_index[formula_index_string]
        fuzz_ratio = rapidfuzz.fuzz.ratio(formula_index_string,formula_input_string)
        match_candidates[formula_qid] = fuzz_ratio

    match_candidates_sorted = sorted(match_candidates.items(), key=lambda kv: kv[1], reverse=True)
    results = match_candidates_sorted[:result_limit]

    for result in results:
        qid = result[0]
        formula = qid_index[qid]
        score = result[1]
        result_jsonline = {'qid': qid, 'formula': formula, 'score': score}
        print(result_jsonline)

    return results

# EXECUTE

print('\nCREATE INDEX\n')
formula_index,qid_index = create_index()
print('\nEMPLOY INDEX\n')
formula_input_string = 'E=mc^2'
result_limit = 10
formula_qid = employ_index(formula_index,qid_index,
                           formula_input_string,
                           result_limit)
