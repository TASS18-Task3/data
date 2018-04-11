import argparse
import json
import os
import re
import sys
from typing import Sequence

MIND_FNAME = 'mind/task_A.mind'
OUTPUT_DIR = '../training/dev'

INPUT_PREFIX = 'input_'
OUTPUT_A_PREFIX = 'output_A_'
RE_INPUT = re.compile(f'^{INPUT_PREFIX}.*$')
RE_OUTPUT_A = re.compile(f'^{OUTPUT_A_PREFIX}.*$')


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

        gold_fname = output_fname(full_fname, OUTPUT_A_PREFIX, training_input)
        text_file = full_fname
        gold_file = gold_fname

        if not os.path.isfile(gold_file):
            print('Matching output not found!!')
            continue

        for span in learn_from_file(text_file, gold_file):
            yield span


def learn_from_file(text_file:str, gold_file:str):
    text = ""
    gold_keyphrases = []
    with open(text_file) as fd:
        text = fd.read()
    with open(gold_file) as fd:
        gold_keyphrases = fd.readlines()
    return extract_keyphrases(text, gold_keyphrases)

def extract_keyphrases(text:str, gold_keyphrases:Sequence[str]):
    for _,start,end in extract_spans(gold_keyphrases):
        yield text[start:end].lower()

def extract_spans(gold_keyphrases:Sequence[str]):
    for keyphrase in gold_keyphrases:
        keyphrase = keyphrase.strip()
        if keyphrase:
            yield tuple(int(x) for x in keyphrase.split('\t'))



def save_knowledge(mind, path='', fname=MIND_FNAME):
    full_name = os.path.join(path, fname)
    with open(full_name, mode='w') as fd:
        json.dump(mind, fd, ensure_ascii=False)

def load_knowledge(path='', fname=MIND_FNAME):
    full_name = os.path.join(path, fname)
    if os.path.exists(full_name):
        with open(full_name) as fd:
            return json.load(fd)
    else:
        return []



def process_file(text_file:str, mind):
    sentences = None
    with open(text_file) as fd:
        sentences = fd.readlines()

    offset = 0
    for s in sentences:
        for word, start, end in process_sentence(s, mind):
            yield word, offset + start, offset + end
        offset += len(s)

def process_sentence(sentence:str, mind):
    for word, start, end in extract_words(sentence):
        if word.lower() in mind:
            yield word, start, end

def extract_words(sentence:str):
    word_start = 0
    for word_end, char in enumerate(sentence):
        if not char.isalnum():
            if word_start != word_end:
                yield sentence[word_start:word_end], word_start, word_end
            word_start = word_end + 1



def train(directory, training_input=None):
    mind = list(set(learn_from_directory(directory, training_input)))
    save_knowledge(mind)

def test(text_file, output_dir=OUTPUT_DIR):
    if not RE_INPUT.match(os.path.basename(text_file)):
        return

    mind = load_knowledge()

    full_fname = output_fname(text_file, OUTPUT_A_PREFIX, output_dir)
    with open(full_fname, mode='w') as fd:
        for i, (_, start, end) in enumerate(process_file(text_file, mind)):
            fd.write('%s\t%s\t%s\n' % (i+1, start, end))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', nargs='?', help='Process INPUT file')
    parser.add_argument('-t','--train', metavar='DIR', dest='train', action='store', help='Train from DIR directory')
    args = parser.parse_args(sys.argv[1:])

    if args.train:
        train(args.train)
    if args.input:
        test(args.input)

if __name__ == '__main__':
    main()
