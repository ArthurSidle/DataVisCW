import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import zipfile

####################################################################################
# Load data #
####################################################################################

@st.cache
def load_imdb_data(req):
    url = 'DataVisDataFiles/title.{}.tsv.gz'.format(req)
    #url = 'https://arthursdata.blob.core.windows.net/datavis/title.{}.tsv.gz'.format(req)
    return pd.read_csv(url, sep='\t', index_col=0, compression='infer')

@st.cache
def load_strmsrvc_data(srvc_name):
    with zipfile.ZipFile('DataVisDataFiles/{}.zip'.format(srvc_name)) as f:
        titles_file = f.open('titles.csv')
        title = pd.read_csv(titles_file, index_col=0)
        titles_file.close()
    return title

title = {
    'basics':   load_imdb_data('basics_min'),
    #'episode':  load_imdb_data('episode'),
    #'ratings':  load_imdb_data('ratings')
}

strm = {
    'ntfl': load_strmsrvc_data('ntfl'),
    'amzn': load_strmsrvc_data('amzn'),
    'crnc': load_strmsrvc_data('crnc'),
    'dark': load_strmsrvc_data('dark'),
    'dsny': load_strmsrvc_data('dsny'),
    'hbo':  load_strmsrvc_data('hbo'),
    'hulu': load_strmsrvc_data('hulu'),
    'prmt': load_strmsrvc_data('prmt'),
    'raku': load_strmsrvc_data('raku')
}



####################################################################################
# Prepare data #
####################################################################################

@st.cache
def calc_stream_catalogue():
    catalogue = {}

    for service_name, service_data in strm.items():
        catalogue.update({service_name:
            pd.merge(title['basics'], service_data, how='inner', left_on='tconst', right_on='imdb_id')})
    
    return catalogue

stream_catalogue = calc_stream_catalogue()
stream_scores = [title['basics'].shape[0]] + [x.shape[0] for x in stream_catalogue.values()]
stream_index = [
    'IMDB',
    'Netflix',
    'Amazon Prime Video',
    'Crunchyroll',
    'Dark Matter TV',
    'Disney+',
    'HBO Max',
    'Hulu',
    'Paramount+',
    'Rakuten TV'
]

pyplot_container = st.container()
multiselect_container = st.container()

with multiselect_container:
    selected_options = st.multiselect('Choose which streaming services to view the library size of.',
    options = stream_index,
    default = stream_index)

stream_avail = pd.Series(stream_scores, index=stream_index)
stream_selected = stream_avail[selected_options]

sns.set_theme(style='darkgrid')
stream_avail_plot = sns.barplot(x=stream_selected, y=stream_selected.index).figure
plt.xlabel('No. of Titles')
plt.ylabel('Streaming Service')

with pyplot_container:
    st.pyplot(stream_avail_plot)

@st.cache
def get_catalogue_size():
    catalogue_join = pd.DataFrame(columns=stream_catalogue['ntfl'].columns)

    for service_name, service_data in stream_catalogue.items():
        catalogue_join = pd.merge(catalogue_join, service_data, how='outer', on='imdb_id')
    
    return catalogue_join.shape[0]

catalogue_size = get_catalogue_size()
imdb_size = title['basics'].shape[0]
stream_on_imdb = (catalogue_size / imdb_size) * 100
stream_on_imdb = round(stream_on_imdb * 100) / 100

st.write('Only around {}% of the IMDB catalogue of movies and TV shows can be watched on streaming services'.format(stream_on_imdb))