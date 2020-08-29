import statistics as stat
import pandas as pd

def group_by_block(df, block_index=1, time_index=2):
    return df.groupby('BLOCK')['NS'].apply(list)

# Median percent of timing if block has occurence
def median_percent_of_block(sum_timings, blocks, block_index=1, time_index=2):
    data = {}
    for item in blocks.itertuples():
        block_hash = item[block_index]
        block_time = item[time_index]
        try:
            item_time = sum_timings.loc[block_hash]
            median_percent = stat.median(item_time) * 100 / block_time
            data[block_hash] = median_percent
        except KeyError:
            continue

    return pd.DataFrame.from_dict(data, orient='index', columns=["NS"])


# total percent of given timings if block has occurence
def total_percent_of_block(sum_timings, blocks, block_index=1, time_index=2):
  data = {}
  for item in blocks.itertuples():
      block_hash = item[1]
      block_time = item[2]
      data[block_hash] = 0
      for summed in sum_timings:
          try:
              item_time = sum(summed.loc[block_hash])      
              data[block_hash] = data[block_hash] + item_time
          except KeyError:
              continue
      data[block_hash] = data[block_hash] * 100 / block_time
  return pd.DataFrame.from_dict(data, orient='index', columns=["NS"])