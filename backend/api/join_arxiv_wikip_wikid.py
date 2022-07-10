import os
import json


from backend.annomathtex.recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from backend.annomathtex.recommendation.static_wikidata_handler import StaticWikidataHandler


class ArXivReader:
    """
    This class reads the extracted list of arXiv identifiers and returns a dictionary of the results, with respect to
    the queried identifier. The queried identifier being an identifier clicked by the user through the frontend.
    """
    def __init__(self):
        self.evaluation_file = self.read_file()
        self.evaluation_dict = self.create_item_dict()

    def read_file(self):
        """
        Read the file containing the extacted arXiv identifiers.
        :return: The read file as a string, with some unnecessary characters removed.
        """
        #path = os.path.join(os.getcwd(), 'annomathtex', 'recommendation', 'evaluation_files', 'Evaluation_list_all.rtf')
        path = os.path.join('../annomathtex/recommendation/evaluation_files/Evaluation_list_all.rtf')
        with open(path, 'r') as f:
            file = f.read()
        file = file.replace('\par', '\n')
        return file.split('\n\n\n\n')[1:]

    def create_item_dict(self):
        """
        Create a dictionary of the file that was parsed by the method read_file().
        :return: The dictionary that was created.
        """
        item_dict = {}
        for item in self.evaluation_file:
            item_parts = item.split('\n\n')
            if len(item_parts) >= 11:
                if len(item_parts) == 12:
                    item_parts = item_parts[:-1]
                identifier = item_parts[0].replace('\\', '')
                item_dict[identifier] = list(
                    map(
                        lambda x: {
                            #'name': x.split()[0][:-1]
                            'name': x.split()[0][:-1].lower(),
                            'value': x.split()[1][:].lower()
                        },
                        item_parts[1:]
                    )
                )
        return item_dict


def pp(dict_list, source):
    """
    post process: add QID and fill to recommendations limit
    :param dict_list: ditionary list of recommendations from one source
    :return:
    """

    def add_qid_all_math(r, in_source):

        path = os.path.join('../annomathtex/recommendation/evaluation_files/math_wikidata_items.json')
        with open(path, 'r') as f:
            file = f.read()

        all_math_items = json.loads(file, encoding = "utf-8")

        if source not in ['wikidata1Results', 'wikidata2Results']:
            if source in ['wikipediaEvaluationItems']:
                r['name'] = r.pop('description')
                r.pop('identifier')
                r.pop('wikimedia_link')

            name = r['name']

            if name in all_math_items:
                r['qid'] = all_math_items[name]
            else:
                r['qid'] = 'N/A'
        else:
            r.pop('link')
        r['name'] = r['name'].replace("\'", '__APOSTROPH__')
        return r

    for identifier in dict_list[0]:
        # dict_list_identifier = list(map(add_qid_all_math, dict_list[0]))
        dict_list_identifier = list(map(lambda d: add_qid_all_math(d, in_source = source), dict_list[0][identifier]))


def recommendations_dict_change_order(rd):

    rdf = {}

    for source in rd:
        for identifier in rd[source][0]:

            if rd[source][0][identifier]:

                try:
                    rdf[identifier]
                except KeyError:
                    rdf[identifier] = []

                rdf[identifier].append({source: recommendations_dict[source][0][identifier]})

    return rdf


if __name__ == "__main__":

    ArXiV_dict = ArXivReader().evaluation_dict
    wikipediaEvaluationItems_dict = WikipediaEvaluationListHandler().read_file()
    wikidata1Results_dict = StaticWikidataHandler().read_identifier_file()

    recommendations_dict = {'arXivEvaluationItems': [ArXiV_dict],
                            'wikipediaEvaluationItems': [wikipediaEvaluationItems_dict],
                            'wikidata1Results': [wikidata1Results_dict],
                            # 'wikidata2Results': [],
                            # 'wordWindow': [],
                            # 'formulaConceptDB': [],
                            # 'manual': []
                            }

    recommendations_dict_pp_loc = dict(map(lambda kv: (kv[0], pp(kv[1], kv[0])), recommendations_dict.items()))

    recommendations_dict_formatted = recommendations_dict_change_order(recommendations_dict)

    with open('../annomathtex/recommendation/evaluation_files/identifier_index.json', 'w', encoding='utf-8') as f:
        json.dump(recommendations_dict_formatted, f, ensure_ascii=False, indent=4)



