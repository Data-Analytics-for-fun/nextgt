# nextgt
First try with FinTech-Data

### Installation
> the requirement is to install some open libraries: 
- Pandas: https://github.com/pandas-dev/pandas
- matplotlib: https://github.com/matplotlib/matplotlib
- sklearn: https://github.com/scikit-learn/scikit-learn

### Run
> python analyse.py 

- this script is develop specifically for this test-data set. will have some following features: 
1. Import data from csv-file, look up all NaN values in data (rows, columns) and tell us where NaN data is.
The result is found at column 'Sub_fund_long_name'.
2. Re-select the columns without this column
3. Following the task, we find all rows of instrument 2A which might have missing data (NaN-values)
4. Calculate Correlation of all 11 instruments 1A, 1B, 1C, etc. and export all results as json-format 
5. Convert data to time-series data 
6. Normalize and visualize data by column and export result as png-image-format.

- Notice: run this file at local also output result at console. 
