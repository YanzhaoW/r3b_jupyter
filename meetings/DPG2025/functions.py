import itertools
import numpy as np
import pandas as pd


def convert_2d_to_arrays(histgram):
    nbinsy = histgram.GetNbinsY()
    nbinsx = histgram.GetNbinsX()
    total_size = nbinsy * nbinsx
    x_data = np.zeros(nbinsx)
    y_data = np.zeros(nbinsy)
    z_data = np.zeros((nbinsy, nbinsx))
    for index in range(nbinsx):
        x_data[index] = histgram.GetXaxis().GetBinCenter(index + 1)
    for index in range(nbinsy):
        y_data[index] = histgram.GetYaxis().GetBinCenter(index + 1)
    for idx_x, idx_y in itertools.product(range(1, nbinsx), range(1, nbinsy)):
        z_data[idx_y, idx_x] = histgram.GetBinContent(idx_x + 1, idx_y + 1)
    return x_data, y_data, z_data

def convert_1d_to_df(histgram):
    nbinsx = histgram.GetNbinsX()
    x_data = np.zeros(nbinsx)
    y_data = np.zeros(nbinsx)

    for index in range(0, nbinsx):
        x_data[index] = histgram.GetBinCenter(index + 1)
        y_data[index] = histgram.GetBinContent(index + 1)

    return pd.DataFrame({"x": x_data, "y": y_data})
        


def convert_to_df(hist):
    num_of_bins = hist.GetNbinsX()

    x_vals = np.zeros(num_of_bins)
    y_vals = np.zeros(num_of_bins)
    y_sums = np.zeros(num_of_bins)

    sum_val = 0.0

    for index in range(0, num_of_bins):
        x_vals[index] = hist_proj.GetBinCenter(index + 1)
        y_vals[index] = hist_proj.GetBinContent(index + 1)
        sum_val += y_vals[index]
        y_sums[index] = sum_val

    y_sums = y_sums / sum_val

    return pd.DataFrame({"x": x_vals, "y": y_vals, "CDF": y_sums})