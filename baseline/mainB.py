import argparse
import json
import os
import random
import re
import sys
from typing import Sequence

random.seed(0)

MIND_FNAME = 'mind/task_B.mind'
OUTPUT_DIR = '../training/dev'

INPUT_PREFIX = 'input_'
OUTPUT_A_PREFIX = 'output_A_'
OUTPUT_B_PREFIX = 'output_B_'
RE_INPUT = re.compile(f'^{INPUT_PREFIX}.*$')
RE_OUTPUT_A = re.compile(f'^{OUTPUT_A_PREFIX}.*$')
RE_OUTPUT_B = re.compile(f'^{OUTPUT_B_PREFIX}.*$')

CLASSX_LIST = [ 'Concept', 'Action' ]


def output_fname(input_fname, prefix, to_dir=None):
    dir_name = os.path.dirname(input_fname)
    fname = os.path.basename(input_fname)
    output = prefix + fname[len(INPUT_PREFIX):]
    if to_dir is not None:
        dir_name = to_dir
    return os.path.join(dir_name, output)


def learn_from_directory(directory, training_input=None):
    if not os.path.isdir(directory):
        print(f'Directory is not valid!!! {directory}')
        return

    for fname in os.listdir(directory):
        full_fname = os.path.join(directory, fname)
        if not os.path.isfile(full_fname) or not RE_INPUT.match(fname):
            continue

        gold_fnameA = output_fname(full_fname, OUTPUT_A_PREFIX, training_input)
        gold_fnameB = output_fname(full_fname, OUTPUT_B_PREFIX, training_input)
        text_file = full_fname
        gold_fileA = gold_fnameA
        gold_fileB = gold_fnameB

        if not os.path.isfile(gold_fileA) or not os.path.isfile(gold_fileB):
            print('Matching output not found!!')
            continue

        yield learn_from_file(text_file, gold_fileA, gold_fileB)

def learn_from_file(text_file:str, gold_fileA:str, gold_fileB:str):
    text = ""
    gold_keyphrases = []
    gold_classifications = []

    with open(text_file) as fd:
        text = fd.read()
    with open(gold_fileA) as fd:
        gold_keyphrases = fd.readlines()
    with open(gold_fileB) as fd:
        gold_classifications = fd.readlines()

    map_id_to_keyphrase = dict(extract_keyphrases(text, gold_keyphrases))
    classifications = extract_classifications(gold_classifications)
    classification_map = {}
    for idx, classx in classifications:
        keyphrase = map_id_to_keyphrase[idx]
        try:
            classification_map[keyphrase][classx] += 1
        except KeyError:
            classification_map[keyphrase] = dict((x, int(x==classx.title())) for x in CLASSX_LIST)
    return classification_map

def extract_keyphrases(text:str, gold_keyphrases:Sequence[str]):
    for idx,start,end in extract_spans(gold_keyphrases):
        yield idx, text[start:end].lower()

def extract_spans(gold_keyphrases:Sequence[str]):
    for keyphrase in gold_keyphrases:
        keyphrase = keyphrase.strip()
        if keyphrase:
            yield tuple(int(x) for x in keyphrase.split('\t'))

def extract_classifications(gold_classifications:Sequence[str]):
    for classification in gold_classifications:
        classification = classification.strip()
        if classification:
            idx, classx = classification.split('\t')
            yield int(idx), classx



def save_knowledge(mind, path='', fname=MIND_FNAME):
    full_name = os.path.join(path, fname)
    with open(full_name, mode='w') as fd:
        json.dump(mind, fd, ensure_ascii=False, indent=1)

def load_knowledge(path='', fname=MIND_FNAME):
    full_name = os.path.join(path, fname)
    if os.path.exists(full_name):
        with open(full_name) as fd:
            return json.load(fd)
    else:
        return {}



def process_file(text_file:str, gold_fileA:str, mind):
    text = ""
    gold_keyphrases = []

    with open(text_file) as fd:
        text = fd.read()
    with open(gold_fileA) as fd:
        gold_keyphrases = fd.readlines()

    for idx, keyphrase in extract_keyphrases(text, gold_keyphrases):
        keyphrase = keyphrase.lower()
        yield idx, get_highest_class_and_disambiguate(keyphrase, mind)

def get_highest_class_and_disambiguate(keyphrase:str, mind):
    try:
        mind_classification = mind[keyphrase]
        max_count = max(mind_classification.values())
        max_classes = [classx for classx, count in mind_classification.items() if count == max_count]
        max_class = random.choice(max_classes)
        if len(max_classes) > 1:
            mind_classification[max_class] += 1
        return max_class
    except:
        classx = random.choice(CLASSX_LIST)
        mind_classification = dict((x, int(x==classx)) for x in CLASSX_LIST)
        return classx


def train(directory, training_input=None):
    mind = {}
    for x in learn_from_directory(directory, training_input):
        join_knowledge(mind, x)
    save_knowledge(mind)

def join_knowledge(mind, new_knowledge):
    for keyphrase, classification in new_knowledge.items():
        try:
            mind_classification = mind[keyphrase]
            for classx, count in classification.items():
                try:
                    mind_classification[classx] += count
                except KeyError:
                    mind_classification[classx] = count
        except KeyError:
            mind[keyphrase] = classification.copy()

def with_dual_class(mind):
    for key,value in mind.items():
        if all( value[classx] > 0 for classx in CLASSX_LIST ):
            yield key, value

def test(text_file, gold_fileA, output_dir=OUTPUT_DIR):
    if not RE_INPUT.match(os.path.basename(text_file)):
        return
    mind = load_knowledge()

    full_fname = output_fname(text_file, OUTPUT_B_PREFIX, output_dir)
    with open(full_fname, mode='w') as fd:
        for idx, classx in process_file(text_file, gold_fileA, mind):
            fd.write('%s\t%s\n' % (idx, classx))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', metavar='TEXT', nargs='?', help='Process TEXT file')
    parser.add_argument('outputA', metavar='OUTPUT-A', nargs='?', help='Process OUTPUT-A file')
    parser.add_argument('-t','--train', metavar='DIR', dest='train', action='store', help='Train from DIR directory')
    args = parser.parse_args(sys.argv[1:])

    if args.train:
        train(args.train)

    if args.text and args.outputA:
        test(args.text, args.outputA)
    elif args.text or args.outputA:
        print(f'Missing file!!!')


if __name__ == '__main__':
    main()
