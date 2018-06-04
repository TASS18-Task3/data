# coding: utf8

import csv
from pathlib import Path
from score_test import evaluate_1, evaluate_2, evaluate_3


gold_folder = Path("test") / "gold"


def build_participants_table():
    base = Path("submissions")
    return [f for f in base.iterdir() if f.is_dir()]


def update(result, scenario, name):
    for k,v in scenario.items():
        result[name + '-' + k] = v

    return result


def compute_taskA(d):
    total_pre = d['correct_A'] + d['partial_A'] + d['spurious_A']
    total_rec = d['correct_A'] + d['partial_A'] + d['missing_A']
    pre = ((d['correct_A'] + 0.5 * d['partial_A']) / total_pre) if total_pre else 0
    rec = ((d['correct_A'] + 0.5 * d['partial_A']) / total_rec) if total_rec else 0
    d['task_A_pre'] = pre
    d['task_A_rec'] = rec
    d['task_A_f1'] = ( 2 * pre * rec ) / ( pre + rec ) if ( pre + rec > 0 ) else 0
    return d


def compute_taskB(d):
    total_acc = d['correct_B'] + d['incorrect_B']
    acc = ( d['correct_B']  / total_acc) if total_acc else 0
    d['task_B_acc'] = acc
    return d


def compute_taskC(d):
    total_pre = d['correct_C'] + d['spurious_C']
    total_rec = d['correct_C'] + d['missing_C']
    pre = ((d['correct_C']) / total_pre) if total_pre else 0
    rec = ((d['correct_C']) / total_rec) if total_rec else 0
    d['task_C_pre'] = pre
    d['task_C_rec'] = rec
    d['task_C_f1'] = ( 2 * pre * rec ) / ( pre + rec ) if ( pre + rec > 0 ) else 0
    return d


def compute_scenario1(d):
    total_pre = d['correct_A'] + d['partial_A'] + d['spurious_A'] + d['correct_B'] + d['incorrect_B'] + d['correct_C'] + d['spurious_C']
    total_rec = d['correct_A'] + d['partial_A'] + d['missing_A'] + d['correct_B'] + d['incorrect_B'] + d['correct_C'] + d['missing_C']

    pre = ( d['correct_A'] + 0.5 * d['partial_A'] + d['correct_B'] + d['correct_C'] ) / total_pre if total_pre > 0 else 0
    rec = ( d['correct_A'] + 0.5 * d['partial_A'] + d['correct_B'] + d['correct_C'] ) / total_rec if total_rec > 0 else 0

    d['total_micro_pre'] = pre
    d['total_micro_rec'] = rec
    d['total_micro_f1'] = ( 2 * pre * rec ) / ( pre + rec ) if ( pre + rec > 0 ) else 0


def compute_scenario2(d):
    total_pre = d['correct_B'] + d['incorrect_B'] + d['correct_C'] + d['spurious_C']
    total_rec = d['correct_B'] + d['incorrect_B'] + d['correct_C'] + d['missing_C']

    pre = ( d['correct_B'] + d['correct_C'] ) / total_pre if total_pre > 0 else 0
    rec = ( d['correct_B'] + d['correct_C'] ) / total_rec if total_rec > 0 else 0

    d['total_micro_pre'] = pre
    d['total_micro_rec'] = rec
    d['total_micro_f1'] = ( 2 * pre * rec ) / ( pre + rec ) if ( pre + rec > 0 ) else 0


def compute_scenario3(d):
    total_pre = d['correct_C'] + d['spurious_C']
    total_rec = d['correct_C'] + d['missing_C']

    pre = ( d['correct_C'] ) / total_pre if total_pre > 0 else 0
    rec = ( d['correct_C'] ) / total_rec if total_rec > 0 else 0

    d['total_micro_pre'] = pre
    d['total_micro_rec'] = rec
    d['total_micro_f1'] = ( 2 * pre * rec ) / ( pre + rec ) if ( pre + rec > 0 ) else 0


def compute_micro_f1(d1, d2, d3):
    total_pre_1 = d1['correct_A'] + d1['partial_A'] + d1['spurious_A'] + d1['correct_B'] + d1['incorrect_B'] + d1['correct_C'] + d1['spurious_C']
    total_rec_1 = d1['correct_A'] + d1['partial_A'] + d1['missing_A'] + d1['correct_B'] + d1['incorrect_B'] + d1['correct_C'] + d1['missing_C']
    correct_1 = d1['correct_A'] + 0.5 * d1['partial_A'] + d1['correct_B'] + d1['correct_C']

    total_pre_2 = d2['correct_B'] + d2['incorrect_B'] + d2['correct_C'] + d2['spurious_C']
    total_rec_2 = d2['correct_B'] + d2['incorrect_B'] + d2['correct_C'] + d2['missing_C']
    correct_2 = d2['correct_B'] + d2['correct_C']

    total_pre_3 = d3['correct_C'] + d3['spurious_C']
    total_rec_3 = d3['correct_C'] + d3['missing_C']
    correct_3 = d3['correct_C']

    total_pre = total_pre_1 + total_pre_2 + total_pre_3
    total_rec = total_rec_1 + total_rec_2 + total_rec_3
    correct = correct_1 + correct_2 + correct_3

    pre = correct / total_pre if total_pre > 0 else 0
    rec = correct / total_rec if total_rec > 0 else 0

    return 2 * pre * rec / ( pre + rec ) if ( pre + rec ) > 0 else 0


def evaluate_participant(submit_folder):
    scenario1 = evaluate_1("scenario1.txt", gold_folder / "scenario1-ABC", submit_folder / "scenario1-ABC")
    scenario2 = evaluate_2("scenario2.txt", gold_folder / "scenario2-BC", submit_folder / "scenario2-BC")
    scenario3 = evaluate_3("scenario3.txt", gold_folder / "scenario3-C", submit_folder / "scenario3-C")

    compute_taskA(scenario1)
    compute_taskB(scenario1)
    compute_taskC(scenario1)
    compute_scenario1(scenario1)

    compute_taskB(scenario2)
    compute_taskC(scenario2)
    compute_scenario2(scenario2)

    compute_taskC(scenario3)
    compute_scenario3(scenario3)

    result = dict()
    update(result, scenario1, 'S1')
    update(result, scenario2, 'S2')
    update(result, scenario3, 'S3')

    result['Name'] = submit_folder.name.split('-')[0].strip()
    result['Z-average_f1'] = ( scenario1['total_micro_f1'] + scenario2['total_micro_f1'] + scenario3['total_micro_f1'] ) / 3
    result['Z-average_tasks'] = ( scenario1['task_A_f1'] + scenario2['task_B_acc'] + scenario3['task_C_f1'] ) / 3
    result['Z-micro_f1'] = compute_micro_f1(scenario1, scenario2, scenario3)

    return result


def evaluate_all():
    results = []

    for folder in build_participants_table():
        results.append(evaluate_participant(folder))

    keys = list(results[0].keys())
    keys.sort()

    with open('results.tsv', 'w') as fp:
        for key in keys:
            fp.write(key + "\t")
            for item in results:
                v = item[key]

                if isinstance(v, str):
                    fp.write(v)
                elif isinstance(v, int):
                    fp.write(str(v))
                elif isinstance(v, float):
                    fp.write("%.3f" % v)

                fp.write("\t")
            fp.write("\n")


if __name__ == '__main__':
    evaluate_all()
