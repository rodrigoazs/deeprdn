from deeprdn.model import DeepRDN, NotFittedError
from srlearn import Background, Database
from unittest.mock import Mock
import numpy as np
import pytest


def test_model_set_estimator():
    model = DeepRDN(estimator=lambda x: (1, x))
    result = model._get_estimator(0)
    assert result == (1, 0)


def test_model_number_of_clauses_and_cycles():
    bk = Background(
        number_of_clauses=1,
        number_of_cycles=2
    )
    model = DeepRDN(
        background=bk,
        number_of_clauses=10,
        number_of_cycles=15
    )
    assert model.background.number_of_clauses == 10
    assert model.background.number_of_cycles == 15


def test_model_assert_not_fitted_error():
    bk = Background(
        number_of_clauses=1,
        number_of_cycles=2
    )
    model = DeepRDN(
        background=bk,
        number_of_clauses=10,
        number_of_cycles=15
    )
    with pytest.raises(NotFittedError):
        model.predict_proba(None)

def test_model_raises_value_error_in_check_params():
    model = DeepRDN(
        background=None,
        target=None,
        number_of_clauses=0,
        number_of_cycles=-1
    )
    with pytest.raises(ValueError):
        model._check_params()


def test_model_get_x():
    bk = Background(
        number_of_clauses=1,
        number_of_cycles=2
    )
    model = DeepRDN(
        background=bk,
        target="test",
        number_of_clauses=1,
        number_of_cycles=1,
    )
    tree_mock = Mock()
    tree_mock.get_proved_vector.return_value = np.array([[1, 0, 0], [1, 0, 0]])
    model.trees_ = [tree_mock, tree_mock]
    result = model._get_X(None)
    assert result.shape == (2, 6)


def test_model_filter_database():
    db = Database()
    db.facts = [
        'test(a,b).',
        'test2(a,b).',
        'test3(a,b).',
        'test4(a,b).',
        'test5(a,b).',
        'test6(a,b).',
        'test7(a,b).',
        'test8(a,b).',
        'test9(a,b).',
        'test10(a,b).',
    ]
    model = DeepRDN(
        predicate_ratio=0.9,
        sample_ratio=1.0,
    )
    new_db = model._filter_database(db)
    assert len(new_db.facts) == 9
    model = DeepRDN(
        predicate_ratio=1.0,
        sample_ratio=0.5,
    )
    new_db = model._filter_database(db)
    assert len(new_db.facts) == 5


def test_model_fit(monkeypatch):
    class VectorMock(Mock):
        def get_proved_vector(self, database):
            return np.array([[1, 0, 0], [1, 0, 0]])

    vector_mock = VectorMock()
    monkeypatch.setattr('deeprdn.model.VectorBoostedRDN', vector_mock)
    vector_sequential = Mock()
    monkeypatch.setattr('deeprdn.model.Sequential', vector_sequential)
    db = Database()
    bk = Background()
    model = DeepRDN(
        background=bk,
        target="test",
        sample_ratio=1.0,
        predicate_ratio=1.0,
    )
    model.fit(db)
