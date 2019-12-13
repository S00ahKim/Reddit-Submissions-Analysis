import pandas as pd
import numpy as np

sbr = ['aiyu', 'bangtan', 'BlackPink', 'computerscience', 'datascience', 'deeplearning', 'exo', 'Futurology', 'gameofthrones', 'GilmoreGirls', 'Got7', 'kpop', 'kpoppers', 'MachineLearning', 'red_velvet', 'snsd', 'tensorflow', 'TheGoodPlace', 'twice']
last = [1575084666, 1575125910, 1575119104, 1575123317, 1575117820, 1575100154, 1575115686, 1575123523, 1575125621, 1575117685, 1575125169, 1575125194, 1575124892, 1575121464, 1575123882, 1575120823, 1575123122, 1575125832, 1575125679]

meta = pd.DataFrame(np.column_stack([sbr, last]), 
                    columns=['subreddit', 'last'])

meta.to_csv('./data/metadata/data.csv')