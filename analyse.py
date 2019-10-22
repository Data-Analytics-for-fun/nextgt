import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def nan_columns(data):
       """
       Description: return name of all columns which have NaN_value
       :param data: pandas.core.frame.DataFrame
       :return: list of all possible NaN_column(s)
       """
       nan_bool = data.isnull().any()
       if isinstance(data, pd.DataFrame):
              key_true = [key for key, value in nan_bool.iteritems() if value]
              return key_true
       else:
              return nan_bool

def nan_rows(data, nan=True):
       """
       Description: return all rows containing NaN values in type DataFrame
       :param data: pandas.core.frame.DataFrame
       :param nan: Boolean-input True to search for NaN values, False to search and drop that row
       :return: data with all possible found NaN_rows or without the NaN_rows (if nan=False)
       """
       if isinstance(data, pd.DataFrame) and nan:     
              return data[data.isnull().any(axis=1)]

       elif isinstance(data, pd.DataFrame) and not nan:
              return data[data.notnull().any(axis=1)].dropna(axis=0, how='any')

       else:
              return data.isnull().any()  

def calc_Corr(data, instruments, save=True):
       """
       Description: calculate the correlation between the column NAV-share of the 11 instruments        
       :param data: pandas.core.frame.DataFrame
       :param instruments: list of all parameters in tuple-format (e.g. [(1, 'A'), (1, 'B'), (1, 'C')])
       """
       for inst in instruments:                     
              da = data[data['Sub-fund_code']==inst[0]]
              da = da[da['Share_code']==inst[1]]
              da.drop(['Sub-fund_code'], axis=1, inplace=True)
              output = da.corr(method ='pearson')
              
              # export correlation table to json-file
              if save:
                     output.to_json(str(inst[0])+inst[1]+'.json')

def vis_dat(data, column, saveimg):
       """
       Description: visualize time-series data (specific test) by column
       :param data: pandas.core.frame.DataFrame
       :param column: column as y-axis following time-series as x-axis
       :param saveimg: name of the saving image file
       """    
       # Normalize data using MinMaxScaler
       scaler = MinMaxScaler() 

       scaled_values = scaler.fit_transform(data[column].values.reshape(-1, 1)) 
       data.loc[:, column] = scaled_values

       # Optional: dat[column].plot(figsize=(15,10), marker='o', alpha=0.5, linestyle='-')
       data[column].plot(figsize=(25,10), linewidth=0.5)

       # Export to file image
       plt.savefig(saveimg+'.png')
       plt.show()

def run(datapath):
       """
       Description: read data from csv-file and convert to time series format
       :param datapath: path to location containing data in csv-format
       """
       ftdat = pd.read_csv(datapath)

       print("Find all columns that contains NaN values: {}".format(nan_columns(ftdat)))
       print("Find all rows that contains Nans values, number of rows with NaN values: {}".format(len(nan_rows(ftdat))))

       # Re-select the columns without containing NaN-values
       dat = ftdat[['Sub-fund_code', 'Share_code', 'Valuation_date', 'Sub-fund_currency',
                     'Net_assets_share_type', 'Numbre_of_Shares_outstanding', 'NAV_share',
                     'CCY_NAV_share', 'Isin_code', 'NUMBER_unit_subsc', 'Amount_subsc',
                     'NUMBER_unit_repurch', 'Amount_unit_repurch',
                     'Dividend_share', 'Date_pay_div', 'Pccy_dividend_share',
                     'Payment_dividend_ccy', 'Sub-fund_dividend_ccy', 'Total_Net_Assets']]       
       
       # Find and remove all rows of instrument 2A which has missing data
       missing = dat[dat['Sub-fund_code']==2]
       print("After reselect the new columns, check all rows with NaN values: ", len(nan_rows(missing[missing['Share_code']=='A'], "\n")))
       
       # Calculate Correlation
       instruments = [(1, 'A'), (1, 'B'), (1, 'C'), (1, 'D'), (2, 'A'), (2, 'B'), (2, 'C'), (2, 'D'), (2, 'E'), (3, 'A'), (3, 'B')]
       calc_Corr(dat, instruments)

       # Create new data from original data and convert to time-series data
       df = dat[['Valuation_date', 'Net_assets_share_type', 'Numbre_of_Shares_outstanding', 'NAV_share', 'NUMBER_unit_subsc', 'Amount_subsc', 'NUMBER_unit_repurch', 'Amount_unit_repurch', 'Dividend_share', 'Date_pay_div', 'Pccy_dividend_share',
              'Payment_dividend_ccy', 'Total_Net_Assets']]                     
       # FIX WARNING: df.loc[:, 'Year'] = [t.split('/')[2] for t in df['Valuation_date']]
       df = df.assign(Year = [t.split('/')[2] for t in df['Valuation_date']])
       # FIX WARNING: df.loc[:, 'Month'] = [t.split('/')[1] for t in df['Valuation_date']]
       df = df.assign(Month = [t.split('/')[1] for t in df['Valuation_date']])
       # FIX WARNING: df.loc[:, 'Day'] = [t.split('/')[0] for t in df['Valuation_date']]
       df = df.assign(Day=[t.split('/')[0] for t in df['Valuation_date']])
              
       df.loc[:, 'Time'] = pd.to_datetime(dict(year=df.Year, month=df.Month, day=df.Day))
       df.drop(['Year', 'Month', 'Day'], axis=1, inplace=True)
       df.index = pd.to_datetime(df.pop('Time'), unit='ms')

       # Visualize data
       vis_dat(df, 'NAV_share', 'save_NAV_share')

if __name__ == '__main__':
       datapath = "./data/ngt_test_example_data.csv"
       run(datapath)
