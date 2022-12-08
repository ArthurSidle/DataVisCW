import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import zipfile
import requests
import io

def load_imdb_data(req):
    url = 'DataVisDataFiles/title.{}.tsv.gz'.format(req)
    #url = 'https://arthursdata.blob.core.windows.net/datavis/title.{}.tsv.gz'.format(req)
    return pd.read_csv(url, sep='\t', index_col=0, compression='infer')

def load_strmsrvc_data(srvc_name):
    #with requests.get('https://arthursdata.blob.core.windows.net/datavis/{}.zip'.format(srvc_name), stream=True) as uncomp:
        #with zipfile.ZipFile(io.BytesIO(uncomp.content)) as f:
    with zipfile.ZipFile('DataVisDataFiles/{}.zip'.format(srvc_name)) as f:
        titles_file = f.open('titles.csv')
        #credits_file = f.open('credits.csv')
        
        title = pd.read_csv(titles_file, index_col=0)
        #credit = pd.read_csv(credits_file, index_col=0)

        titles_file.close()
        #credits_file.close()
    
    #return {'titles':title, 'credits':credit}
    return title

title = {
    'basics':   load_imdb_data('basics_min'),
    #'episode':  load_imdb_data('episode'),
    'ratings':  load_imdb_data('ratings')
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

st.write(title['basics'].head())
st.write(strm['ntfl'].head())