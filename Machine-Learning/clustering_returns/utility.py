#%%
import pandas as pd
# Load Data
def load_data():
    df = pd.read_csv("../data/48_Industry_Portfolios_daily.CSV", sep = ',')

    # Build the Dataframe
    df.rename(columns={"#,na_values =' NaN'": "date"},inplace=True)
    df.columns = [column.strip() for column in df.columns]
    df['date'] = pd.to_datetime(df['date'],format = '%Y%m%d')
    df.set_index('date', inplace = True)
    return df/100

# # Example
# df = load_data()
# df.head()