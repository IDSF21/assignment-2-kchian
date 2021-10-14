import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px

# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))

df = pd.read_csv("data\Food_Supply_Quantity_kg_Data.csv")

# TODO map countries to continents to do more cool visualizations
print(df["Obesity"])
option = st.sidebar.selectbox(
    'What would you like the point size to be?',
    [
        "Obesity",
        "Undernourished",
        "Vegetables",
        "Fish, Seafood",
    ]
)

yaxis = st.sidebar.selectbox(
    'Y-Axis',
    [
        "Deaths",
        "Recovered",
        "Active",
    ]
)

df[option] =  pd.to_numeric(df[option], errors='coerce').fillna(0)

fig = px.scatter(
    df, 
    x="Confirmed", 
    y=f"{yaxis}",
    size=option, 
    color=option,
    hover_name="Country",
    hover_data=[],
    labels={
        f"{yaxis}":f"{yaxis} (% of pop)", 
        "Confirmed":"Confirmed (% of pop)"
    }
)
fig.update_xaxes(type='log')
fig.update_yaxes(type='log')
st.plotly_chart(fig, use_container_width=True)