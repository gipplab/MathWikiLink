import json
import logging
import time
import os

from backend.annomathtex.recommendation.math_sparql import MathSparql
from backend.annomathtex.recommendation.sparql_queries import identifier_query

logging.basicConfig(level=logging.INFO)
update_identifier_logger = logging.getLogger(' - Update identifier-index - ')

"""
SPARQL-Properties 
    P527    -   has part or parts
    P4934   -   calculated from
    P7235   -   in defining formula
    P416    -   quantity symbol
    P7973   -   quantity symbol (LaTex)
    P2534   -   defining formula   
               
    Example for Usage on: https://github.com/gipplab/PhysWikiQuiz/blob/main/module1_formula_and_identifier_retrieval.py
"""


class IdentifierSPARQLUpdater:
    """
    This class reads the extracted list of already known (local) identifiers and re-queries via SPARQL.

    If there's a new result (previous value is N/A) or a different QID the index is updated.
    """

    def __init__(self, local_file='identifier_index.json'):

        self.identifier_query = identifier_query  # Use the SPARQL-Query already supplied by AnnoMathTex

        # Use different SPARQL-Query with P7973 (quantity symbol (LaTex) for more results than P416 (quantity symbol)
        self.identifier_query_latex = """
            SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {{
                ?item wdt:P7973 ?def.
                FILTER(CONTAINS(?def, '{}'@en))
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .}}
            }}    
            LIMIT {}
        """

        self.wikidata_online_dict = {}
        self.local_dict = {}
        self.n_updated_total = 0
        self.filename = local_file  # Default-Filename
        self.TIME_BETWEEN_QUERY = 2

        path = os.path.join('../../dataset/' + self.filename)

        with open(path, 'r', encoding='utf-8') as f:
            self.local_dict = json.load(f)

        # Check for each identifier given in the dictionary
        for identifier in self.local_dict:

            # Limit the length of identifier in search query to "1" to avoid syntax errors through LaTeX-Content from
            # index file.
            # TODO: Extend to longer identifiers (especially greek symbols in LaTeX-syntax)
            if len(identifier) == 1:
                # Add result to temporary dict
                self.wikidata_online_dict[identifier] = self.query(identifier)

                # Avoid firing too many requests in a short period of time (HTTP 429)
                time.sleep(self.TIME_BETWEEN_QUERY)

                # Query done, compare with (local) file content and integrate new data into local dict
                self.compare(identifier)

        update_identifier_logger.info('Updated a TOTAL of {} QID to index.'.format(self.n_updated_total))

    def dump(self, filename='identifier_index.json'):
        """
        Write results to local JSON-File.
        """

        path = os.path.join('../../dataset/' + filename)
        with open(path, 'w') as f:
            json.dump(self.local_dict, f, ensure_ascii=False, indent=4)
            update_identifier_logger.info('Wrote to file. END.')

    def query(self, identifier=identifier_query):
        """
        Helper-Function for SPARQL-Query. Not sure if necessary.
        """
        identifier_result = MathSparql().query(self.identifier_query, identifier)

        return identifier_result

    def compare(self, identifier):
        """
        Main-Function which compares and updates the results per identifier from the online source to local dictionary.
        """
        # Check if there is online content from Wikidata for given identifier, if not there is nothing to do
        n_updated_identifiers = 0
        if len(self.wikidata_online_dict[identifier]) > 0:

            # Iterate over local dictionary items
            for dict_item in self.local_dict[identifier]:

                # Use only Wikidata-Results
                if dict_item.get('wikidata1Results') is not None:
                    # Wikidata-Results exist
                    # print(self.wikidata_online_dict[identifier])

                    local_item = dict_item['wikidata1Results']
                    online_item = self.wikidata_online_dict[identifier]

                    # Save temporary results in local variables
                    # Output for DEBUG purposes
                    print('IDENTIFIER {}'.format(identifier))
                    online_elements = {}
                    local_elements = {}
                    print('ONLINE')
                    for o_i in online_item:
                        online_elements[o_i['qid']] = {
                            'qid': o_i['qid'],
                            'name': o_i['name'],
                            'item_description': o_i['item_description']
                        }

                        print(' QID : {}, \t NAME: {}, \t DESCRIPTION: {}'.format(o_i['qid'], o_i['name'],
                                                                                  o_i['item_description']))

                    print('===========================')
                    print('LOCAL')
                    for l_i in local_item:
                        local_elements[l_i['qid']] = {
                            'qid': l_i['qid'],
                            'name': l_i['name'],
                            'item_description': l_i['item_description']
                        }

                        print(' QID : {}, \t NAME: {}, \t DESCRIPTION: {}'.format(l_i['qid'], l_i['name'],
                                                                                  l_i['item_description']))

                    # Use only the new QIDs
                    diff = set(online_elements.keys()) - set(local_elements.keys())
                    if len(diff) > 0:
                        print('UPDATE : {}'.format(diff))
                    else:
                        print('UPDATE: no new elements.')

                    # Count the number of updated items
                    n_updated_identifiers = n_updated_identifiers + len(diff)

                    # Copy new online elements (key = QID) into local results
                    for new_qid in diff:
                        dict_item['wikidata1Results'].append(online_elements[new_qid])

                    if n_updated_identifiers > 0:
                        update_identifier_logger.info(
                            'Update: Adding {} new QIDs ({}) for identifier \'{}\' from Wikidata'.format(
                                n_updated_identifiers, diff,
                                identifier))
                    else:
                        update_identifier_logger.info('No new results for identifier \'{}\'.'.format(identifier))

                    self.n_updated_total = self.n_updated_total + n_updated_identifiers
        else:
            update_identifier_logger.info('No results for identifier \'{}\', skipped.'.format(identifier))


if __name__ == "__main__":
    default_filename = 'identifier_index.json'

    # Start up.
    updater_obj = IdentifierSPARQLUpdater(default_filename)

    # Write file.
    updater_obj.dump(default_filename)
