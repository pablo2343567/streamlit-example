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

    
df = pd.read_excel('datos.csv')
