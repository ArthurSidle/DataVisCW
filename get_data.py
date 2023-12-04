import numpy as np
import pandas as pd
import concurrent
from dataset_loader import DatasetLoader


def get_steam_data():
    def get_data():
        dl = DatasetLoader("steam", "steam")
        steam_df = dl.decompress_data()
        steam_lost_df = pd.read_csv("data/steam_lost.csv", encoding="unicode_escape")

        steam_lost_df.set_index('AppID', inplace=True)

        return [steam_df.shape[0], steam_lost_df.shape[0]]

    with concurrent.futures.ThreadPoolExecutor(1) as executor:
        software_counts = executor.submit(get_data).result()
    
    data_out = {
        "percent": {
            "x": software_counts,
            "y": ["Available", "Lost"]
        }
    }

    return data_out

def get_delisters():
    df_out = pd.read_csv("final_data/serial_delisters.csv")
    df_out = df_out[0:10]
    return df_out