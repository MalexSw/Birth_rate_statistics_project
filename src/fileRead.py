# main.py
import pandas as pd
import matplotlib.pyplot as plt
import re


def readFileBirthCountsByCountry():
    return pd.read_csv("data2.csv")

def findCountries(df):
    return df['geo'][df['geo'].str.fullmatch(r'[A-Z]{2}')].unique().tolist()


def readFileBirthCounts():
    file_path = 'data2.csv'
    df = pd.read_csv(file_path)
    birth_counts = df['OBS_VALUE']
    return birth_counts

def readFileBirthesOverYears():
    file_path = 'data2.csv'
    df = pd.read_csv(file_path)
    births_per_year = df.groupby('TIME_PERIOD')['OBS_VALUE'].sum()
    return births_per_year
        