#!/usr/bin/python3
# coding: utf8

import sys
import os
import random
import pprint
import collections

from tools import (get_span,
                   read_input,
                   read_phrases,
                   read_labels,
                   read_links,
                   compare_phrases,
                   compare_labels,
                   compare_links)


def evaluate(gold_A, gold_B, gold_C, submit_A, submit_B, submit_C):
    result_A = compare_phrases(gold_A, submit_A)
    result_B = compare_labels(gold_B, submit_B, result_A['mapping'])
    result_C = compare_links(gold_C, submit_C, result_A['mapping'])

    return dict(
        correct_A=len(result_A['correct']),
        correct_B=len(result_B['correct']),
        correct_C=len(result_C['correct']),
        partial_A=len(result_A['partial']),
        missing_A=len(result_A['missing']),
        missing_C=len(result_C['missing']),
        spurious_A=len(result_A['spurious']),
        spurious_C=len(result_C['spurious']),
        incorrect_B=len(result_B['incorrect']),
    )

def evaluate_1(name, gold, submit):
    gold_A = read_phrases(os.path.join(gold, 'output_A_%s' % name))
    gold_B = read_labels(os.path.join(gold, 'output_B_%s' % name))
    gold_C = read_links(os.path.join(gold, 'output_C_%s' % name))

    submit_A = read_phrases(os.path.join(submit, 'scenario1-ABC', 'output_A_%s' % name))
    submit_B = read_labels(os.path.join(submit, 'scenario1-ABC', 'output_B_%s' % name))
    submit_C = read_links(os.path.join(submit, 'scenario1-ABC', 'output_C_%s' % name))

    return evaluate(gold_A, gold_B, gold_C, submit_A, submit_B, submit_C)


def evaluate_2(name, gold, submit):
    gold_A = read_phrases(os.path.join(gold, 'output_A_%s' % name))
    gold_B = read_labels(os.path.join(gold, 'output_B_%s' % name))
    gold_C = read_links(os.path.join(gold, 'output_C_%s' % name))

    submit_A = gold_A
    submit_B = read_labels(os.path.join(submit, 'scenario2-BC', 'output_B_%s' % name))
    submit_C = read_links(os.path.join(submit, 'scenario2-BC', 'output_C_%s' % name))

    return evaluate(gold_A, gold_B, gold_C, submit_A, submit_B, submit_C)


def evaluate_3(name, gold, submit):
    gold_A = read_phrases(os.path.join(gold, 'output_A_%s' % name))
    gold_B = read_labels(os.path.join(gold, 'output_B_%s' % name))
    gold_C = read_links(os.path.join(gold, 'output_C_%s' % name))

    submit_A = gold_A
    submit_B = gold_B
    submit_C = read_links(os.path.join(submit, 'scenario3-C', 'output_C_%s' % name))

    return evaluate(gold_A, gold_B, gold_C, submit_A, submit_B, submit_C)


def update(dict_1, dict_2):
    for k,v in dict_1.items():
        dict_2[k] += v


if __name__ == '__main__':
    if len(sys.argv) > 1:
        gold = os.path.join(sys.argv[1], 'ref')
        submit = os.path.join(sys.argv[1], 'res')

        sub_submit = os.path.join(submit, 'submit')

        if os.path.exists(sub_submit):
            submit = sub_submit

        output = sys.argv[2]
    else:
        print('(!) Using `training/dev` as test files and `training/gold` as reference files.')
        gold = 'training/gold'
        submit = 'training/dev'
        output = '.'

    totals1 = collections.defaultdict(lambda: 0.0) # init with float to force float division
    totals2 = collections.defaultdict(lambda: 0.0)
    totals3 = collections.defaultdict(lambda: 0.0)

    for fname in os.listdir(gold):
        if fname.startswith('output_A_'):
            name = fname[9:]

            scenario1 = evaluate_1(name, gold, submit)
            update(scenario1, totals1)

            scenario2 = evaluate_2(name, gold, submit)
            update(scenario2, totals2)

            scenario3 = evaluate_3(name, gold, submit)
            update(scenario3, totals3)

    # pprint.pprint(('Scenario 1', totals1))
    # pprint.pprint(('Scenario 2', totals2))
    # pprint.pprint(('Scenario 3', totals3))

    correct_1 = sum([totals1['correct_A'], totals1['correct_B'], totals1['correct_C'], 0.5 * totals1['partial_A']])
    subtotal_1 = sum([totals1['partial_A'], totals1['correct_A'], totals1['correct_B'], totals1['incorrect_B'], totals1['correct_C']])

    abc_prec = correct_1 / sum([subtotal_1, totals1['spurious_A'], totals1['spurious_C']])
    abc_rec = correct_1 / sum([subtotal_1, totals1['missing_A'], totals1['missing_C']])
    abc_f1 = 2 * abc_prec * abc_rec / ( abc_prec + abc_rec )

    correct_2 = sum([totals2['correct_B'], totals2['correct_C']])
    subtotal_2 = sum([totals2['correct_B'], totals2['incorrect_B'], totals2['correct_C']])

    bc_prec = correct_2 / sum([subtotal_2, totals2['spurious_C']])
    bc_rec = correct_2 / sum([subtotal_2, totals2['missing_C']])
    bc_f1 = 2 * bc_prec * bc_rec / ( bc_prec + bc_rec )

    correct_3 = totals3['correct_C']
    subtotal_3 = totals3['correct_C']

    c_prec = correct_3 / sum([subtotal_3, totals2['spurious_C']])
    c_rec = correct_3 / sum([subtotal_3, totals2['missing_C']])
    c_f1 = 2 * c_prec * c_rec / ( c_prec + c_rec )

    macro = sum([abc_f1, bc_f1, c_f1]) / 3

    print('abc_prec:%.5f' % abc_prec)
    print('abc_rec:%.5f' % abc_rec)
    print('abc_f1:%.5f' % abc_f1)
    print('bc_prec:%.5f' % bc_prec)
    print('bc_rec:%.5f' % bc_rec)
    print('bc_f1:%.5f' % bc_f1)
    print('c_prec:%.5f' % c_prec)
    print('c_rec:%.5f' % c_rec)
    print('c_f1:%.5f' % c_f1)
    print('macro:%.5f' % macro)

    with open(os.path.join(output, 'scores.txt'), 'w') as fp:
        fp.write('abc_prec:%.5f\n'% abc_prec)
        fp.write('abc_rec:%.5f\n' % abc_rec)
        fp.write('abc_f1:%.5f\n'  % abc_f1)

        fp.write('bc_prec:%.5f\n' % bc_prec)
        fp.write('bc_rec:%.5f\n'  % bc_rec)
        fp.write('bc_f1:%.5f\n'   % bc_f1)

        fp.write('c_prec:%.5f\n'  % c_prec)
        fp.write('c_rec:%.5f\n'   % c_rec)
        fp.write('c_f1:%.5f\n'    % c_f1)

        fp.write('macro:%.5f\n'   % macro)
