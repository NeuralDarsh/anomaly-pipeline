import sys

print("Python version:", sys.version)

import pandas
import numpy
import sklearn
import xgboost
import joblib
import matplotlib
import redis
import streamlit

print("pandas      :", pandas.__version__)
print("numpy       :", numpy.__version__)
print("scikit-learn:", sklearn.__version__)
print("xgboost     :", xgboost.__version__)
print("joblib      :", joblib.__version__)
print("matplotlib  :", matplotlib.__version__)
print("redis       :", redis.__version__)
print("streamlit   :", streamlit.__version__)

print()
print("All libraries are installed correctly. Level 0 is complete!")