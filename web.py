import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    data = pd.concat([pd.read_parquet('all_data1.parquet'), pd.read_parquet('all_data2.parquet')])
    return data
    
st.title('Welcome to DiffCNN')
data = load_data()

select_box1 = st.selectbox('What is the cell type you want to try', data['cell_type'].unique(), placeholder='Select a cell', index=None)
select_box2 = st.selectbox('What is the drug you want to apply on the cell', data['sm_name'].unique(), placeholder='Select a drug', index=None)


if select_box1 != None and select_box2 != None:
    x = data[data['cell_type'] == select_box1]
    x = x[x['sm_name'] == select_box2]
    x = x.drop(['cell_type', 'SMILES', 'sm_name'], axis=1)
    x = x.iloc[0]
    x = x.sort_values(key=abs)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['red' if val < 0 else 'blue' for val in x]
    bars = plt.bar(x.index[:10], x[:10], color=colors)
    plt.xticks(rotation=45)
    plt.xlabel('Genes')
    plt.ylabel('Differential gene expression value')
    plt.title('The top 10 most affected genes')
    plt.tight_layout()
    st.pyplot(fig)