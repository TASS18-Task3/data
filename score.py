#!/usr/bin/python3

import sys
import os
import random

gold = sys.argv[1] if len(sys.argv) > 1 else 'gold'
submit = sys.argv[2] if len(sys.argv) > 2 else 'submit'

with open(os.path.join(sys.argv[2], 'scores.txt'), 'wb') as fp:
    for label in "abc bc c".split():
        for val in "f1 prec rec".split():
            fp.write('%s_%s:%.5f\n' % (label, val, random.uniform(0,1)))

    fp.write('macro:%.5f\n' % random.uniform(0,1))
