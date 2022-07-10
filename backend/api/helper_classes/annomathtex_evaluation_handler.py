from backend.annomathtex.views.helper_classes.token_clicked_handler import TokenClickedHandler


class AnnoMathTexEvaluationHandler:

    def __init__(self, input_type, api_input):
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
             # splitting the formula at '='
            try:
                self.formula_identifier_explained = self.input.split('=', 1)[0]
                self.formula_identifier_explaining = self.input.split('=', 1)[1]
            except:
                return 'Error: No formula provided'

            self.annomathtex_item['searchString'] = {self.formula_identifier_explained:
                                                     self.formula_identifier_explaining}
            self.annomathtex_item['tokenType'] = {'Formula': ''}
            self.annomathtex_item['mathEnv'] = {'dummy': self.input}

        self.response, self.source_dicts = TokenClickedHandler(self.annomathtex_item).get_recommendations()

    def annomathtex_retrieval(self, limit):
        results = {}

        for self.source in self.source_dicts:
            results[self.source] = []

            for recommendation in self.source_dicts[self.source][:limit]:
                try:
                    recommendation['qid']
                except KeyError as e:
                    if e.args[0] == 'qid':
                        recommendation['qid'] = ''
                    else:
                        return 'KeyError in get_results'

                results[self.source].append({'name' : recommendation['name'], 'qid':recommendation['qid']})

        return results
