.PHONY : training

training:
	(cd ../data/training/dev && zip -r - *) > training.zip

