# coding: utf8

import os
import sys
import pprint
import collections
from os.path import abspath, join, exists


def read_input(path):
    with open(path, encoding='utf8') as fp:
        return fp.read()


def read_phrases(path):
    phrases = {}

    with open(path) as fp:
        for line in fp:
            idx, start, end = line.split()
            phrases[int(idx)] = dict(
                start=int(start),
                end=int(end),
            )

    return phrases


def read_labels(path):
    labels = {}

    with open(path) as fp:
        for line in fp:
            idx, label = line.split()
            labels[int(idx)] = label

    return labels


def read_links(path):
    links = []

    with open(path) as fp:
        for line in fp:
            line = line.split()
            rel = line[0]

            try:
                links.append(dict(
                    rel=rel,
                    arg1=int(line[1]),
                    arg2=int(line[2]),
                    arg3=None,
                ))
            except:
                pass

    return links


def find_obj(objs, x):
    if isinstance(objs, dict):
        source = objs.items()
    else:
        source = zip(objs, objs)

    for idx, l in source:
        for field in l:
            if l[field] != x[field]:
                break
        else:
            return idx

    return None


def between(x, a, b):
    return x >= a and x <= b


def intersect(x1, y1, x2, y2):
    if x1 >= y1:
        return False
    if x2 >= y2:
        return False

    return between(x1, x2, y2) or between(y1, x2, y2) or between(x2, x1, y1) or between(y2, x1, y1)


def find_partial(objs, x):
    fidx = find_obj(objs, x)

    if fidx:
        return fidx, True

    start = x['start']
    end = x['end']

    for idx, l in objs.items():
        sstart = l['start']
        send = l['end']

        if intersect(start, end, sstart, send):
            return idx, False

    return None, False


def sort(items):
    return sorted(items, key=lambda x: (x['start'], x['end']))


def compare_phrases(gold_phrases, dev_phrases):
    correct = []
    missing = []
    spurious = []
    partial = []
    mapping = {}

    for idx, l in gold_phrases.items():
        fidx, exact = find_partial(dev_phrases, l)

        if fidx and not "eval:%i" % fidx in mapping:
            if exact:
                correct.append(l)
            else:
                partial.append((l, dev_phrases[fidx]))

            mapping["ref:%i" % idx] = fidx
            mapping["eval:%i" % fidx] = idx
        else:
            missing.append(l)

    for fidx, l in dev_phrases.items():
        if not "eval:%i" % fidx in mapping:
            spurious.append(l)

    return dict(
        correct=sort(correct),
        missing=sort(missing),
        spurious=sort(spurious),
        partial=partial,
        mapping=mapping,
    )


def compare_labels(gold, dev, mapping):
    confussion_matrix = collections.defaultdict(lambda: 0)

    correct = []
    incorrect = []
    spurious = []
    missing = []

    for idx, l in gold.items():
        fidx = mapping.get('ref:%i' % idx)

        if not fidx:
            missing.append(dict(id=idx, label=l))
            continue

        if not fidx in dev:
            missing.append(dict(id=idx, label=l))
            confussion_matrix[(l, 'None')] += 1

        l2 = dev[fidx]
        confussion_matrix[(l, l2)] += 1

        if l == l2:
            correct.append(dict(fidx=fidx, label=l2))
        else:
            incorrect.append(dict(fidx=fidx, label=l2, correct=l))

    for fidx, l in dev.items():
        if "eval:%i" % fidx in mapping:
            continue

        spurious.append(dict(fidx=fidx, label=l))

    return dict(
        confussion_matrix=confussion_matrix,
        correct=correct,
        incorrect=incorrect,
        missing=missing,
        spurious=spurious,
    )


def map_entities(x, mapping, map_key):
    result = dict(
        rel=x['rel'],
        arg1=None,
        arg2=None,
        arg3=None,
    )

    for key in ["arg1", "arg2", "arg3"]:
        value = x[key]

        if value is None:
            result[key] = None
            continue

        mapped = map_key + ":%i" % value

        if not mapped in mapping:
            return False

        result[key] = mapping[mapped]

    return result


def find_relation(rel, relations):
    for r in relations:
        for k in ["rel", "arg1", "arg2", "arg3"]:
            if r[k] != rel[k]:
                break
        else:
            return True

    return False


def compare_links(gold_links, dev_links, mapping):
    correct = []
    missing = []
    spurious = []

    for rel in gold_links:
        mapped = map_entities(rel, mapping, "ref")

        if not mapped:
            missing.append(rel)
            continue

        if not find_relation(mapped, dev_links):
            missing.append(rel)
            continue

        correct.append(rel)

    for rel in dev_links:
        mapped = map_entities(rel, mapping, "eval")

        if not mapped:
            spurious.append(rel)
            continue

        if not find_relation(mapped, gold_links):
            spurious.append(rel)

    return dict(
        correct=correct,
        missing=missing,
        spurious=spurious,
    )


def get_span(sentences, obj):
    return sentences[obj["start"]:obj["end"]]
