#!/usr/bin/python3
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

        if fidx and not "eval:%i"%fidx in mapping:
            if exact:
                correct.append(l)
            else:
                partial.append((l, dev_phrases[fidx]))

            mapping["ref:%i"%idx] = fidx
            mapping["eval:%i"%fidx] = idx
        else:
            missing.append(l)

    for fidx, l in dev_phrases.items():
        if not "eval:%i"%fidx in mapping:
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
        if "eval:%i"%fidx in mapping:
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
        arg1 = None,
        arg2 = None,
        arg3 = None,
    )

    for key in ["arg1", "arg2", "arg3"]:
        value = x[key]

        if value is None:
            result[key] = None
            continue

        mapped = map_key+":%i"%value

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


def evaluate_phrases(input_file, gold_phrases_file, dev_phrases_file):
    sentences = read_input(input_file)
    gold_phrases = read_phrases(gold_phrases_file)
    dev_phrases = read_phrases(dev_phrases_file)

    comparison = compare_phrases(gold_phrases, dev_phrases)

    print("# Task A (detecting phrases)")
    print("  input file:        %s" % input_file)
    print("  gold file: %s" % gold_phrases_file)
    print("  dev file:  %s" % dev_phrases_file)

    print('\n* Correct (%i):' % len(comparison['correct']))
    for item in comparison['correct']:
        item["text"] = get_span(sentences, item)
        print(u'  - "{text}" from {start} to {end}.'.format(**item))

    print('* Partial (%i):' % len(comparison['partial']))
    for item, other in comparison['partial']:
        item["text"] = get_span(sentences, item)
        other["text"] = get_span(sentences, other)
        print(u'  - "{text}" from {start} to {end}'.format(**item), end="")
        print(u' vs "{text}" from {start} to {end}.'.format(**other))

    print('* Missing (%i):' % len(comparison['missing']))
    for item in comparison['missing']:
        item["text"] = get_span(sentences, item)
        print(u'  - "{text}" from {start} to {end}.'.format(**item))

    print('* Spurious (%i):' % len(comparison['spurious']))
    for item in comparison['spurious']:
        item["text"] = get_span(sentences, item)
        print(u'  - "{text}" from {start} to {end}.'.format(**item))

    ok = len(comparison['correct']) + 0.5 * len(comparison['partial'])
    precision = ok / (ok + len(comparison['spurious']))
    recall = ok / (ok + len(comparison['missing']))
    f1 = 2 * precision * recall / (precision + recall)

    print("\nPrecision = %.2f\nRecall = %.2f\nF1 Score = %.2f" % (precision, recall, f1))

    return sentences, gold_phrases, dev_phrases, comparison['mapping']


def evaluate_labels(gold_labels_file, dev_labels_file, sentences, gold_phrases, dev_phrases, mapping):
    gold_labels = read_labels(gold_labels_file)
    dev_labels = read_labels(dev_labels_file)

    print("\n# Taks B (labeling phrases)")
    print("  gold file: %s" % gold_labels_file)
    print("  dev file:  %s" % dev_labels_file)

    comparison = compare_labels(gold_labels, dev_labels, mapping)

    print('\n* Correct (%i):' % len(comparison['correct']))
    for item in comparison['correct']:
        item["start"] = dev_phrases[item['fidx']]["start"]
        item["end"] = dev_phrases[item['fidx']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end}.'.format(**item))

    print('\n* Incorrect (%i):' % len(comparison['incorrect']))
    for item in comparison['incorrect']:
        item["start"] = dev_phrases[item['fidx']]["start"]
        item["end"] = dev_phrases[item['fidx']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end} (correct is {correct}).'.format(**item))

    print('\n* Missing (%i):' % len(comparison['missing']))
    for item in comparison['missing']:
        item["start"] = gold_phrases[item['id']]["start"]
        item["end"] = gold_phrases[item['id']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end}.'.format(**item))

    print('\n* Spurious (%i):' % len(comparison['spurious']))
    for item in comparison['spurious']:
        item["start"] = dev_phrases[item['fidx']]["start"]
        item["end"] = dev_phrases[item['fidx']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end}.'.format(**item))

    ok = len(comparison['correct']) * 1.0
    micro = len(comparison['correct']) + len(comparison['incorrect'])
    macro = micro + len(comparison['missing']) + len(comparison['spurious'])

    precision = ok / (micro + len(comparison['spurious']))
    recall = ok / (micro + len(comparison['missing']))
    f1 = 2 * precision * recall / (precision + recall)

    print("\nMicro-accuracy: %.2f" % (ok / micro))
    print("Macro-accuracy: %.2f" % (ok / macro))
    print("Precision: %.2f" % precision)
    print("Recall: %.2f" % recall)
    print("F1: %.2f" % f1)


def evaluate_links(gold_links_file, dev_links_file, sentences, gold_phrases, dev_phrases, mapping):
    gold_links = read_links(gold_links_file)
    dev_links = read_links(dev_links_file)

    print("\n# Taks C (linking)")
    print("  gold file: %s" % gold_links_file)
    print("  dev file:  %s" % dev_links_file)

    comparison = compare_links(gold_links, dev_links, mapping)

    print('\n* Correct (%i):' % len(comparison['correct']))
    for item in comparison['correct']:
        item["text1"] = get_span(sentences, gold_phrases[item['arg1']]) if item['arg1'] else ""
        item["text2"] = get_span(sentences, gold_phrases[item['arg2']]) if item['arg2'] else ""
        item["text3"] = get_span(sentences, gold_phrases[item['arg3']]) if item['arg3'] else ""

        if item["text3"]:
            print('  - {rel} involving "{text1}", "{text2}" and "{text3}".'.format(**item))
        else:
            print('  - {rel} involving "{text1}" and "{text2}".'.format(**item))

    print('* Missing (%i):' % len(comparison['missing']))
    for item in comparison['missing']:
        item["text1"] = get_span(sentences, gold_phrases[item['arg1']]) if item['arg1'] else ""
        item["text2"] = get_span(sentences, gold_phrases[item['arg2']]) if item['arg2'] else ""
        item["text3"] = get_span(sentences, gold_phrases[item['arg3']]) if item['arg3'] else ""

        if item["text3"]:
            print('  - {rel} involving "{text1}", "{text2}" and "{text3}".'.format(**item))
        else:
            print('  - {rel} involving "{text1}" and "{text2}".'.format(**item))

    print('* Spurious (%i):' % len(comparison['spurious']))
    for item in comparison['spurious']:
        item["text1"] = get_span(sentences, dev_phrases[item['arg1']]) if item['arg1'] else ""
        item["text2"] = get_span(sentences, dev_phrases[item['arg2']]) if item['arg2'] else ""
        item["text3"] = get_span(sentences, dev_phrases[item['arg3']]) if item['arg3'] else ""

        if item["text3"]:
            print('  - {rel} involving "{text1}", "{text2}" and "{text3}".'.format(**item))
        else:
            print('  - {rel} involving "{text1}" and "{text2}".'.format(**item))

    ok = len(comparison['correct']) * 1.0
    precision = ok / (ok + len(comparison['spurious']))
    recall = ok / (ok + len(comparison['missing']))
    f1 = 2 * precision * recall / (precision + recall)

    print("\nPrecision: %.2f" % precision)
    print("Recall: %.2f" % recall)
    print("F1: %.2f" % f1)


def evaluate(file):
    gold = sys.argv[1] if len(sys.argv) > 1 else "gold"
    dev = sys.argv[2] if len(sys.argv) > 2 else "dev"

    input_file = abspath(join(gold, 'input_%s.txt' % file))
    gold_phrases_file = abspath(join(gold, 'output_A_%s.txt' % file))
    dev_phrases_file = abspath(join(dev, 'output_A_%s.txt' % file))

    if not exists(input_file):
        raise ValueError("Input file '%s' not found." % input_file)

    if not exists(gold_phrases_file):
        raise ValueError("Gold phrases file '%s' not found." % gold_phrases_file)

    if not exists(dev_phrases_file):
        raise ValueError("Development phrases file '%s' not found." % dev_phrases_file)

    l = evaluate_phrases(input_file, gold_phrases_file, dev_phrases_file)

    gold_labels_file = abspath(join(gold, 'output_B_%s.txt' % file))
    dev_labels_file = abspath(join(dev, 'output_B_%s.txt' % file))

    if not exists(gold_labels_file):
        raise ValueError("Gold phrases file '%s' not found." % gold_phrases_file)

    if not exists(dev_labels_file):
        print("\n(!) Skipping Task B: file '%s' not found. Assuming task is not completed yet." % dev_labels_file)
    else:
        evaluate_labels(gold_labels_file, dev_labels_file, *l)

    ref_links_file = abspath(join(gold, 'output_C_%s.txt' % file))
    eval_links_file = abspath(join(dev, 'output_C_%s.txt' % file))

    if not exists(eval_links_file):
        print("\n(!) Skipping Task C: file '%s' not found. Assuming task is not completed yet." % eval_links_file)
    else:
        evaluate_links(ref_links_file, eval_links_file, *l)


if __name__ == '__main__':
    gold = sys.argv[1] if len(sys.argv) > 1 else "gold"
    dev = sys.argv[2] if len(sys.argv) > 2 else "dev"

    for fname in os.listdir(gold):
        if fname.startswith("input_"):
            evaluate(fname[6:-4])
