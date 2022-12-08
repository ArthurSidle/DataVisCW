import pandas as pd

title_basics = pd.read_csv('DataVisDataFiles/title.basics.tsv.gz', sep='\t', index_col=0, compression='infer')



title_basics.drop(title_basics[
    (title_basics.titleType == 'short') |
    (title_basics.titleType == 'tvEpisode') |
    (title_basics.titleType == 'tvSpecial') |
    (title_basics.titleType == 'tvShort') |
    (title_basics.titleType == 'videoGame')
].index, inplace=True)

title_basics.drop('originalTitle', axis=1, inplace=True)
title_basics.drop('titleType', axis=1, inplace=True)
title_basics.drop('endYear', axis=1, inplace=True)
title_basics.drop('isAdult', axis=1, inplace=True)

title_basics.to_csv('DataVisDataFiles/title.basics_min.tsv.gz', sep='\t', compression='gzip')