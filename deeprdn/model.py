from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from deeprdn.boost import VectorBoostedRDN
from srlearn import Database, Background
from typing import Callable
import numpy as np
import random
import re


class DeepRDN:
    """Deep Relational Network Dependency Estimator
    """
    def __init__(
        self,
        background: Background = None,
        target: str = "None",
        n_bagging_trees: int = 50,
        n_boosting_trees: int = 1,
        node_size: int = 2,
        number_of_clauses: int = 4,
        number_of_cycles: int = 100,
        max_tree_depth: int = 2,
        predicate_prob: float = 0.5,
        sample_prob: float = 0.5,
        estimator: Callable = None,
    ):
        """Initialize a DeepRDN

        Args:
            background (Background, optional): Background knowledge with respect
                to the database. Defaults to None.
            target (str, optional): Target predicate to learn. Defaults to "None".
            n_bagging_trees (int, optional): Number of trees to fit as bagging.
                Each bagging provides n_boosting_trees boosting trees. Defaults to 50.
            n_boosting_trees (int, optional): Number of trees to fit as boosting.
                Each boosting provides around number_of_clauses clauses as input
                parameter. Defaults to 1.
            node_size (int, optional): Maximum number of literals in each node.
                Defaults to 2.
            number_of_clauses (int, optional): Maximum number of clauses in the
                tree (i.e. maximum number of leaves). Defaults to 4.
            number_of_cycles (int, optional): Maximum number of times the code
                will loop to learn clauses, increments even if no new clauses are
                learned. Defaults to 100.
            max_tree_depth (int, optional): Maximum number of nodes from root to
                leaf (height) in the tree. Defaults to 2.
            predicate_prob (float, optional): Probability of considering a predicate
                in the search space. Defaults to 0.5.
            sample_prob (float, optional): Probability of considering a sample when
                training. Defaults to 0.5.
            estimator (Callable, optional): A function that receives a numpy array
            as feature vector of the target samples and returns a classifier and its
            parameters to call the fit method. Defaults to None.
        """
        self.background = background
        self.target = target
        self.n_bagging_trees = n_bagging_trees
        self.n_boosting_trees = n_boosting_trees
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.predicate_prob = predicate_prob
        self.sample_prob = sample_prob
        self.trees_ = None
        self.estimator_ = None
        self._get_estimator = estimator if estimator else self._get_neural_estimator

        if type(self.background) == Background:
            self.background.number_of_clauses = number_of_clauses
            self.background.number_of_cycles = number_of_cycles

    def _check_params(self):
        if self.target == "None":
            raise ValueError("target must be set, cannot be {0}".format(self.target))
        if not isinstance(self.target, str):
            raise ValueError(
                "target must be a string, cannot be {0}".format(self.target)
            )
        if self.background is None:
            raise ValueError(
                "background must be set, cannot be {0}".format(self.background)
            )
        if not isinstance(self.background, Background):
            raise ValueError(
                "background should be a srlearn.Background object, cannot be {0}".format(  # noqa: E501
                    self.background
                )
            )
        if not isinstance(self.n_bagging_trees, int) or isinstance(
            self.n_bagging_trees, bool
        ):
            raise ValueError(
                "n_bagging_trees must be an integer, cannot be {0}".format(
                    self.n_bagging_trees
                )
            )
        if self.n_bagging_trees <= 0:
            raise ValueError(
                "n_bagging_trees must be greater than 0, cannot be {0}".format(
                    self.n_bagging_trees
                )
            )
        if not isinstance(self.n_bagging_trees, int) or isinstance(
            self.n_boosting_trees, bool
        ):
            raise ValueError(
                "n_boosting_trees must be an integer, cannot be {0}".format(
                    self.n_boosting_trees
                )
            )
        if self.n_boosting_trees <= 0:
            raise ValueError(
                "n_boosting_trees must be greater than 0, cannot be {0}".format(
                    self.n_boosting_trees
                )
            )

    def _check_is_fitted(self):
        if self.estimator_ is None or self.trees_ is None:
            raise NotFittedError

    def fit(self, database: Database):
        """Learn structure and parameters

        Args:
            database (Database): Database containing examples and facts.
        """
        # check parameters
        self._check_params()

        # fit bagging trees
        self.trees_ = []
        for i in range(self.n_bagging_trees):
            tree = VectorBoostedRDN(
                background=self.background,
                target=self.target,
                n_estimators=self.n_boosting_trees,
                node_size=self.node_size,
                max_tree_depth=self.max_tree_depth,
            )
            tree.fit(self._filter_database(database))
            self.trees_.append(tree)

        # compile feature and target vectors
        X_train = self._get_X(database)
        Y_train = self._get_y(database)
        
        # get estimator and fit it
        model, params = self._get_estimator(X_train)
        model.fit(X_train, Y_train, **params)
        self.estimator_ = model

        return self

    def predict_proba(self, database):
        self._check_is_fitted()
        X_pred = self._get_X(database)
        return self.estimator_.predict(X_pred)[:, 1]

    def _get_X(self, database):  # noqa: N802
        X = np.concatenate(
            [tree.get_proved_vector(database) for tree in self.trees_],
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

    def _get_neural_estimator(self, X_train):
        # define the estimator
        model = Sequential()
        model.add(Dropout(0.5, input_shape=(X_train.shape[1],)))
        model.add(Dense(10))
        model.add(Dropout(0.5))
        model.add(Dense(10))
        model.add(Dense(2, activation="softmax"))
        model.compile(
            loss="categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"]
        )

        # define training params
        params = {
            'epochs': 25,
            'batch_size': 32,
            'verbose': 0,
        }

        return model, params


class NotFittedError(ValueError, AttributeError):
    pass
