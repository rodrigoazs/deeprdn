from background_knowledge.pandas_bk import PandasBackgroundKnowledge


def test_background_knowledge():
    pos = ["teste(teste2, teste3)."]
    facts = [
        "teste2(teste2, teste3).",
        "teste3(teste2, teste3, teste4).",
        "teste3(teste2, teste3, teste4).",
        "teste3(teste2, teste3, teste4).",
    ]
    bk = PandasBackgroundKnowledge(pos, [], facts)
    assert bk.pos["teste"].shape == (1, 2)
    assert bk.pos["teste"].columns[1] == "teste_1"
    assert bk.facts["teste2"].shape == (1, 2)
    assert bk.facts["teste3"].shape == (3, 3)
    assert bk.facts["teste2"].columns[0] == "teste2_0"
    assert bk.facts["teste3"].columns[1] == "teste3_1"
