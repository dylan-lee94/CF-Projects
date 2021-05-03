#%%
import numpy as np
import pandas as pd
import os

#%%
def generate_splits(returns, win_size,step_size):
    #Moving time window Setup
    num_steps = (len(returns)-win_size)//step_size

    # Generate indices for sliding window Train/Test split
    for j in range(0,num_steps*step_size,step_size):
        train_index = np.r_[j:j+win_size]
        test_index =  np.r_[j+win_size:j+win_size+step_size]
        yield (train_index,test_index) 


# # Example:
# ts = list(range(20))

# for train_index, test_index in generate_splits(ts,win_size=4,step_size=2):
#     print(train_index,test_index)

#%%
# Load Data
def load_data():
    os.chdir("../data")
    df = pd.read_csv("48_Industry_Portfolios_daily.CSV", sep = ',')

    # Build the Dataframe
    df.rename(columns={"#,na_values =' NaN'": "date"},inplace=True)
    df.columns = [column.strip() for column in df.columns]
    df['date'] = pd.to_datetime(df['date'],format = '%Y%m%d')
    df.set_index('date', inplace = True)
    return df

# # Example
# df = load_data()
# df.head()
