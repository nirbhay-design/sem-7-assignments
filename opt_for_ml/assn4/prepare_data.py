import numpy as np
import pandas as pd
import os

stocks_32_months = ["data_2months/AWL.NS.csv", "data_2months/MRPL.NS.csv","data_2months/BHARTIARTL.NS.csv"]
stocks_52_months = list(map(lambda x:os.path.join("data_2months",x),os.listdir("data_2months/")))
stocks_54_months = list(map(lambda x:os.path.join("data_4months",x),os.listdir("data_4months/")))


def save_stocks(csv_files, final_csv_file):
    csv_data = {}
    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        np_data = np.array(data)
        csv_data[csv_file] = np_data[:,-3]
    df = pd.DataFrame(csv_data)
    df.to_csv(final_csv_file,index=False)

save_stocks(stocks_32_months, "que1_data.csv")    
save_stocks(stocks_52_months, "que2_data.csv")    
save_stocks(stocks_54_months, "que3_data.csv")    