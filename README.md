# Impact Pre-training

This repository is the replication package of the work "Automating Code-Related Tasks Through Transformers: The Impact of Pre-training"

The `SLR` folder contains the material from the sistematic literature review. In particular:
  - `SLR/queries.numbers` contains the queries executed for each source;
  - `SLR/data` contains the collected papers.


The `code` folder contains the scripts to reproduce our experiments: In particular:
  - `code/training` contains the Google Colab scripts to run the pre-training and the fine-tuning. Note that you need a Pro Goggle Colab account tu succesfully run the scripts (on the TPUs);  
  - `code/cleaning` contains the scripts we used to clean the dataset;
  - `code/generate_mutants` contains all the necessary to generate mutants of given Java methods.


The `results` folder contains statistical analysis, BLEU score and Levenstein distance of the models predictions.


We stored all the processed data (pre-training datasets and fine-tuning datasets) on Zenodo, available at the following link https://zenodo.org/record/7052859#.YxdNkuxBxlZ
