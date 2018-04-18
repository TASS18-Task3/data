.PHONY : training clean

training:
	(cd ../data/training/dev && zip -r - *) > training.zip

clean:
	cd training/submit ; rm scenario1-ABC/*.txt ; rm scenario2-BC/*.txt ; rm scenario3-C/*.txt