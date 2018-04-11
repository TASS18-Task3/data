import argparse
import json
import os
import random
import re
import sys
from typing import Sequence

random.seed(0)

MIND_FNAME = 'mind/task_C.mind'
OUTPUT_DIR = '../training/dev'

INPUT_PREFIX = 'input_'
OUTPUT_A_PREFIX = 'output_A_'
OUTPUT_B_PREFIX = 'output_B_'
OUTPUT_C_PREFIX = 'output_C_'
RE_INPUT = re.compile(f'^{INPUT_PREFIX}.*$')
RE_OUTPUT_A = re.compile(f'^{OUTPUT_A_PREFIX}.*$')
RE_OUTPUT_B = re.compile(f'^{OUTPUT_B_PREFIX}.*$')
RE_OUTPUT_C = re.compile(f'^{OUTPUT_C_PREFIX}.*$')

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
        gold_fnameC = output_fname(full_fname, OUTPUT_C_PREFIX, training_input)
        text_file = full_fname
        gold_fileA = gold_fnameA
        gold_fileB = gold_fnameB
        gold_fileC = gold_fnameC

        if not os.path.isfile(gold_fileA) or not os.path.isfile(gold_fileB) or not os.path.isfile(gold_fileC):
            print('Matching output not found!!')
            continue

        yield learn_from_file(text_file, gold_fileA, gold_fileB, gold_fileC)

def learn_from_file(text_file:str, gold_fileA:str, gold_fileB:str, gold_fileC:str):
    text = ""
    gold_keyphrases = []
    gold_classifications = []
    gold_relations = []

    with open(text_file) as fd:
        text = fd.read()
    with open(gold_fileA) as fd:
        gold_keyphrases = fd.readlines()
    with open(gold_fileB) as fd:
        gold_classifications = fd.readlines()
    with open(gold_fileC) as fd:
        gold_relations = fd.readlines()

    map_id_to_keyphrase = dict(extract_keyphrases(text, gold_keyphrases))
    map_id_to_classification = dict(extract_classifications(gold_classifications))

    relations = extract_relations(gold_relations)
    relation_map = {}
    for rclass, idx, idy in relations:
        keyphrase_x = map_id_to_keyphrase[idx]
        keyphrase_y = map_id_to_keyphrase[idy]

        class_x = map_id_to_classification[idx]
        class_y = map_id_to_classification[idy]

        try:
            relation_map[keyphrase_x, keyphrase_y, class_x, class_y].add(rclass)
        except KeyError:
            relation_map[keyphrase_x, keyphrase_y, class_x, class_y] = { rclass }

    return relation_map

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

def extract_relations(gold_relations:Sequence[str]):
    for relation in gold_relations:
        relation = relation.strip()
        if relation:
            rclass, idx, idy = relation.split('\t')
            yield rclass, int(idx), int(idy)

def extract_keyphrases_per_sentence(text:str, gold_keyphrases:Sequence[str]):
    sentences = text.splitlines(True)
    offset = 0
    for s in sentences:
        yield extract_keyphrases_of_sentence(s, offset, gold_keyphrases)
        offset += len(s)

def extract_keyphrases_of_sentence(sentence:str, offset:int, gold_keyphrases:Sequence[str]):
    for idx, start, end in extract_spans(gold_keyphrases):
        start -= offset
        end -= offset
        if 0 <= start <= end < len(sentence):
            yield idx, sentence[start:end].lower()



def save_knowledge(mind, path='', fname=MIND_FNAME):
    mind = dict( ('\t'.join(key), list(value)) for key, value in mind.items() )
    full_name = os.path.join(path, fname)
    with open(full_name, mode='w') as fd:
        json.dump(mind, fd, ensure_ascii=False, indent=1)

def load_knowledge(path='', fname=MIND_FNAME):
    full_name = os.path.join(path, fname)
    if os.path.exists(full_name):
        with open(full_name) as fd:
            mind = json.load(fd)
            return dict( (tuple(key.split('\t')), set(value)) for key,value in mind.items() )
    else:
        return {}



def process_file(text_file:str, gold_fileA:str, gold_fileB:str, mind):
    text = ""
    gold_keyphrases = []
    gold_classifications = []

    with open(text_file) as fd:
        text = fd.read()
    with open(gold_fileA) as fd:
        gold_keyphrases = fd.readlines()
    with open(gold_fileB) as fd:
        gold_classifications = fd.readlines()

    map_id_to_classification = dict(extract_classifications(gold_classifications))

    for sentence_keyphrases in extract_keyphrases_per_sentence(text, gold_keyphrases):
        keyphrases = list(sentence_keyphrases)
        for idx, keyphrase_x in keyphrases:
            keyphrase_x = keyphrase_x.lower()
            class_x = map_id_to_classification[idx]
            for idy, keyphrase_y in keyphrases:
                keyphrase_y = keyphrase_y.lower()
                class_y = map_id_to_classification[idy]
                try:
                    for rclass in mind[keyphrase_x, keyphrase_y, class_x, class_y]:
                        yield rclass, idx, idy
                except KeyError:
                    pass



def train(directory, training_input=None):
    mind = {}
    for x in learn_from_directory(directory, training_input):
        join_knowledge(mind, x)
    save_knowledge(mind)

def join_knowledge(mind, new_knowledge):
    for key, relations in new_knowledge.items():
        try:
            mind_relations = mind[key]
            mind_relations.update(relations)
        except KeyError:
            mind[key] = relations.copy()

def with_multiple_relations(mind):
    for key,value in mind.items():
        if len(value) > 1:
            yield key, value

def test(text_file, gold_fileA, gold_fileB, output_dir=OUTPUT_DIR):
    if not RE_INPUT.match(os.path.basename(text_file)):
        return
    mind = load_knowledge()

    full_fname = output_fname(text_file, OUTPUT_C_PREFIX, output_dir)
    with open(full_fname, mode='w') as fd:
        for rclass, idx, idy in process_file(text_file, gold_fileA, gold_fileB, mind):
            fd.write('%s\t%s\t%s\n' % (rclass, idx, idy))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', metavar='TEXT', nargs='?', help='Process TEXT file')
    parser.add_argument('outputA', metavar='OUTPUT-A', nargs='?', help='Process OUTPUT-A file')
    parser.add_argument('outputB', metavar='OUTPUT-B', nargs='?', help='Process OUTPUT-B file')
    parser.add_argument('-t','--train', metavar='DIR', dest='train', action='store', help='Train from DIR directory')
    args = parser.parse_args(sys.argv[1:])

    if args.train:
        train(args.train)

    if args.text and args.outputA and args.outputB:
        test(args.text, args.outputA, args.outputB)
    elif args.text or args.outputA or args.outputB:
        print(f'Missing file!!!')


if __name__ == '__main__':
    main()
