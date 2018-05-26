# coding: utf8

import tabulate
import collections
from pathlib import Path


def summarize(corpus):
    gold = Path(corpus) / 'gold'
    inpt = Path(corpus) / 'input'
    entities = collections.Counter()
    relations = collections.Counter()
    sentences = 0

    input_files = {}
    b_files = {}
    c_files = {}

    for fp in inpt.glob('**/input_*'):
        input_files[fp.name] = fp

    files = len(input_files)

    for fp in input_files.values():
        sentences += len([l for l in fp.open() if l.strip()])

    for fp in gold.glob('**/output_B*'):
        b_files[fp.name] = fp

    for fp in b_files.values():
        entities.update([line.strip().split()[-1] for line in fp.open()])

    entities['total'] = sum(entities.values())

    for fp in gold.glob('**/output_C*'):
        c_files[fp.name] = fp

    for fp in c_files.values():
        relations.update([line.strip().split()[0] for line in fp.open()])

    relations['total'] = sum(relations.values())
    relations['relations'] = sum(relations[k] for k in 'part-of property-of is-a same-as'.split())
    relations['roles'] = sum(relations[k] for k in 'subject target'.split())

    return {
        'files': files,
        'sentences': sentences,
        'annotations': entities['total'] + relations['total'],
        'entities': entities,
        'relations': relations,
    }


def _add(d1, d2):
    result = {}

    for k,v1 in d1.items():
        v2 = d2[k]

        if isinstance(v1, dict):
            result[k] = _add(v1, v2)
        else:
            result[k] = v1 + v2

    return result


def _add_many(*dicts):
    dicts = list(dicts)
    result = dicts.pop()

    while dicts:
        result = _add(result, dicts.pop())

    return result


def _get_key(key, d):
    key_parts = key.split(".")

    for part in key_parts:
        d = d[part]

    return d


def table():
    trial = summarize('trial')
    training = summarize('training')
    develop = summarize('develop')
    test = summarize('test')
    totals = _add_many(trial, training, develop, test)

    keys = [
        "files",
        "sentences",
        "annotations",
        "entities.total",
        "entities.Concept",
        "entities.Action",
        "relations.roles",
        "relations.subject",
        "relations.target",
        "relations.relations",
        "relations.is-a",
        "relations.part-of",
        "relations.property-of",
        "relations.same-as"
    ]

    dicts = [totals, trial, training, develop, test]
    rows = []

    for key in keys:
        rows.append([_get_key(key, d) for d in dicts])

    return tabulate.tabulate(rows, tablefmt='latex')


if __name__ == '__main__':
    print(table())
