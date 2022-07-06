import json
import logging
import os
import time

from backend.annomathtex.recommendation.math_sparql import MathSparql
from backend.annomathtex.recommendation.sparql_queries import *

logging.basicConfig(level=logging.INFO)
update_identifier_logger = logging.getLogger(__name__)


class IdentifierSPARQLUpdater:
    """
    This class reads the extracted list of already known (local) identifiers and re-queries via SPARQL.
    If there's a new result (previous value is N/A) or a different QID the index is updated.
    """

    def __init__(self, local_file='identifier_index.json'):

        self.identifier_query = identifier_query    # Use the SPARQL-Query already supplied by AnnoMathTex
        self.wikidata_online_dict = {}
        self.local_dict = {}
        self.n_updated_total = 0
        self.filename = local_file  # Default-Filename
        self.TIME_BEETWEEN_QUERY = 2;


        # Open JSON-File
        path = os.path.join(self.filename)
        with open(path, 'r', encoding='utf-8') as f:
            self.local_dict = json.load(f)

        for identifier in self.local_dict:

            # Workaround: Only use identifiers of length one. (SPARQL-queries are problematic, especially containing LaTeX-content.
            # Possible solution: Use regex to ensure correct format of identifier or switch between queries
            # update_identifier_logger.info('Handling identifier: {}'.format(identifier))
            if len(identifier) == 1:
                # Add result to temporary dict
                self.wikidata_online_dict[identifier] = self.query(identifier)

                # Avoid firing too many requests in a short period of time (HTTP 429)
                time.sleep(self.TIME_BEETWEEN_QUERY)

                # Query done, compare with (local) file content and integrate new data into local dict
                self.compare(identifier)

        update_identifier_logger.info('Updated a TOTAL of {} QID to index.'.format(self.n_updated_total))

    def dump(self):
        """
        Method to write out the JSON-Output-File.
        TODO: Use variable for filename
        """
        with open('identifier_index_new.json', 'w') as f:
            json.dump(self.local_dict, f, ensure_ascii=False, indent=4)
            update_identifier_logger.info('Wrote to file. END.')


    def query(self, identifier):
        """
        Helper-Function for SPARQL-Query. Not sure if necessary.
        """
        try:
            identifier_result = MathSparql().query(self.identifier_query, identifier)
        except Error as e:
            update_identifier_logger.error()

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
                if dict_item.get('wikidata1Results') != None:
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
                    print('UPDATE : {}'.format(diff))

                    # Count the number of updated items
                    n_updated_identifiers = n_updated_identifiers + len(diff)

                    # Copy new online elements (key = QID) into local results
                    for new_qid in diff:
                        dict_item['wikidata1Results'].append(online_elements[new_qid])

                    update_identifier_logger.info(
                        'Update: ADDED {} QIDs ({}) to identifier {} from Wikidata'.format(n_updated_identifiers, diff,
                                                                                           identifier))
                    self.n_updated_total = self.n_updated_total + n_updated_identifiers


if __name__ == "__main__":

    # Start up.
    updater_obj = IdentifierSPARQLUpdater('identifier_index.json')

    # Write file.
    updater_obj.dump()

