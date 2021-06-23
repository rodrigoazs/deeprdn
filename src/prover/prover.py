import pandas as pd
from prover.base import BaseProver
from fol import Variable, Constant


class Prover(BaseProver):
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

    def prove(self, mapping, clause):
        last_mapping = mapping.copy()
        for literal in clause:
            literal_mapping = {}
            for i, argument in enumerate(literal.arguments):
                if type(argument) == Constant:
                    literal_mapping[i] = [argument.name]
                if type(argument) == Variable:
                    if (
                        argument.name != "_"
                        and last_mapping.get(argument.name) is not None  # noqa: W503
                    ):
                        literal_mapping[i] = last_mapping.get(argument.name)
            df = self.facts[literal.predicate.name]
            for i, mapping in literal_mapping.items():
                df = df[df["{}_{}".format(literal.predicate.name, i)].isin(mapping)]
            if not len(df):
                return False
            for i, argument in enumerate(literal.arguments):
                if type(argument) == Variable and argument.name != "_":
                    last_mapping[argument.name] = df[
                        "{}_{}".format(literal.predicate.name, i)
                    ].values.tolist()
        return True
