# Project Goals
The goal of my project is to equip the user with a set of interactive visualizations that allow them to evaluate to what extent diet, obesity, and undernourishment affect COVID-19 statistics. Questions that can be answered by this visualization include "Are there ways that one can improve their chances of surviving COVID-19 through diet?" and "what are the characteristics of countries/people which managed the pandemic the best". Once I saw the dataset and the potential answers it could provide, I knew I had to at least try to enable people to answer these critical questions.

The Dataset itself is from [Kaggle](https://www.kaggle.com/mariaren/covid19-healthy-diet-dataset) (there's another link in the data folder). It contains data from the UN and Johns Hopkins, so there are reputable sources. The purpose is, of course, to see how dietary data can be used to mitigate COVID - even a single life saved is a huge deal.

# Design Decisions
Like many datasets, this one was a challenge because of the sheer number of variables and interactions there were. Broadly speaking, design decisions were driven by what I believe users would need to draw personalized information for action (without trying to be medical advice). Of course, my own curiosity also played a factor.


I started with a bubble plot which contained deaths vs confirmed cases, where the size of each point corresponded to a food category. I found that this was somewhat effective, but there were so many options for food types that it was difficult to answer a question relevant to a user. This is why I changed it to be weight vs mortality, keeping the bubble sizes as food categories (but in an interactive widget), but setting the default to be a scatter. This removed an information overload, while letting the user adapt to their actionable lives (a vegetarian cannot eat more meat, but they might be interested in dairy products, for example). A scatter plot with the option of a bubble plot conveys the independent countries in tandem with their COVID trends without having to limit the scope of the data as well.

This also let me make a guided visualization using Streamlit's states. Focusing on the broader variables rather than the fine-grained food types allowed me to actively visualize a narrative based on the trends in the scatter plot. I decided to do this because I love it when I come across it online - it's a thoughtful and elegant way a creator can guide a user's thoughts interactively. On top of that, it doesn't remove a user's ability to customize the graphic to expand upon what I guide them through.

For the first bar graph, I knew that I wanted to allow users to see what the characteristics were for the most or least successful countries. I knew I wanted something that lets the user drill down into what they're interested in. Alternatives I considered included another scatter plot and a scaled bar chart like the one after this.  There are three dimensions in the dataset important for the user to answer the questions I laid out, obesity, food categories, and COVID stats. The stacked bar chart allows users to compare magnitudes of COVID statistics and distribution of food categories, killing two birds in one stone and leading to the next chart. 

The second bar graph augments the first. I broke these up into two graphs so that one can recontextualize the fine detail contained in food categories back to the bigger picture of obesity / undernourishment rates. I decided to make use of the percentage property of adding to 100 instead of doing multiple bar charts because it helps visualize each category's relative values.

Finally, I included a GeoScatter plot. The rationale for this is obvious, COVID is a physical phenomenon, affected by geography, population densities, and cultures. The geospatial relationship is easily shown in a map, and the scatter allows for sizes and colors to encode information. The easy alternative was a Chloropleth map, but showing disease rates as sizes instead of colors emphasizes disproportionate statistics more. I found it worked better to convey the end goal - disparaties between countries and continents - without being as affected by outliers. The interactivity from plotly allows a drill down do an area of interest, further reducing the need for the broad chloropleth scheme.




# Development process

I worked alone. I spent about 12 hours on this, mostly on a combination of development and graph decisions.
First, I chose a dataset, for about an hour. I wanted one that was meaningful to me and was more than just eye candy - something educational or actionable.
I spent about 30 minutes trying to come up with a good question to answer, and the rest of the time on development / deciding between graph choices. Over an hour was spent on the stateful guided interaction, since it's not well documented in Streamlit.
I started with matplotlib, then tried Vega-Lite, and settled on Plotly. It had all the interactive hover and chart types I wanted.
