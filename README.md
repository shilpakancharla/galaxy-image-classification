# Galaxy Image Classification: Comparison of Machine Learning and Deep Learning Techniques

Repository to store code written by Group 11 (CSC 522: Automated Learning & Data Analysis), Spring 2021 offered by Dr. Thomas Price.

Collaborators: Ishan Bhatt (ivbhatt), Pragna Bollam (pbollab), Meghana Kota (mkota), Shilpa Kancharla (skancha).

This repository contains the Python scripts that contains each task in the pipeline. 

## Files

* **sdss_image_captur.py**: uses the API provided by the Sloan Sky Observatory to get images of elliptical and spiral galaxies
* **webscrape_image_capture.py**: uses the proxycrawl python package to scrape images of irregular images from Google, also invalid images are scraped using this code (but different search strings)
* **augmenting_irregular_images.py**: performs data-augmentation on the images of irregular galaxies
* **combining_dataset.py**: combines the dataset (until this point images of different classes are stored in different formats in different places), resizes the images, standardizes everything.
* **pca.py**: Performs PCA (and PCA related experiments on the combined dataset)
* **svm_and_rf.py**: trains SVM & random forest models
* **mlp.py**: trains the MLP model
* **cnn.py**: trains the CNN model
* **demonstrate_nb.py**: used to fetch all trained models and generate predictions on same data
