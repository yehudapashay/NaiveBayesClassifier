# NaiveBayesClassifier
Naive Bayes Classifier implementaion

<H2> Prerequisites </H2>

In the project we have used in:Python 2.7 and pndas.
*	Python 2.7 .
* pandas 0.24.2 .

<H2>Files description</H2>

* Structure - A file that describes the constituent features of each record in the database -includes the target value that appears last in the list.
The file is used by the program to study the database structure it needs to handle .
* train - A file that contain the records that will be used to build the classifier.
* test - A file that contain the records that the program will classify.

<H2> Running </H2>

For running the program please run the GUI file.

Use the ‘Browse’ buttons to choose the folder T that contains the following files:
* Structure.txt
* train.csv
* test.csv
Fill the number of discretization bins.
Choose the ‘Build’ button to build the classifier, and then choose the ‘Classify button to classify the records in the test file.

![p7](https://user-images.githubusercontent.com/44204651/62790241-55b06480-bad3-11e9-86b5-71d6083cf039.JPG)

<H2>The classification process</H2>

The program will read the ‘Structure’ file, thus concluding the model structure that it will be classified.
Once the model structure is loaded, the program will load the ‘train’ file and separate for each record its various attributes.
After reading the files, the data cleaning step will be followed which will include the following steps:

<H3>1.Complete missing values:</H3>
  
* For numeric values - average value of all records belonging to the same class.
* For categorical values - the most common value.

<H3>2.Discretization:</H3>
  
We will do the discretization process for each numeric variable by the amount of bins received from the user. We'll use Equal-width Partitioning.

<H3>Results</H3>

After pressing the Predicate button, the program will read the ‘test’ file and classify its records according to the Naïve Bayes algorithm using m-estimator (m=2).
The classification results will be found in the ‘output’ file so that each row in the file contains the record number and classification given to it by the algorithm.

