from fol import Literal, Predicate, Variable, Constant
from background_knowledge.pandas_bk import PandasBackgroundKnowledge
from prover import Prover


def test_prover():
    facts = [
        "actor(john).",
        "actor(maria).",
        "director(isaac).",
        "movie(movie1, john).",
        "movie(movie1, isaac).",
    ]
    bk = PandasBackgroundKnowledge([], [], facts)

    prover = Prover(bk.facts)
    result = prover.prove(
        {"A": ["john"], "B": ["isaac"]},
        [
            Literal(Predicate("actor"), [Variable("A")]),
            Literal(Predicate("director"), [Variable("B")]),
            Literal(Predicate("movie"), [Variable("C"), Variable("A")]),
            Literal(Predicate("movie"), [Variable("C"), Variable("B")]),
        ],
    )
    assert result
    result = prover.prove(
        {"A": ["john"], "B": ["maria"]},
        [
            Literal(Predicate("actor"), [Variable("A")]),
            Literal(Predicate("director"), [Variable("B")]),
            Literal(Predicate("movie"), [Variable("C"), Variable("A")]),
            Literal(Predicate("movie"), [Variable("C"), Variable("B")]),
        ],
    )
    assert not result
    result = prover.prove(
        {"A": ["john"], "B": ["isaac"]},
        [
            Literal(Predicate("actor"), [Variable("A")]),
            Literal(Predicate("director"), [Variable("B")]),
            Literal(Predicate("movie"), [Variable("_"), Variable("A")]),
            Literal(Predicate("movie"), [Variable("_"), Variable("B")]),
        ],
    )
    assert result
    result = prover.prove(
        {"A": ["john"], "B": ["isaac"]},
        [
            Literal(Predicate("actor"), [Variable("A")]),
            Literal(Predicate("director"), [Variable("B")]),
            Literal(Predicate("movie"), [Constant("movie1"), Variable("A")]),
            Literal(Predicate("movie"), [Constant("movie1"), Variable("B")]),
        ],
    )
    assert result
