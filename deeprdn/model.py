from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from deeprdn.boost import VectorBoostedRDN
from srlearn import Database, Background
import numpy as np
import random
import re


class DeepRDN:
    def __init__(
        self,
        background=None,
        target="None",
        n_estimators=50,
        node_size=2,
        number_of_clauses=4,
        max_tree_depth=2,
        n_boost_estimators=1,
        predicate_prob=0.5,
        sample_prob=0.5,
    ):
        self.background = background
        if type(self.background) == Background:
            self.background.number_of_clauses = number_of_clauses
        self.target = target
        self.n_estimators = n_estimators
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.n_boost_estimators = n_boost_estimators
        self.predicate_prob = predicate_prob
        self.sample_prob = sample_prob
        self.estimators_ = []
        self.stacking_ = None

    def fit(self, database):
        for i in range(self.n_estimators):
            estimator = VectorBoostedRDN(
                background=self.background,
                target=self.target,
                n_estimators=self.n_boost_estimators,
                node_size=self.node_size,
                max_tree_depth=self.max_tree_depth,
            )
            estimator.fit(self._filter_database(database))
            self.estimators_.append(estimator)
        X_train = self._get_X(database)
        Y_train = self._get_y(database)
        model = Sequential()
        model.add(Dropout(0.5, input_shape=(X_train.shape[1],)))
        model.add(Dense(10))
        model.add(Dropout(0.5))
        model.add(Dense(10))
        model.add(Dense(2, activation="softmax"))
        model.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        model.fit(X_train, Y_train, epochs=25, batch_size=32, verbose=0)
        self.stacking_ = model

        return self

    def predict_proba(self, database):
        X_pred = self._get_X(database)
        return self.stacking_.predict(X_pred)[:, 1]

    def _get_X(self, database):  # noqa: N802
        X = np.concatenate(
            [estimator.get_proved_vector(database) for estimator in self.estimators_],
            axis=1,
        )
        return X

    def _get_y(self, database):
        y = np.array(
            [[0.0, 1.0] for _ in range(len(database.pos))]
            + [[1.0, 0.0] for _ in range(len(database.neg))]
        )
        return y

    def _filter_database(self, database):
        if self.predicate_prob == 1.0 and self.sample_prob == 1.0:
            return database
        facts = []
        predicates = {}
        for fact in database.facts:
            literals = re.match("([a-zA-Z0-9\_]*)\([a-zA-Z0-9\,\s\_]*\)\.", fact)
            predicate = literals.groups()[0]
            if predicate not in predicates:
                predicates[predicate] = (
                    True if random.random() < self.predicate_prob else False
                )
            if predicates[predicate] and random.random() < self.sample_prob:
                facts.append(fact)
        new_database = Database()
        new_database.pos = database.pos
        new_database.neg = database.neg
        new_database.facts = facts
        return new_database
