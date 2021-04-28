import statistics as stat
from sklearn.metrics import mean_absolute_error, median_absolute_error
import pandas as pd
import numpy as np

def group_block(timings, block_index='BLOCK', time_index='NS'):
  timings[time_index + '_median'] = timings[time_index].groupby(timings[block_index]).transform('median')
  timings[time_index + '_sum'] = timings[time_index].groupby(timings[block_index]).transform('sum')
  timings = timings.drop(columns=time_index)
  timings = timings.drop_duplicates()
  return timings

# From: https://stackoverflow.com/a/40341529
def subset_by_iqr(df, column, whisker_width=1.5):
  """Remove outliers from a dataframe by column, including optional 
      whiskers, removing rows for which the column value are 
      less than Q1-1.5IQR or greater than Q3+1.5IQR.
  Args:
      df (`:obj:pd.DataFrame`): A pandas dataframe to subset
      column (str): Name of the column to calculate the subset from.
      whisker_width (float): Optional, loosen the IQR filter by a
                              factor of `whisker_width` * IQR.
  Returns:
      (`:obj:pd.DataFrame`): Filtered dataframe
  """
  # Calculate Q1, Q2 and IQR
  q1 = df[column].quantile(0.25)                 
  q3 = df[column].quantile(0.75)
  iqr = q3 - q1
  # Apply filter with respect to IQR, including optional whiskers
  filter = (df[column] >= q1 - whisker_width*iqr) & (df[column] <= q3 + whisker_width*iqr)
  return df.loc[filter]    


def mean_absolute_error_percent(y_true, y_pred):
  return mean_absolute_error(y_true, y_pred) / y_true.mean() * 100

def max_error(y_true, y_pred):
  errors = y_true - y_pred
  return errors.max()

def median_absolute_error_percent(y_true, y_pred):
  return median_absolute_error(y_true, y_pred) / y_true.median() * 100

# From: https://gist.github.com/powerlim2/5622563
def adj_r2_score(model,y,yhat):
  """Adjusted R square — put fitted linear model, y value, estimated y value in order
  
    Example:
    In [142]: metrics.r2_score(diabetes_y_train,yhat)
    Out[142]: 0.51222621477934993

    In [144]: adj_r2_score(lm,diabetes_y_train,yhat)
    Out[144]: 0.50035823946984515"""
  from sklearn import metrics
  adj = 1 - float(len(y)-1)/(len(y)-len(model.coef_)-1)*(1 - metrics.r2_score(y,yhat))
  return adj