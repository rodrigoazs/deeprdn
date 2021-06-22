from read_model import (
    read_horn_clause_from_string,
    read_literals_from_string,
    extract_weight_from_string,
    get_horn_clause_from_string,
)
from fol import Literal, Predicate, Variable, Constant


def test_read_horn_clause_from_string():
    clause_string = "(workedunder(A, B, 0.8581489350995084) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B))."  # noqa
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(A, B, 0.8581489350995084)"
    assert tail == "actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B)"
    clause_string = "workedunder(_, _, -0.14185106490048816) /* #neg=308 */ ."
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(_, _, -0.14185106490048816)"
    assert tail == ""


def test_read_literals_from_string():
    clause_string = 'actor(A), director(B), movie(UniqueVar1, A), movie("const", B)'
    ret = read_literals_from_string(clause_string)
    assert ret[0] == Literal(Predicate("actor"), [Variable("A")])
    assert ret[2] == Literal(
        Predicate("movie"), [Variable("UniqueVar1"), Variable("A")]
    )
    assert ret[3] == Literal(Predicate("movie"), [Constant("const"), Variable("B")])
    clause_string = ""
    ret = read_literals_from_string(clause_string)
    assert len(ret) == 0


def test_extract_weight_from_string():
    literal_string = "workedunder(A, B, 0.8581489350995084)"
    weight, literal = extract_weight_from_string(literal_string)
    assert weight == 0.8581489350995084
    assert literal == "workedunder(A, B)"


def test_get_horn_clause_from_string():
    clause_string = "(workedunder(A, B, 0.8581489350995084) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B))."  # noqa
    clause = get_horn_clause_from_string(clause_string)
    assert clause.weight == 0.8581489350995084
    assert clause.head == Literal(
        Predicate("workedunder"), [Variable("A"), Variable("B")]
    )
    assert clause.tail == [
        Literal(Predicate("actor"), [Variable("A")]),
        Literal(Predicate("director"), [Variable("B")]),
        Literal(Predicate("movie"), [Variable("UniqueVar1"), Variable("A")]),
        Literal(Predicate("movie"), [Variable("UniqueVar1"), Variable("B")]),
    ]
    clause_string = "workedunder(_, _, -0.14185106490048816) /* #neg=308 */ ."
    clause = get_horn_clause_from_string(clause_string)
    assert clause.weight == -0.14185106490048816
    assert clause.head == Literal(
        Predicate("workedunder"), [Variable("_"), Variable("_")]
    )
    assert len(clause.tail) == 0
