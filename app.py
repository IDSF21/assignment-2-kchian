import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import pycountry
import plotly.graph_objects as go

# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
st.title("Does diet and obesity affect the mortality rate of COVID-19?")

df = pd.read_csv("data\Food_Supply_Quantity_kg_Data.csv")


def toggle_demo_mode():
    st.session_state["demo_mode"] = False

def check_demo_mode():
    return "demo_mode" in st.session_state and st.session_state["demo_mode"] 

df["Base"] = 0.1
# SIDEBAR
all_food_columns = [
    "Alcoholic Beverages","Animal fats","Animal Products","Aquatic Products, Other","Cereals - Excluding Beer","Eggs","Fish, Seafood","Fruits - Excluding Wine","Meat","Milk - Excluding Butter","Miscellaneous","Offals","Oilcrops","Pulses","Spices","Starchy Roots","Stimulants","Sugar & Sweeteners","Sugar Crops","Treenuts","Vegetable Oils","Vegetables","Vegetal Products"
]

st.sidebar.title("Scatter options")

size_options = all_food_columns
# size_options = [
#     "Vegetables",
#     "Fish, Seafood",
# ]
size_opt = st.sidebar.selectbox('What would you like the point size to be?', [None] + all_food_columns, on_change=toggle_demo_mode)
yaxis_options = [
    "Obesity",
    "Undernourished",
]

yaxis_opt = st.sidebar.selectbox('Y-Axis', yaxis_options, on_change=toggle_demo_mode)

df["Mortality"] = df["Deaths"] / df["Confirmed"] 
xaxis_options = [
    "Mortality",
    "Deaths",
    "Confirmed",
]

xaxis_opt = st.sidebar.selectbox('X-Axis (Scatter)', xaxis_options, on_change=toggle_demo_mode)

logx = st.sidebar.checkbox('logx', on_change=toggle_demo_mode)
logy = st.sidebar.checkbox('logy', on_change=toggle_demo_mode)


st.sidebar.title("Bar graph options")
xaxis_bar_opt = st.sidebar.selectbox('X-Axis (Bar)', xaxis_options, on_change=toggle_demo_mode)
ascending = st.sidebar.checkbox('Ascending', on_change=toggle_demo_mode)


st.sidebar.title("Map options")
map_opt = st.sidebar.selectbox('Size/Color metric', xaxis_options, on_change=toggle_demo_mode, index=1)


# numeric conversions
for i in yaxis_options + size_options + xaxis_options:
    df[i] =  pd.to_numeric(df[i], errors='coerce').fillna(0)


desc_dict = {i:i + " (% of diet in weight)" for i in all_food_columns}
for i in yaxis_options:
    desc_dict[i] = f"{i} (% of population)"
desc_dict["Mortality"] = "Mortality (deaths/confirmed case)"
desc_dict["Deaths"] = "Deaths (% of population)"
desc_dict["Confirmed"] = "Confirmed (% of population)"
desc_dict["Obesity"] = "Obesity (% of population)"

# BUBBLE CHART

def write_bubble():
    fig = px.scatter(
        df, 
        x=xaxis_opt, 
        y=f"{yaxis_opt}",
        size=size_opt, 
        color=size_opt,
        hover_name="Country",
        hover_data=[],
        labels={
            yaxis_opt:desc_dict[yaxis_opt], 
            xaxis_opt:desc_dict[xaxis_opt], 
        }
    )
    if logx:
        fig.update_xaxes(type='log')
    if logy:
        fig.update_yaxes(type='log')
    st.plotly_chart(fig, use_container_width=True)

def write_stacked_bar():
    
    subset = df.dropna()[df[xaxis_bar_opt] > 0].sort_values(xaxis_bar_opt, ascending=ascending)[:10]
    subset[all_food_columns] = subset[all_food_columns].multiply(df[xaxis_bar_opt], axis="index")/ 100
    fig = px.bar(
        subset, 
        x="Country", 
        y=all_food_columns, 
        title=f"Diet of 10 Countries with the {'Smallest' if ascending else 'Largest'} {desc_dict[xaxis_bar_opt]}",
        labels={
            "value": desc_dict[xaxis_bar_opt]
        }
    )
    st.plotly_chart(fig)
    
def write_stacked_obesity_bar():
    subset = df.dropna()[df[xaxis_bar_opt] > 0].sort_values(xaxis_bar_opt, ascending=ascending)[:20]
    subset["Other"] = 100 - df["Obesity"] - df["Undernourished"]
    cols = [
        "Obesity",
        "Undernourished",
        "Other",
    ]
    fig = px.bar(
        subset, 
        x="Country", 
        y=cols, 
        title=f"Obesity level of 10 Countries with the Largest {desc_dict[xaxis_bar_opt]}"
    )
    st.plotly_chart(fig)


def write_scatter_geo():
    def get_alpha3(x):
        cnt = pycountry.countries.get(name=x)
        if not cnt:
            if x.startswith("Iran"):
                x = "Iran"
            elif x == "Korea, North":
                return "PRK"
            elif x == "Korea, South":
                return "KOR"
            elif x == "Taiwan*":
                return "TWN"
            elif x.startswith("Venezuela"):
                return "VEN"
            cnt = pycountry.countries.search_fuzzy(x)
            if len(cnt):
                return cnt[0].alpha_3
            return None
        return cnt.alpha_3
    df["Alpha3"] = df["Country"].apply(get_alpha3)

    fig = go.Figure()
    # fig.add_trace(go.Choropleth(locations=df["Alpha3"],
    #                     z=df["Obesity"],
    #                     hovertext=df["Country"],))
    fig.update_layout(title_text=f'Per-country Aggregation of {map_opt}')
    fig.add_trace(
        go.Scattergeo(
            locationmode="ISO-3",
            locations=df["Alpha3"],
            # hovertext=df["Country"],,
            hovertext = ['{}:  {}% {}'.format(i["Country"],i[map_opt], map_opt) for ind, i in df.iterrows()],
            marker = dict(
                size = df[map_opt]*100 if map_opt is not "Confirmed" else df[map_opt]*2, # adjusting relative size
                color = df[map_opt],
                opacity = 1,
                line_width = 1,
                line=dict(
                    color='MediumPurple',
                    width=2
                ),
            )
        )
    )
    st.plotly_chart(fig)

st.write("""
Let's start with a simple plot: obesity vs mortality (deaths/confirmed case) per country. You can change the scatter chart to a bubble chart if 
you'd like, where the sizes correspond to the percentage by weight of consumption of a certain food category. You can also 
change the x-axis.
""") 

if check_demo_mode() and "clicked1" in st.session_state and st.session_state["clicked1"]:
    # stage 3
    yaxis_opt = "Obesity"
    xaxis_opt = "Confirmed"
    write_bubble()
    st.write("""
It looks like if a country has more obese people, it is more likely they have a high death percentage. This could easily
be correlation and not causation (perhaps more obese people live in crowded countries). And it doesn't seem like obesity affects
the chances that they recover given our initial graph (indicated by mortality). 
""")
    def toggle_clicked():
        st.session_state["demo_mode"] = True
        st.session_state["clicked2"] = True
        st.session_state["clicked1"] = False
    show2 = st.button('What else?', on_click = toggle_clicked)
elif check_demo_mode() and "clicked2" in st.session_state and st.session_state["clicked2"]:
    # stage 2
    yaxis_opt = "Undernourished"
    xaxis_opt = "Confirmed"
    write_bubble()
    st.write("""
There's also a definite pattern between undernourished and confirmed percentage, aligning with what we saw earlier. If a country has
a larger undernourished population, possibly indicating less development, there are fewer confirmed cases (and thus deaths).
""")
    def toggle_clicked():
        st.session_state["demo_mode"] = True
        st.session_state["clicked2"] = False
        st.session_state["clicked3"] = True
    show2 = st.button('What else?', on_click = toggle_clicked)
elif check_demo_mode() and "clicked3" in st.session_state and st.session_state["clicked3"]:
    # stage 3
    yaxis_opt = "Undernourished"
    xaxis_opt = "Mortality"
    write_bubble()
    st.write("""
Mortality, on the other hand, doesn't seem to follow the same pattern - regardless of obesity and undernourished rates, the mortality, and thus
recovery rate, seems fairly uniform. Feel free to play around outside of these demos - it's interesting to see how food type (point size) can indicate 
obesity.

You can use log scales (via checkboxes in the sidebar) to help mitigate the outlier's effect on the graph, or just zoom in to the graph.
""")

else:
    # stage 1
    write_bubble()
    st.write("""
It's not apparent from default values whether there's a correlation between Obesity and Mortality. However, 
changing the X-Axis to Deaths allows patterns to start emerging.
""")
    def toggle_clicked():
        st.session_state["clicked1"] = True
        st.session_state["demo_mode"] = True
    show1 = st.button('Show me', on_click = toggle_clicked)




write_stacked_bar()
st.write("""
Via this stacked bar chart, you can observe the diets of the top/bottom 10 countries in either death or mortality. You can change
which metric by using the sidebar "X-Axis" widget. There is no obvious pattern for relating the diet of all top/bottom countries to any of the x-axis
metrics, but at the same time, it means that overall diet may not affect chances at recovering from or getting COVID.

Try toggling the ascension parameter. There tends to be more animal products and fats in the small-mortality chart.
This is possibly a result of being a more developed nation, same as the relationship identified through the scatter.
""")

write_stacked_obesity_bar()
st.write("""
Via these two stacked bar charts, you can observe the diets of the top/bottom 10 countries in either death or mortality. You can change
which metric by using the sidebar "X-Axis" widget. There is no obvious pattern for relating the diet of all top/bottom countries to any of the x-axis
metrics, but at the same time, it means that overall diet may not affect chances at recovering from or getting COVID.

Between the two bar charts, however, if you play around a bit there tends to be more animal products and fats in the small-mortality chart.
This is possibly a result of being a more developed nation, same as the relationship identified through the scatter.
""")
write_scatter_geo()
st.write("""
Via the geo scatter, you can see the relation between your chosen metric and geography. Densely populated areas, like Europe, seem to suffer heavily,
likely implying easier spread.
""")