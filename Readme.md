# Development data for TASS-2018 Task 3: eHealth Knowledge Discovery

This repository contains the training data for the Task 3 in TASS 2018.
The files and folders are organized as follows:

* [`trial`](/trial) contains relevant files for the trial phase.
* [`training`](/training)  contains relevant files for the training phase.
* [`training_example`](/training_example)  contains an example training phase, as it appears in the website.
* [`test`](/test)  contains relevant files for the test phase.
* [`score_training.py`](/score_training.py) is a Python 3 script that provides an evaluation useful for the training pahse (see [below](#training-phase)).
* [`score_test.py`](/score_test.py)  is a Python 3 script that provides the exact same evaluation as used in the Codalab competition (see [below](#trial-phase))

## Trial phase

In the trial phase, we released an example input file with all the relevant output files, that can be used by participants to understand the competition workflow and the files format. All the relevant files are located in the `trial` folder. In this folder you'll find three subfolders:

* `input` contains the input files that you will receive for each evaluation scenario:
    * `scenario1-ABC` contains the files to be used for the scenario 1 evaluation.
        * `input_trial.txt`: plain text.
    * `scenario2-BC` contains the files to be used for the scenario 2 evaluation.
        * `input_trial.txt`: plain text.
        * `output_A_trial.txt`: gold output for task A.
    * `scenario3-C` contains the files to be used for the scenario 3 evaluation.
        * `input_trial.txt`: plain text.
        * `output_A_trial.txt`: gold output for task A.
        * `output_B_trial.txt`: gold output for task B.

    The purpose of this folder is to illustrate how participants should expect the input files to be structured in the [test phase](#test-phase).

* `submit` contains the outputs files that you should submit for each evaluation scenario:
    * `scenario1-ABC` contains the files to be submitted for the scenario 1 evaluation.
        * `input_trial.txt`: plain text.
    * `scenario2-BC` contains the files to be submitted for the scenario 2 evaluation.
        * `input_trial.txt`: plain text.
        * `output_A_trial.txt`: gold output for task A.
    * `scenario3-C` contains the files to be submitted for the scenario 3 evaluation.
        * `input_trial.txt`: plain text.
        * `output_A_trial.txt`: gold output for task A.
        * `output_A_trial.txt`: gold output for task B.

    The purpose of this folder is to illustrate how participants should expect the input files to be structured in the [test phase](#test-phase).

## Development evaluation

The file `evaluate.py` performs an automatic evaluation of your output files against the gold files. You can use this script to validate your technique(s). The metrics reported are exactly the same ones that will be used in the final evaluation. This script simply evaluates each pair of gold/dev files separately and outputs detailed information of all the mistakes. This file's output corresponds to the `Development evaluation...` sections in each of the subtasks.

To run it simply use:

```bash
python3 evaluate.py [gold-folder] [dev-folder]
```

If the optional args `gold-folder` and `dev-folder` are provided, then the files are looked for in those folders instead of the default `gold` and `dev`. You can use these options to test different variants or to see the evaluation for the example files, by running:

```bash
python3 evaluate.py example/gold example/dev
```

## Final evaluation

The file `score.py` performs the final evaluation exactly as described in the competition rules, i.e., according to the three evaluation scenarios presented. It assumes the gold files are in `gold` and the files to be submitted are in the `submit` folder, according to the folder structure presented there. This file's output is the one actually used in `Codalab` to rank competitors.

```bash
python3 score.py gold/ submit/
```

This script will output a file `score.txt` in the `submit` folder that contains the calculated metrics described in the `Overall evaluation...` section of the competition rules.

## Training

The actual training data is not ready yet. Only the trial data is included in the `gold` folder now. This repository will be updated with the actual gold training files in due time.

You can use the trial data to see a more complex scenario than that presented in the examples, and to begin developing your ideas until the actual training data is ready.

**The trial data is not expected to be part of the final evaluation, just use it for your convenience now.**

## Testing

The testing data is not ready yet, but will be included in due time in the `testing` folder.
This folder will contain the **test** files divided in the corresponding scenarios:

* `scenario1-ABC` will contain **only** `input_*.txt` files.
* `scenario2-BC` will contain input files **and** the corresponding `output_A_*.txt` files.
* `scenario3-C` will contain input files **and** the corresponding `output_A_*.txt` files **and also** the corresponding `output_B_*.txt` files .
