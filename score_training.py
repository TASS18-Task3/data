#!/usr/bin/python3
# coding: utf8

import os
import sys
import pprint
import collections
from tools import (get_span,
                   read_input,
                   read_phrases,
                   read_links,
                   read_labels,
                   compare_phrases,
                   compare_links,
                   compare_labels)

from os.path import abspath, join, exists


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

    print('* Incorrect (%i):' % len(comparison['incorrect']))
    for item in comparison['incorrect']:
        item["start"] = dev_phrases[item['fidx']]["start"]
        item["end"] = dev_phrases[item['fidx']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end} (correct is {correct}).'.format(**item))

    print('* Missing (%i):' % len(comparison['missing']))
    for item in comparison['missing']:
        item["start"] = gold_phrases[item['id']]["start"]
        item["end"] = gold_phrases[item['id']]["end"]
        item["text"] = get_span(sentences, item)
        print('  - {label} "{text}" from {start} to {end}.'.format(**item))

    print('* Spurious (%i):' % len(comparison['spurious']))
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


def evaluate(file, folder):
    input_file = abspath(join(folder, 'input', 'input_%s.txt' % file))
    gold_phrases_file = abspath(join(folder, 'gold', 'output_A_%s.txt' % file))
    dev_phrases_file = abspath(join(folder, 'dev', 'output_A_%s.txt' % file))

    if not exists(input_file):
        raise ValueError("Input file '%s' not found." % input_file)

    if not exists(gold_phrases_file):
        raise ValueError("Gold phrases file '%s' not found." % gold_phrases_file)

    if not exists(dev_phrases_file):
        raise ValueError("Development phrases file '%s' not found." % dev_phrases_file)

    l = evaluate_phrases(input_file, gold_phrases_file, dev_phrases_file)

    gold_labels_file = abspath(join(folder, 'gold', 'output_B_%s.txt' % file))
    dev_labels_file = abspath(join(folder, 'dev', 'output_B_%s.txt' % file))

    if not exists(gold_labels_file):
        raise ValueError("Gold phrases file '%s' not found." % gold_phrases_file)

    if not exists(dev_labels_file):
        print("\n(!) Skipping Task B: file '%s' not found. Assuming task is not completed yet." % dev_labels_file)
    else:
        evaluate_labels(gold_labels_file, dev_labels_file, *l)

    ref_links_file = abspath(join(folder, 'gold', 'output_C_%s.txt' % file))
    eval_links_file = abspath(join(folder, 'dev', 'output_C_%s.txt' % file))

    if not exists(eval_links_file):
        print("\n(!) Skipping Task C: file '%s' not found. Assuming task is not completed yet." % eval_links_file)
    else:
        evaluate_links(ref_links_file, eval_links_file, *l)


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else "training"

    for fname in os.listdir(os.path.join(folder, 'input')):
        if fname.startswith("input_"):
            evaluate(fname[6:-4], folder)
