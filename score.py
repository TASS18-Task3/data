#!/usr/bin/python3
# coding: utf8

import sys
import os
import random


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


def evaluate_1(fname, gold, submit):
    pass


if __name__ == '__main__':
    gold = sys.argv[1] if len(sys.argv) > 1 else 'gold'
    submit = sys.argv[2] if len(sys.argv) > 2 else 'submit'

    for fname in os.listdir(gold):
        if fname.endswith('_input.txt'):
            scenario1 = evaluate_1(fname, gold, submit)
            scenario2 = evaluate_2(fname, gold, submit)
            scenario3 = evaluate_3(fname, gold, submit)

    with open(os.path.join(sys.argv[2], 'scores.txt'), 'wb') as fp:
        for label in "abc bc c".split():
            for val in "f1 prec rec".split():
                fp.write('%s_%s:%.5f\n' % (label, val, random.uniform(0,1)))

        fp.write('macro:%.5f\n' % random.uniform(0,1))
