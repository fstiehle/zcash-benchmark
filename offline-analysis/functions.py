import statistics as stat
import pandas as pd

def group_block(timings, block_index='BLOCK', time_index='NS'):
  timings[time_index + '_median'] = timings[time_index].groupby(timings[block_index]).transform('median')
  timings[time_index + '_sum'] = timings[time_index].groupby(timings[block_index]).transform('sum')
  timings = timings.drop(columns=time_index)
  timings = timings.drop_duplicates()
  return timings