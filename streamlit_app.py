import streamlit as st
import pandas as pd

from collections import namedtuple
import altair as alt
import math

import operator
import matplotlib as plt
import numpy as np
import pygal
import xlrd
from pygal.style import Style


df = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d99.csv',na_values='NA', keep_default_na=False)

df99 = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d.csv',na_values='NA', keep_default_na=False)

dft = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/t.csv',na_values='NA', keep_default_na=False)




a = list ( dft.loc['Paises'] )

a



