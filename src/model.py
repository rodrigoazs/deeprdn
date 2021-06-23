from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from boost import VectorBoostedRDN
import numpy as np


class NeuralRDN:
    def __init__(
        self,
        background=None,
        target="None",
        n_estimators=10,
        node_size=2,
        max_tree_depth=3,
        n_boost_estimators=1,
    ):
        self.background = background
        self.target = target
        self.n_estimators = n_estimators
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.n_boost_estimators = n_boost_estimators
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
            estimator.fit(database)
            self.estimators_.append(estimator)
        X_train = self._get_X(database)
        Y_train = self._get_y(database)
        model = Sequential()
        model.add(Dense(5, input_shape=(X_train.shape[1],)))
        model.add(Dense(5))
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
