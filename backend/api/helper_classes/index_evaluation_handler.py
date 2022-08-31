import os
import json

from ..formula_index_retrieval import employ_index


class IndexEvaluationHandler:
    """
    This class evaluates the identifier index provided in /dataset/identifier_index.json or formulae and QID indices via
    the formula_index_retrieval.py helper script in /api for recommendation retrieval via HTTP GET requests in api.py.
    """
    def __init__(self, index_type):
        """
        Check which recommendation index type is requested (identifier/formulae) and read the corresponding index file
        via read_index_file function.

        :param index_type: requested index type by api.py as a string
        """
        self.index_type = index_type
        if self.index_type == 'identifier':
            self.identifier_dict = self.read_index_file()
        elif self.index_type == 'formula':
            self.formula_index, self.qid_index = self.read_index_file()

    def read_index_file(self):
        """
        Read the file containing the identifier or formula and corresponding QID index.

        :return: The read file(s) as a string.
        """
        if self.index_type == 'identifier':
            # load identifier index
            path = os.path.join('dataset', 'identifier_index.json')
            with open(path, 'r') as json_file:
                identifier_dict = json.load(json_file)
            return identifier_dict
        elif self.index_type == 'formula':
            # load formula index
            path = os.path.join('dataset')
            with open(os.path.join(path, 'formula_string_index.json'), 'r') as f:
                formula_index = json.load(f)
            # load qid index
            with open(os.path.join(path, 'formula_qid_index.json'), 'r') as f:
                qid_index = json.load(f)
            return formula_index, qid_index

    def check_identifier_index(self, symbol, limit):
        """
        Checks the identifier index for requested recommendations, optionally removes value and item_description from
        entries and returns the results by their source.

        :param symbol: identifier symbol/name as a string
        :param limit: number of returned results as an integer
        :return: results dictionary for the given identifier symbol by their source
        """

        results = {}

        symbol = symbol if symbol in self.identifier_dict else '\\{}'.format(symbol)
        if symbol in self.identifier_dict:
            identifier_dict_symbol = self.identifier_dict[symbol]
            for source_dict in identifier_dict_symbol:
                for source, entries in source_dict.items():
                    for positions in entries:
                        try:
                            positions.pop('value')
                        except:
                            pass

                        try:
                            positions.pop('item_description')
                        except:
                            pass
                    results[source] = entries[:limit]
        return results

    def check_formula_index(self, formula, limit):
        """
        Checks the formulae index for requested recommendations and adds QID's by using the employ_index function
        in /api/formula_index_retrieval.py helper script, removes score for wikidata1Results source
        and returns the results.

        :param formula: formula as a string
        :param limit: number of returned results as an integer
        :return: results dictionary for the given formula by their source
        """

        results = employ_index(formula, limit, self.formula_index, self.qid_index)
        for result in results['wikidata1Results']:
            result.pop('score')

        return results


