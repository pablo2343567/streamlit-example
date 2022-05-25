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


df = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d99.csv')

df99 = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d.csv')

dft = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/t.csv')





dft[0]
