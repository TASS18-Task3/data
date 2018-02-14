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

In the trial phase, we are releasing an example input file and all the relevant output files, that can be used by participants to understand the competition workflow and the files format. All the relevant files are located in the `trial` folder. In this folder you'll find three subfolders:

* [`input`](/trial/input) contains the input files that you will receive for each evaluation scenario. The purpose of this folder is to illustrate how participants should expect the input files to be structured in the [test phase](#test-phase).

    * [`scenario1-ABC`](/trial/input/scenario1-ABC) contains the files to be submitted for the scenario 1 evaluation.
        * [`input_trial.txt`](/trial/input/scenario1-ABC/input_trial.txt) is plain text.
    * [`scenario2-BC`](/trial/input/scenario2-BC) contains the files to be submitted for the scenario 2 evaluation.
        * [`input_trial.txt`](/trial/input/scenario2-BC/input_trial.txt) is plain text.
        * [`output_A_trial.txt`](/trial/input/scenario2-BC/output_A_trial.txt) is the gold output for task A.
    * [`scenario3-C`](/trial/input/scenario3-C) contains the files to be submitted for the scenario 3 evaluation.
        * [`input_trial.txt`](/trial/input/scenario3-C/input_trial.txt) is plain text.
        * [`output_A_trial.txt`](/trial/input/scenario3-C/output_A_trial.txt) is the gold output for task A.
        * [`output_B_trial.txt`](/trial/input/scenario3-C/output_B_trial.txt) is the gold output for task B.

* [`submit`](/trial/submit) contains the outputs files that you should submit for each evaluation scenario. The purpose of this folder is to illustrate how participants should submit their output to Codalab in the [test phase](#test-phase).
    * [`scenario1-ABC`](/trial/submit/scenario1-ABC) contains the files to be submitted for the scenario 1 evaluation.
        * [`output_A_trial.txt`](/trial/submit/scenario1-ABC/output_A_trial.txt) is the expected output file for task A in scenario 1.
        * [`output_B_trial.txt`](/trial/submit/scenario1-ABC/output_B_trial.txt) is the expected output file for task B in scenario 1.
        * [`output_C_trial.txt`](/trial/submit/scenario1-ABC/output_C_trial.txt) is the expected output file for task C in scenario 1.
    * [`scenario2-BC`](/trial/submit/scenario2-BC) contains the files to be submitted for the scenario 2 evaluation.
        * [`output_B_trial.txt`](/trial/submit/scenario2-BC/output_B_trial.txt) is the expected output file for task B in scenario 2.
        * [`output_C_trial.txt`](/trial/submit/scenario2-BC/output_C_trial.txt) is the expected output file for task C in scenario 2.
    * [`scenario3-C`](/trial/submit/scenario3-C) contains the files to be submitted for the scenario 3 evaluation.
        * [`output_C_trial.txt`](/trial/submit/scenario3-C/output_C_trial.txt) is the expected output file for task C in
        scenario 3.

* [`gold`](/trial/gold) contains the reference files used by the competition evaluator to compare against and score the submitted files. These are just the plain text and outputs for each of the tasks.

### Trial submissions

During the Trial phase you are expected to submit this trial outputs into Codalab to test the workflow and get used to the formats. Please make sure to try at least once to submit these files on your own. To prepare a submission, you should zip the contents on the `submit` folder in a `.zip` file and send them through Codalab's interface. The content of the `zip` file should be **only** the three folders `scenario*` with their respective content, as illustrated below:

```
submission.zip/
    scenario1-ABC/
        output_A_trial.txt
        output_B_trial.txt
        output_C_trial.txt
    scenario2-BC/
        output_B_trial.txt
        output_C_trial.txt
    scenario3-C/
        output_C_trial.txt
```

[This file](https://github.com/TASS18-Task3/data/releases/download/trial-v1.0/sample_trial.zip) is a sample `.zip` with exactly the trial output in the exact format that should be uploaded to Codalab.

> **Make sure** not to mistakenly zip the `submit` folder *itself*, but only **it's content**.

### Trial score

The file `score_test.py` performs the final evaluation exactly as described in the competition rules, i.e., according to the three evaluation scenarios presented. It assumes the reference files are in a `gold` subdirectory and the files to be submitted are in the `submit` folder, according to the folder structure presented there. This file's output is the one actually used in `Codalab` to rank competitors.

This script will output a file `score.txt` that contains the calculated metrics described in the `Overall evaluation...` section of the competition rules.

## Training phase

During the training phase the folder `training` will contain the reference files that are needed to train a model. Inside this folder you will find three sub-folders:

* `input` contains all the `input_*.txt` files with plain text.
* `gold` contains all the reference `output_*.txt` files for the three tasks, that you should use to train your models.
* `dev` is an empty folder where you are expected to place your own `output_*.txt` for using the supplied [evaluation script](/score_training.py)

> **NOTE** the training data is not ready yet, in its place we are distributing an `example_training` folder that follows the same structure, so that participants can test the evaluation script and get used to the workflow and formats.

### Training evaluation

The file `score_training.py` performs an automatic evaluation of your output files against the gold files. You can use this script to validate your technique(s). The metrics reported are exactly the same ones that will be used in the final evaluation. This script simply evaluates each pair of gold/dev files separately and outputs detailed information of all the mistakes. This file's output corresponds to the `Development evaluation...` sections in each of the subtasks.

To run it simply use:

```bash
python3 score_training.py [training-folder]
```

If the optional arg `training-folder` is provided, then the files are looked for in that folders instead of the default `training`. You can use these options to test different variants or to see the evaluation for the example files, by running:

```bash
python3 evaluate.py training_example
```

## Testing phase

This folder will contain the **test** files divided in the corresponding scenarios, following the same structure as presented in the [trial folder](#trial-phase):

* `input` will contain the relevant input files:
    * `scenario1-ABC` will contain **only** `input_*.txt` files.
    * `scenario2-BC` will contain input files **and** the corresponding `output_A_*.txt` files.
    * `scenario3-C` will contain input files **and** the corresponding `output_A_*.txt` files **and also** the corresponding `output_B_*.txt` files .
* `submit` will contain empty subfolders where you should place your output files:
    * `scenario1-ABC` where you should place the `output_A_*.txt`, `output_B_*.txt` and `output_C_*.txt` files for the scenario 1 evaluation.
    * `scenario2-BC` where you should place the `output_B_*.txt` and `output_C_*.txt` files for the scenario 2 evaluation.
    * `scenario3-C` where you should place the `output_C_*.txt` files for the scenario 3 evaluation.

> **NOTE:** The testing data is not ready yet, but will be included in due time in the `testing` folder.

### Submissions

During the Test phase you are expected to submit the final outputs into Codalab to for grading. To prepare a submission, you should zip the contents on the `submit` folder in a `.zip` file and send them through Codalab's interface. The content of the `zip` file should be **only** the three folders `scenario*` with their respective content, as illustrated below:

```
submission.zip/
    scenario1-ABC/
        output_A_trial.txt
        output_B_trial.txt
        output_C_trial.txt
    scenario2-BC/
        output_B_trial.txt
        output_C_trial.txt
    scenario3-C/
        output_C_trial.txt
```

[This file](https://github.com/TASS18-Task3/data/releases/download/trial-v1.0/sample_trial.zip) is a sample `.zip` with exactly the trial output in the exact format that should be uploaded to Codalab.

> **Make sure** not to mistakenly zip the `submit` folder *itself*, but only **it's content**.

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
    <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
</a>
<br />
<span>Copyright (c) 2018 University of Alicante &amp; University of Havana.</span> <br>
<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">TASS-2018 Task3 eHealth KD Corpus</span> is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<br />Based on a work at
<a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/tass18-task3/data" rel="dct:source">https://github.com/tass18-task3/data</a>.

### External resources from MedlinePlus

Corpus data has been gathered from [MedlinePlus.gov](https://medlineplus.gov/index.html) and manually post-processed.

**NLM Copyright Information**

> Government information at NLM Web sites is in the public domain. Public domain information may be freely distributed and copied, but it is requested that in any subsequent use the National Library of Medicine (NLM) be given appropriate acknowledgement. When using NLM Web sites, you may encounter documents, illustrations, photographs, or other information resources contributed or licensed by private individuals, companies, or organizations that may be protected by U.S. and foreign copyright laws. Transmission or reproduction of protected items beyond that allowed by fair use as defined in the copyright laws requires the written permission of the copyright owners. Specific NLM Web sites containing protected information provide additional notification of conditions associated with its use.

