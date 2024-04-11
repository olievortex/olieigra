"""Command to process raw IGRA data into a features file and a li prediction file"""
from datetime import datetime
import math
import os
import numpy as np
import pandas as pd

from metpy.calc import lifted_index, parcel_profile
from metpy.units import units

from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.preprocessing import StandardScaler

from datasource_igra_csv import DatasourceIgraCsv
from datasource_igra_raw import DatasourceIgraRaw


def clean_dataset(features_filename: str, prediction_filename: str):
    """Clean the features and predictions and save the results"""
    df = pd.read_csv(features_filename)
    df['li'] = pd.read_csv(prediction_filename)

    # Remove data with NaN values
    df = df.dropna()

    # Separate the datasets
    x = df.drop(['date', 'hour', 'li'], axis=1)
    y = df['li'].values

    # Scale the X dataset
    ss = StandardScaler()
    x = ss.fit_transform(x)

    # Select the best 50 features
    skb = SelectKBest(mutual_info_regression, k=50)
    x = skb.fit_transform(x, y)

    # Save as numpy files
    np.save(features_filename.replace('.csv', '.npy'), x)
    np.save(prediction_filename.replace('.csv', '.npy'), y)


if __name__ == '__main__':
    ONEDRIVE = 'c:/Users/oliev/OneDrive/Documents/olievortex/data/igra'
    WORKSPACE = 'c:/workspace/ml/igra_madness/linreg_lifted_index'
    source_files = ['USM00072558-data.txt', 'USM00072649-data.txt']

    # Create the features file
    OlieIgraAnalyze.orchestrate_igra_analyze(ONEDRIVE, WORKSPACE, source_files)
    clean_dataset(f'{WORKSPACE}/igra-features.csv', f'{WORKSPACE}/igra-prediction-li.csv')
