from backend.annomathtex.views.helper_classes.token_clicked_handler import TokenClickedHandler


class AnnoMathTexEvaluationHandler:
    """
    This class employs the inbuilt AnnoMathTex instance for recommendation retrieval via HTTP GET requests in api.py.
    """

    def __init__(self, input_type, api_input):
        """
        Prepares an item dictionary for correct employment of recommendation retrieval by given identifier
        or formula from HTTP GET in api.py via AnnoMathTex TokenClickedHandler Class.

        :param input_type: requested index type by api.py as a string
        :param api_input: identifier/formula input from HTTP GET request in api.py
        """

        self.input_type = input_type
        self.input = api_input

        self.annomathtex_item = {
            'action': {'getRecommendations': ''},
            'searchString': {},
            'tokenType': {},
            'uniqueId': {'0---0': ''},
            'mathEnv': {'dummy': 'dummy'},
            'annotations': 'none'
            }

        if self.input_type == 'identifier':
            self.annomathtex_item['searchString'] = {self.input: ''}
            self.annomathtex_item['tokenType'] = {'Identifier': ''}

        elif self.input_type == 'formula':
            # split the formula at '=' position for AnnoMathTex retrieval
            try:
                self.formula_identifier_explained = self.input.split('=', 1)[0]
                self.formula_identifier_explaining = self.input.split('=', 1)[1]
            except:
                pass

            self.annomathtex_item['searchString'] = {self.formula_identifier_explained:
                                                     self.formula_identifier_explaining}
            self.annomathtex_item['tokenType'] = {'Formula': ''}
            self.annomathtex_item['mathEnv'] = {'dummy': self.input}

        self.response, self.source_dicts = TokenClickedHandler(self.annomathtex_item).get_recommendations()

    def annomathtex_retrieval(self, limit):
        """
        Reformatting of AnnoMathTex recommendation results.

        :param limit: number of returned results as an integer
        :return: results dictionary of AnnoMathTex retrieval for the given identifier/formula by their source
        """

        results = {}

        for self.source in self.source_dicts:
            results[self.source] = []

            for recommendation in self.source_dicts[self.source][:limit]:
                # Adds empty QID field if there is no
                try:
                    recommendation['qid']
                except KeyError as e:
                    if e.args[0] == 'qid':
                        recommendation['qid'] = ''
                    else:
                        return 'KeyError in get_results'

                results[self.source].append({'name': recommendation['name'], 'qid': recommendation['qid']})

        return results
