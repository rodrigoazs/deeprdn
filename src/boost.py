from srlearn import Database
from srlearn.rdn import BoostedRDN
from prover.prover import Prover
from read_model import get_trees


class VectorBoostedRDN(BoostedRDN):
    def __init__(
        self,
        background=None,
        target="None",
        n_estimators=10,
        node_size=2,
        max_tree_depth=3,
        # neg_pos_ratio=2,
    ):
        super().__init__(
            background=background,
            target=target,
            n_estimators=n_estimators,
            node_size=node_size,
            max_tree_depth=max_tree_depth,
            # neg_pos_ratio=neg_pos_ratio,
        )

    def get_proved_vector(self, database):
        prover = Prover(
            database.pos,
            database.neg,
            database.facts
        )
        trees = get_trees(self.estimators_)
        result = []
        for data in (prover.pos, prover.neg):
            for _, row in data[self.target].iterrows():
                sample = row.values.tolist()
                vec = self._get_proved_sample_vector(prover, trees, sample)
                result.append(vec)
        return result

    def _get_proved_sample_vector(self, prover, trees, sample):
        sample_vector = []
        for tree in trees:
            vector = [0.0] * len(tree)
            for j, clause in enumerate(tree):
                head_mapping = {}
                for i, argument in enumerate(clause.head.arguments):
                    if argument.name != "_":
                        head_mapping[argument.name] = [sample[i]]
                result = prover.prove(head_mapping, clause.tail)
                if result:
                    vector[j] = 1.0
                    break
            sample_vector.extend(vector)
        return sample_vector

    

