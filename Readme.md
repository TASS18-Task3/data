# Development data for TASS-2018 Task 3: eHealth Knowledge Discovery

This repository contains the training data for the Task 3 in TASS 2018.
The files and folders are organized as follows:

* [`trial`](/trial) contains relevant files for the trial phase.
* [`training`](/training)  contains relevant files for the training phase.
* [`training_example`](/training_example)  contains an example training phase, as it appears in the website.
* [`test`](/test)  contains relevant files for the test phase.
* [`develop`](/develop)  contains additional training files useful for fine-tunning or model selection.
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

## Training phase

During the training phase the folder `training` will contain the reference files that are needed to train a model. Inside this folder you will find three sub-folders:

* `input` contains all the `input_*.txt` files with plain text.
* `gold` contains all the reference `output_*.txt` files for the three tasks, that you should use to train your models.
* `submit` is an empty folder where you are expected to place your own `output_*.txt` for using the supplied [evaluation script](/score_training.py)

### Training data statistics

The current version of the training dataset contains a total of **559 sentences** and **5673 annotations**. More details are provided in the next tables:

Entity | 3276
-------|-----
Action | 849
Concept | 2427

Relation | 1012
---------|-----
Is-a | 434
Part-of | 149
Property-of | 399
Same-as | 30

Roles | 1385
---------|-----
Subjects | 599
Targets | 786

### Training evaluation

The file `score_training.py` performs an automatic evaluation of your output files against the gold files. You can use this script to validate your technique(s). The metrics reported are exactly the same ones that will be used in the final evaluation. This script simply evaluates each pair of gold/dev files separately and outputs detailed information of all the mistakes. This file's output corresponds to the `Development evaluation...` sections in each of the subtasks.

To run it simply use:

```bash
python3 score_training.py [training-folder]
```

If the optional arg `training-folder` is provided, then the files are looked for in that folders instead of the default `training`. You can use these options to test different variants or to see the evaluation for the example files, by running:

```bash
python3 score_training.py training_example
```

### Training submissions

During the Training phase you are expected to submit the outputs your technique produces on the training set into Codalab to test the workflow and get used to the formats. Please make sure to try at least once to submit these files on your own. To prepare a submission, you should zip the contents on the `submit` folder in a `.zip` file and send them through Codalab's interface. The content of the `zip` file should be **only** the three folders `scenario*` with their respective content, as illustrated below:

```
submission.zip/
    scenario1-ABC/
        output_A_*.txt
        output_B_*.txt
        output_C_*.txt
    scenario2-BC/
        output_B_*.txt
        output_C_*.txt
    scenario3-C/
        output_C_*.txt
```

> **Make sure** not to mistakenly zip the `submit` folder *itself*, but only **it's content**.

For simplicity, there is `Makefile` that creates the right `zip`. Just running `make` inside the projects root folder should work.

### Baseline implementation

Inside the `baseline` folder you will find a naive implementation of the whole process. This implementation simply counts the number of occurrences of all concepts, actions and relations, and uses these statistics to match the exact same occurrences. Hence, it can be used as a minimal baseline of the expected score in each evaluation scenario.

To run it, `cd` into the `baseline` folder and execute:

```bash
python3 main.py
```

> **(!) BEWARE** that running this script will **overwrite** your `submit` folder with its output.

### Development corpus

An additional 285 sentences are included in the `develop` folder. These sentences are also fully tagged, and are meant to be used for model selection and parameter tunning. We encourage participants to try different models, algorithms, and parameter settings. Each of these different variants should be trained on the **training corpus** only, and then their performance measured on the **development corpus**, to select the best variant. This separation ensures first a fair comparison among participants. Furthermore, comparting different models on a development corpus, independent from the training corpus, also helps reducing the risk of overfitting, and will give you a more accurate estimate of the actual performance of your models.

### Training score

The file `score_test.py` performs the final evaluation exactly as described in the competition rules, i.e., according to the three evaluation scenarios presented. It assumes the reference files are in a `gold` subdirectory and the files to be submitted are in the `submit` folder, according to the folder structure presented there. This file's output is the one actually used in `Codalab` to rank competitors.

This script will output a file `score.txt` that contains the calculated metrics described in the `Overall evaluation...` section of the competition rules.

## Testing phase

> **(!)** The testing phase is already open in Codalab. This phase is blind reviewed, hence you won't be able to see your results until May 28th when all results will be published.

This folder contains the **test** files divided in the corresponding scenarios, following the same structure as presented in the [trial folder](#trial-phase). For each evaluation scenario there is a single input file. Each file contains 100 sentences (300 sentences in total), randomly selected from the original corpus. None of these sentences have been published before either in the training or development corpora. However, the test corpus has been built with care, to guarantee there is a certain level of overlap (in terms of the concepts and relations) with the training and development corpora, but there are also brand new concepts and relations tuples which do not appear in the training set.

* `input` contains the relevant input files:
    * `scenario1-ABC` contains **only** the `input_scenario1.txt`.
    * `scenario2-BC` will contain input files **and** the corresponding `output_A_*.txt` files.
    * `scenario3-C` will contain input files **and** the corresponding `output_A_*.txt` files **and also** the corresponding `output_B_*.txt` files .
* `submit` will contain empty subfolders where you should place your output files:
    * `scenario1-ABC` where you should place the `output_A_*.txt`, `output_B_*.txt` and `output_C_*.txt` files for the scenario 1 evaluation.
    * `scenario2-BC` where you should place the `output_B_*.txt` and `output_C_*.txt` files for the scenario 2 evaluation.
    * `scenario3-C` where you should place the `output_C_*.txt` files for the scenario 3 evaluation.

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

For your convenience, there is `Makefile` in the root project folder to help you prepare the submission data. Just run `make` and the content of the `test/submit` folder will be correctly zipped in the structure that Codalab is expecting.

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

#### NLM Copyright Information

> Government information at NLM Web sites is in the public domain. Public domain information may be freely distributed and copied, but it is requested that in any subsequent use the National Library of Medicine (NLM) be given appropriate acknowledgement. When using NLM Web sites, you may encounter documents, illustrations, photographs, or other information resources contributed or licensed by private individuals, companies, or organizations that may be protected by U.S. and foreign copyright laws. Transmission or reproduction of protected items beyond that allowed by fair use as defined in the copyright laws requires the written permission of the copyright owners. Specific NLM Web sites containing protected information provide additional notification of conditions associated with its use.
