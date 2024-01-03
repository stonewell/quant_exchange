#load stock data from vip data for cn_a
import pathlib
import pandas as pd

from stock_data_provider import load_history_from_file, save_history_to_file, to_history_file_path, get_all_history_file_in_path

from .vip_dataset import load_stock_data as vipdoc_loadstock_data
from .baostock_stock_basic_query import load_stock_info
from .path_config import module_path, data_path as g_data_path, vipdoc_path


def load_stock_data(symbol, do_normalize_data=True):
  stock_path = pathlib.Path(g_data_path) / symbol

  history_file_paths = get_all_history_file_in_path(stock_path)

  data = []
  for history_file in history_file_paths:
    df = load_history_from_file(history_file)

    data.append(df)

  all_df = pd.concat(data)

  all_df = all_df.loc[~all_df.index.duplicated(), :].sort_index().reset_index()

  return all_df
