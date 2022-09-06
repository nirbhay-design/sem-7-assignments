import numpy as np
import pandas as pd
import os

stocks = list(map(lambda x:os.path.join("data_1year",x),os.listdir("data_1year/")))


def save_stocks(csv_files, final_csv_file):
    csv_data = {}
    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        print(csv_file,data.shape)
        np_data = np.array(data)
        csv_data[csv_file] = np_data[:,-3]
    df = pd.DataFrame(csv_data)
    df.to_csv(final_csv_file,index=False)

save_stocks(stocks, "homework_data.csv")    