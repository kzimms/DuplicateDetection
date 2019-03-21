# Duplicate Detection 
### Via Data Similarity Mapping

Due to poor and varied governance across heritage systems, master data was highly inconsistent within and across systems. Differences in encoding conventions complicate the use of out-of-the-box SAP tools for duplicate detection.

The implementation of an unsupervised machine learning model allows duplicate detection without comprehensive (or any) data cleansing on data that may end up being culled or consolidated. This approach is effective for any application in which similar natural language data records need to be grouped together at varying levels of granularity. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project was coded in Python 2.7 although, with minor modifications, could be run in Python 3.6. The below pre-requisites assume the user has a current version of pip installed. 

### Prerequisites

Python 2.7

```
Python --version
2.7.15
```

pip 

```
pip --version
pip 9.0.3 from c:\python27\lib\site-packages (python 2.7)
```
pip will allow you to easily download all of the dependencies for this code base. pip should install when you download python. However, if it does not, follow the download directions here: https://packaging.python.org/tutorials/installing-packages/

The packages and dependencies of this project are:
NumPy, SciPy, Pandas, MatPlotLib, NLTK, PyHDB, scikit-learn

If you do not have one of these installed please install via pip:
```
pip install {package name}
```


### Running the Scripts

A step by step series of examples that tell you how to get a development env running

If you already have csv files of data that you wish to find duplicates in, skip to the next step. If your data is not saved in a HANA database, you will need to write your own script to either pull it into a pandas dataframe or save it to a csv and then start from the next step. 

To pull in data from HANA and save it as a csv file, edit the top of Hana_query.py, save it, and run in the command line. The first four lines provide the necessary information to connect to the correct HANA server. The fifth line specifies a SQL query to run on the HANA server to create the desired datatable. The last two lines refer to your local machine and specify the folder and file name for the datatable to be saved. 

```
######### ALL CHANGES IN THIS BLOCK ###########################
HANAhost = "XX.XXX.XX.XXX"      # put host number in "quotes"
HANAport = 30115                # keep port number as integer
HANAuser = ""             # put username in "quotes"
HANApassword = ""     # put password in "quotes"
SQLquery = ""         # SQL query that would be used in HANA to access data
masterData = ""         # Folder where the data will be saved
fileName = ""           # base of the file name where pull will be saved
###############################################################
```
```
python Hana_query.py
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Authors

* **Kathryn Zimmerman** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* Deepak Nagarajan for his thoughts and insights as this solution came together. 
