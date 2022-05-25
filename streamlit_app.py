from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import operator
import matplotlib as plt
import numpy as np
import pygal
import xlrd
from pygal.style import Style

url = 'https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/datos.csv'   
df = pd.read_csv(url,index_col=0)
