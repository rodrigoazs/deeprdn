import re
from fol import Variable, Constant, Literal, Predicate, HornClause


def read_horn_clause_from_string(clause_string):
    ret = re.sub("(\/\*[a-zA-Z0-9\s\#\=]*\*\/)", "", clause_string)
    match = re.match(
        '\(([a-zA-z0-9\(\),\s\_\."]*):-([a-zA-z0-9\(\),\s\_\."]*)\)\.', ret
    )
    if match:
        head = match.groups()[0].strip()
        tail = match.groups()[1].strip()
        return head, tail
    match = re.match('([a-zA-z0-9\(\),\s\_\."\-]*)\s*\.', ret)
    if match:
        head = match.groups()[0].strip()
        tail = ""
        return head, tail


def read_literals_from_string(clause_string):
    literals = re.findall('([a-zA-Z0-1]*)\(([a-zA-z0-9,\s\_"]*)\)', clause_string)
    for i in range(len(literals)):
        predicate = Predicate(literals[i][0])
        arguments = re.sub("\s", "", literals[i][1]).split(",")
        for j in range(len(arguments)):
            if re.match('"[a-zA-Z0-1]*"', arguments[j]):
                arguments[j] = Constant(arguments[j])
            else:
                arguments[j] = Variable(arguments[j])
        literals[i] = Literal(predicate, arguments)
    return literals


def extract_weight_from_string(literal_string):
    predicate, *arguments, weight = re.findall('([a-zA-z0-9"\.\-]+)', literal_string)
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
