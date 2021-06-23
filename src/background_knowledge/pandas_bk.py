import pandas as pd
from background_knowledge.base import BackgroundKnowledgeBase


class PandasBackgroundKnowledge(BackgroundKnowledgeBase):
    def __init__(self, pos, neg, facts):
        super().__init__(pos, neg, facts)

    def _compile(self, data):
        data_dict = {}
        for item in data:
            predicate, arguments = self._get_literal(item)
            data_dict.setdefault(predicate, []).append(arguments)
        for key, value in data_dict.items():
            data_dict[key] = pd.DataFrame(
                value,
                columns=["{}_{}".format(key, i) for i in range(len(value[0]))],
            )
        return data_dict
