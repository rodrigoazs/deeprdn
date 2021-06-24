from deeprdn.read import (
    read_horn_clause_from_string,
    read_literals_from_string,
    extract_weight_from_string,
    get_horn_clause_from_string,
    get_trees,
)
from deeprdn.fol import Literal, Predicate, Variable, Constant, HornClause


def test_read_horn_clause_from_string():
    clause_string = "(workedunder(A, B, 0.8581489350995084) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B))."  # noqa
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(A, B, 0.8581489350995084)"
    assert tail == "actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B)"
    clause_string = "workedunder(_, _, -0.14185106490048816) /* #neg=308 */ ."
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(_, _, -0.14185106490048816)"
    assert tail == ""
    clause_string = "(workedunder(A, B, -0.1418510649004877) :-  /* #neg=29 */ actor(A), director(B))."
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(A, B, -0.1418510649004877)"
    assert tail == "actor(A), director(B)"
    clause_string = "(workedunder(_, _, -0.03950465058733851) :-  /* #neg=308 */ !)."
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(_, _, -0.03950465058733851)"
    assert tail == ""
    clause_string = "(workedunder(A, B, -0.039504650587338576) :-  /* #neg=29 */ actor(A), director(B), !)."
    head, tail = read_horn_clause_from_string(clause_string)
    assert head == "workedunder(A, B, -0.039504650587338576)"
    assert tail == "actor(A), director(B)"


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
    clause_string = "(workedunder(A, B, -0.1418510649004877) :-  /* #neg=29 */ actor(A), director(B))."
    clause = get_horn_clause_from_string(clause_string)
    assert clause.weight == -0.1418510649004877
    assert clause.head == Literal(
        Predicate("workedunder"), [Variable("A"), Variable("B")]
    )
    assert clause.tail == [
        Literal(Predicate("actor"), [Variable("A")]),
        Literal(Predicate("director"), [Variable("B")]),
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
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.5553664367462832) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar3, A), movie(UniqueVar3, B)).\n(workedunder(A, B, -0.1123163781936064) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.11231637819360686) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.41751358415831175) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar4, A), movie(UniqueVar4, B)).\n(workedunder(A, B, -0.10159632948783635) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.10159632948783649) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.3207118471601512) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar5, A), movie(UniqueVar5, B)).\n(workedunder(A, B, -0.09269127618926097) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.09269127618926054) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.2551722425694875) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar6, A), movie(UniqueVar6, B)).\n(workedunder(A, B, -0.0851847513883968) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.08518475138839678) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.2097577156325347) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar7, A), movie(UniqueVar7, B)).\n(workedunder(A, B, -0.07877675473109179) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.07877675473109143) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.17709649774527644) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar8, A), movie(UniqueVar8, B)).\n(workedunder(A, B, -0.07324622576333704) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.07324622576333696) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.1527438580936716) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar9, A), movie(UniqueVar9, B)).\n(workedunder(A, B, -0.06842697784420276) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.06842697784420296) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.1340070300080119) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar10, A), movie(UniqueVar10, B)).\n(workedunder(A, B, -0.06419184008202623) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.06419184008202625) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.11920380823128321) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar11, A), movie(UniqueVar11, B)).\n(workedunder(A, B, -0.060441948167738575) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.06044194816773883) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.10724508452246814) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar12, A), movie(UniqueVar12, B)).\n(workedunder(A, B, -0.0570993501883345) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.057099350188334355) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.0974011274550112) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar13, A), movie(UniqueVar13, B)).\n(workedunder(A, B, -0.054101797942008145) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.05410179794200828) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.0891675660630682) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar14, A), movie(UniqueVar14, B)).\n(workedunder(A, B, -0.05139901059016829) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.05139901059016858) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.08218604818271556) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar15, A), movie(UniqueVar15, B)).\n(workedunder(A, B, -0.04894994992783667) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.04894994992783642) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.07619570198076865) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar16, A), movie(UniqueVar16, B)).\n(workedunder(A, B, -0.04672080332836748) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.046720803328367526) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.07100250423444295) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar17, A), movie(UniqueVar17, B)).\n(workedunder(A, B, -0.04468346994743662) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.044683469947436556) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.06645938878746442) :-  /* #pos=337 */ director(B), actor(A), movie(UniqueVar18, A), movie(UniqueVar18, B)).\n(workedunder(A, B, -0.04281441025528358) :-  /* #neg=29 */ director(B), actor(A)).\nworkedunder(_, _, -0.04281441025528373) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.06245298988159939) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar19, A), movie(UniqueVar19, B)).\n(workedunder(A, B, -0.04109376153604857) :-  /* #neg=29 */ actor(A), director(B)).\nworkedunder(_, _, -0.041093761536048504) /* #neg=308 */ .\n",  # noqa
        "setParam: stringsAreCaseSensitive = true.\n\nusePrologVariables: true.\n\n\n(workedunder(A, B, 0.05889459763950667) :-  /* #pos=337 */ actor(A), director(B), movie(UniqueVar20, A), movie(UniqueVar20, B), !).\n(workedunder(A, B, -0.039504650587338576) :-  /* #neg=29 */ actor(A), director(B), !).\n(workedunder(_, _, -0.03950465058733851) :-  /* #neg=308 */ !).\n",  # noqa
    ]
    trees = get_trees(trees_string)
    assert len(trees) == 20
    assert len(trees[0]) == 3
    assert type(trees[0]) == list
    assert type(trees[0][0]) == HornClause
    assert (
        str(trees[0][0])
        == "0.8581489350995084 workedunder(A, B) :- actor(A), director(B), movie(UniqueVar1, A), movie(UniqueVar1, B)"
    )
    assert (
        str(trees[0][1])
        == "-0.1418510649004877 workedunder(A, B) :- actor(A), director(B)"
    )
    assert str(trees[0][2]) == "-0.14185106490048816 workedunder(_, _) :- "
