from read_model import (
    read_horn_clause_from_string,
    read_literals_from_string,
    extract_weight_from_string,
    get_horn_clause_from_string,
    get_trees,
)
from fol import Literal, Predicate, Variable, Constant, HornClause


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


def test_get_trees():
    trees_string = [
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.8581489350995084) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B)).\n(workedunder(A, B, -0.1418510649004877) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.14185106490048816) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.719473412210958) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar2, A), movie(UniqueVar2, B)).\n(workedunder(A, B, -0.12544463852839138) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.12544463852839197) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.06245298988159939) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar19, A), movie(UniqueVar19, B)).\n(workedunder(A, B, -0.04109376153604857) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.041093761536048504) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.05889459763950667) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar20, A), movie(UniqueVar20, B), !).\n(workedunder(A, B, -0.039504650587338576) :-  /* #neg=29 */ actor(A), director(B), !).\n(workedunder(_, _, -0.03950465058733851) :-  /* #neg=308 */ !).\n",  # noqa
    ]
    trees = get_trees(trees_string)
    assert len(trees) == 4
    assert len(trees[0]) == 3
    assert type(trees[0]) == list
    assert type(trees[0][0]) == HornClause
