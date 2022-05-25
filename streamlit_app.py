import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/prueba.csv')
df.head()
print(df)
