# Training data for TASS18 Task 3

This repository contains the training data for the Task 3 in TASS 2018.
The files and folders are organized as follows:

* `evaluate.py` is a Python 3 script that performs the evaluation (see [below](#evaluation)).
* `gold/` contains the `input_*.txt` files and the corresponding `output_*.txt` files of the training data.
* `dev/` is an empty folder where you are expected to output your corresponding `output_*.txt` files.
* `example/` contains a example input and output files, with some errors purposedly included, that you can use to understand exactly how the evaluation metric works.
* `submit/` contains a sample submission (actually just the `trial` data splitted accordingly).

## Development evaluation

The file `evaluate.py` performs an automatic evaluation of your output files against the gold files. You can use this script to validate your technique(s). The metrics reported are exactly the same ones that will be used in the final evaluation. This script simply evaluates each pair of gold/dev files separately and outputs detailed information of all the mistakes.

To run it simply use:

```bash
python3 evaluate.py [gold-folder] [dev-folder]
```

If the optional args `gold-folder` and `dev-folder` are provided, then the files are looked for in those folders instead of the default `gold` and `dev`. You can use these options to test different variants or to see the evaluation for the example files, by running:

```bash
python3 evaluate.py example/gold example/dev
```

## Final evaluation

The file `score.py` performs the final evaluation exactly as described in the competition rules, i.e., according to the three evaluation scenarios presented. It assumes the gold files are in `gold` and the files to be submitted are in the `submit` folder, according to the folder structure presented there.

## Notes

The actual training data is not ready yet. Only the trial data is included in the `gold` folder now. This repository will be updated with the actual gold training files in due time.

You can use the trial data to see a more complex scenario than that presented in the examples, and to begin developing your ideas until the actual training data is ready.

**The trial data is not expected to be part of the final evaluation, just use it for your convenience now.**
