all: training.zip test.zip

training.zip: training/submit/*
	(cd ../data/training/submit && zip -r - *) > training.zip

test.zip: test/submit/*
	(cd ../data/test/submit && zip -r - *) > test.zip

clean:
	cd training/submit ; rm scenario1-ABC/*.txt ; rm scenario2-BC/*.txt ; rm scenario3-C/*.txt
	cd test/submit ; rm scenario1-ABC/*.txt ; rm scenario2-BC/*.txt ; rm scenario3-C/*.txt