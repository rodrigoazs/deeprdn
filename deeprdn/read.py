import re
from deeprdn.fol import Variable, Constant, Literal, Predicate, HornClause


def read_horn_clause_from_string(clause_string):
    ret = re.sub("(\/\*[a-zA-Z0-9\s\#\=]*\*\/)", "", clause_string)
    match = re.match(
        '\(([a-zA-Z0-9\(\),\s\_\."\-]*):-([a-zA-Z0-9\(\),\s\_\."]*)\!*\)\.', ret
    )
    if match:
        head = match.groups()[0].strip()
        tail = match.groups()[1].strip()
        if tail:
            tail = tail[:-1] if tail[-1] == "," else tail
        # assert matched correctly
        # accepts "!)."
        if not len(tail) and len(ret.split(":-")[1].strip()) > 3:
            raise Exception(
                'Could not identify horn clause from string "{}".'.format(clause_string)
            )
        return head, tail
    match = re.match('([a-zA-Z0-9\(\),\s\_\."\-]*)\s*\.', ret)
    if match:
        head = match.groups()[0].strip()
        tail = ""
        return head, tail
    raise Exception(
        'Could not identify horn clause from string "{}".'.format(clause_string)
    )


def read_literals_from_string(clause_string):
    literals = re.findall('([a-zA-Z0-9]*)\(([a-zA-Z0-9,\s\_"]*)\)', clause_string)
    for i in range(len(literals)):
        predicate = Predicate(literals[i][0])
        arguments = re.sub("\s", "", literals[i][1]).split(",")
        for j in range(len(arguments)):
            if re.match('"[a-zA-Z0-9]*"', arguments[j]):
                arguments[j] = Constant(arguments[j])
            else:
                arguments[j] = Variable(arguments[j])
        literals[i] = Literal(predicate, arguments)
    return literals


def extract_weight_from_string(literal_string):
    predicate, *arguments, weight = re.findall('([a-zA-Z0-9"\.\-\_]+)', literal_string)
    weight = float(weight)
    literal = "{}({})".format(predicate, ", ".join(arguments))
    return weight, literal


def get_horn_clause_from_string(clause_string):
    head, tail = read_horn_clause_from_string(clause_string)
    weight, head = extract_weight_from_string(head)
    head = read_literals_from_string(head)
    tail = read_literals_from_string(tail)
    clause = HornClause(head[0], tail, weight)
    return clause


def get_trees(tree_list):
    model = []
    for tree in tree_list:
        clauses = tree.split("\n")
        horn_clauses = []
        for clause in clauses:
            # non clause cases
            if (
                not len(clause)
                or clause.startswith("setParam")  # noqa: W503
                or clause.startswith("useStdLogicVariables")  # noqa: W503
                or clause.startswith("usePrologVariables")  # noqa: W503
            ):
                continue
            horn_clauses.append(get_horn_clause_from_string(clause))
        model.append(horn_clauses)
    return model
