import pandas as pd
from PIL import Image
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import gmplot
import pydeck as pdk
import altair as alt
import plotly.io as pio
from plotly.graph_objs import Bar, Data, Figure, Layout, Marker, Scatter
import requests
import seaborn as sns
import openpyxl
import pip
pip.main(["install", "openpyxl"])

#@st.cache(suppress_st_warning=True)
###Header and Parameter
st.header("Purchase market affordability in London")
df = pd.read_excel('https://github.com/CRELYTICA-MatthewYoung/streamlit_upload/blob/main/20220307%20Residential%20Data%20-%20Purchase%20(3)%20(5).xlsx?raw=true', engine='openpyxl')

#st.subheader('Enter your salary and median or average')
with st.sidebar:
    st.header("Configuration")
    with st.form(key="grid_reset"):
        parameter = st.slider("Salary", 21000, 500000)
        which = st.radio("Median or average?", ("Median", "Average"))
        stamp_duty = st.radio("Type of buying?", ("First-time buyers", "Moving home", "Additional home", "Company"))
        st.form_submit_button(label="Reset configuration")
lendingamount = (parameter*4.5)
lending_amount = str(int(lendingamount))
Price_parameter = (lendingamount)+(lendingamount*0.1)
for_title = str(int(Price_parameter))
deposit = (parameter*4.5)*0.1
deposit_for = str(int(deposit))
index = df.index


###Affordability Logic
for i in range (0, len(index)):
    number = int(i)
    if int(df.at[number, 'Salary']) > int(parameter):
        df._set_value(number, 'Affordability', 0)
        df._set_value(number, 'AffordableY', 0)
        df._set_value(number, 'AffordableN', 1)
        df.loc[number, 'Affordable?'] = 'Not Affordable'
    else:
        df._set_value(number, 'Affordability', 1)
        df._set_value(number, 'AffordableY', 1)
        df._set_value(number, 'AffordableN', 0)
        df.loc[number, 'Affordable?'] = 'Affordable'


#st.subheader('What is the circumstance of your buying? :')
#stamp_duty = st.radio("Type of buying?", ("First-time buyers", "Moving home", "Additional home", "Company"))
if stamp_duty == "First-time buyers":
    if Price_parameter > 1500000:
        a = (Price_parameter-1500000)*0.12 + 93750
    elif 1500000 > Price_parameter > 925000: 
        a = (Price_parameter-925000)*0.1 + 36250
    elif 925000 > Price_parameter > 500000: 
        a = (Price_parameter-250000)*0.05 + 2500
    elif 500000 > Price_parameter > 300000:
        a = (Price_parameter-300000)*0.05
    else:
        a = 0
elif stamp_duty == "Moving home":
    if Price_parameter > 1500000:
        a = (Price_parameter-1500000)*0.12 + 93750
    elif Price_parameter > 925000: 
        a = (Price_parameter-925000)*0.1 + 36250
    elif Price_parameter > 250000: 
        a = (Price_parameter-250000)*0.05 + 2500
    elif Price_parameter > 125000: 
        a = (Price_parameter-125000)*0.02
    else:
        a = 0
elif stamp_duty == "Additional home":
    if Price_parameter > 1500000:
        a = (Price_parameter-1500000)*0.15 + 138750
    elif Price_parameter > 925000: 
        a = (Price_parameter-925000)*0.13 + 64000
    elif Price_parameter > 250000: 
        a = (Price_parameter-250000)*0.08 + 10000
    elif Price_parameter > 125000: 
        a = (Price_parameter-125000)*0.05
    else:
        a = 0
else:
    if Price_parameter > 500000:
        a = (Price_parameter-500000)*0.15
    else:
        a = 0
b = str(int(a))


if stamp_duty == "First-time buyers":
    for i in range (0, len(index)):
        number = int(i)
        if int(df.at[number, 'Price']) > 1500000:
            c = ((df.at[number, 'Price'])-1500000)*0.12 + 93750
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 925000:
            c = ((df.at[number, 'Price'])-925000)*0.1 + 36250
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 500000: 
            c = ((df.at[number, 'Price'])-250000)*0.05 + 2500
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 300000:
            c = ((df.at[number, 'Price'])-300000)*0.05
            df._set_value(number, 'Stamp Duty', c)
        else:
            c = 0
            df._set_value(number, 'Stamp Duty', c)
elif stamp_duty == "Moving home":
    for i in range (0, len(index)):
        number = int(i)
        if int(df.at[number, 'Price']) > 1500000:
            c = ((df.at[number, 'Price'])-1500000)*0.12 + 93750
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 925000: 
            c = ((df.at[number, 'Price'])-925000)*0.1 + 36250
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 250000: 
            c = ((df.at[number, 'Price'])-250000)*0.05 + 2500
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 125000: 
            c = ((df.at[number, 'Price'])-125000)*0.02
            df._set_value(number, 'Stamp Duty', c)
        else:
            c = 0
            df._set_value(number, 'Stamp Duty', c)
elif stamp_duty == "Additional home":
    for i in range (0, len(index)):
        number = int(i)
        if int(df.at[number, 'Price']) > 1500000:
            c = ((df.at[number, 'Price'])-1500000)*0.15 + 138750
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 925000: 
            c = ((df.at[number, 'Price'])-925000)*0.13 + 64000
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 250000: 
            c = ((df.at[number, 'Price'])-250000)*0.08 + 10000
            df._set_value(number, 'Stamp Duty', c)
        elif int(df.at[number, 'Price']) > 125000: 
            c = ((df.at[number, 'Price'])-125000)*0.05 + 3750
            df._set_value(number, 'Stamp Duty', c)
        else:
            c = (df.at[number, 'Price'])*0.03
            df._set_value(number, 'Stamp Duty', c)
else:
    for i in range (0, len(index)):
        number = int(i)
        if int(df.at[number, 'Price']) > 500000:
            c = ((df.at[number, 'Price'])-500000)*0.15
            df._set_value(number, 'Stamp Duty', c)
        else:
            c = 0
            df._set_value(number, 'Stamp Duty', c)

figurestamp = px.scatter(df, x="Price", y="Stamp Duty", color = "Affordable?")
figurestamp.update_xaxes(range=[0, 1600000])
figurestamp.update_yaxes(range=[0, 80000])
#st.write(df)

###Affordability Logic
for i in range (0, len(index)):
    number = int(i)
    if int(df.at[number, 'Salary']) > int(parameter):
        df._set_value(number, 'Affordability', 0)
        df._set_value(number, 'AffordableY', 0)
        df._set_value(number, 'AffordableN', 1)
        df.loc[number, 'Affordable?'] = 'Not Affordable'
    else:
        df._set_value(number, 'Affordability', 1)
        df._set_value(number, 'AffordableY', 1)
        df._set_value(number, 'AffordableN', 0)
        df.loc[number, 'Affordable?'] = 'Affordable'


###Inverse distance
for i in range(0, len(index)):
    number = int(i)
    inverse = 3 - (df['Tube DistanceMiles'].iloc[i])
    df._set_value(number, 'Inverse', inverse)
st.write(df)
    

###Detailed map
def map(data):
    selected_columns = data[["Longitude","Latitude"]]
    df = selected_columns.copy()
    df.rename({'Longitude':'lon'}, axis='columns', inplace=True)
    df.rename({'Latitude':'lat'}, axis='columns', inplace=True)
    st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/light-v9',
         initial_view_state=pdk.ViewState(
             latitude=51.5072,
             longitude=-0.1276,
             zoom=9,
             pitch=50,
         ),
         layers=[
             pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=5,
                get_elevation="Price",
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
             ),
             pdk.Layer(
                 'ScatterplotLayer',
                 data=df,
                 get_position='[lon, lat]',
                 get_color='[200, 30, 0, 160]',
                 get_radius=200,
             ),
         ],
     ))



###Price vs Price graph (not in use)
figure1 = px.scatter(df, x="Price", y="Price",
                        color="Affordable?")
figure1.update_xaxes(range=[0, 3000000])
figure1.update_yaxes(range=[0, 3000000])


###Running total graph
for i in range (0, len(index)):
    number = int(i)
    new = ((number+1)/len(index))*100
    df._set_value(number, "Running total", new)
    
figure2 = px.scatter(df, x="Salary", y="Running total",
                        color="Affordable?",
                        labels={
                           "Running total": "Affordability percentage"})
figure2.update_xaxes(range=[0, 500000])
figure2.update_yaxes(range=[0, 100])

#def slicer(df, index):
    #df_North = df[df['Geography']=="North"]
    #st.write(df_North)
    #length1 = df_North.index
    #multiplier1 = index/len(length1)
    #st.subheader(str(multiplier1))
    #df_North["Running total detail"] = df_North["Running total"]*multiplier1
    #figure20 = px.scatter(df_North, x="Salary", y="Running total detail",
                        #color="Affordable?")
    #df_South = df[df['Geography']=="South"]
    #st.write(df_South)
    #length2 = df_South.index
    #multiplier2 = index/len(length2)
    #st.subheader(str(multiplier2))
    #df_South["Running total detail"] = df_South["Running total"]*multiplier2
    #figure21 = px.scatter(df_South, x="Salary", y="Running total detail",
                        #color="Affordable?")
    #figure22 = make_subplots(specs=[[{"secondary_y": True}]])
    #figure22.add_trace(figure20)
    #figure22.add_trace(figure21,secondary_y=True)
    #st.write(figure22)


###Starter info 
#which = st.radio("Median or average?", ("Median", "Average"))
st.subheader("With the entered salary, the bank will lend up to £" + lending_amount)
st.subheader("This means the maximum house price affordable is £" + for_title +
             ' assuming you have a 10% deposit of £' + deposit_for)
st.subheader("A stamp duty of up to £" + b + " is also required up front. Bringing the total amount needed up front to £" +
             str(int(deposit+a)))
sum_first = df["Affordability"].sum()
sum_string = str(int((sum_first/len(index))*100))
st.subheader("The affordability fraction for London is " + sum_string + '%')


###Average/median price by general region
if which == "Average":
    grouped_df = df.groupby("Geography")
    mean_df = grouped_df.mean()
    Geography = ["Central", "East", "North", "South", "West"]
    mean_df["Geography"] = Geography
    #st.write(mean_df)
    figure3 = px.bar(mean_df, x = "Geography", y = "Price",
               color = "Geography",
               labels={
                   "Price": "Average price (£)"})
    figure3.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    figure3.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
else:
    grouped_df = df.groupby("Geography")
    median_df = grouped_df.median()
    Geography = ["Central", "East", "North", "South", "West"]
    median_df["Geography"] = Geography
    #st.write(median_df)
    figure3 = px.bar(median_df, x = "Geography", y = "Price",
               color = "Geography",
               labels={
                   "Price": "Median price (£)"})
    figure3.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    figure3.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})


###Average/median distance from tube
grouped7_df = df.groupby("2")
mean7_df = grouped7_df.mean()
median7_df = grouped7_df.median()
if which == "Average":
    #grouped7_df = df.groupby("2")
    #mean7_df = grouped7_df.mean()
    Geography2 = ["Central", "East", "North", "North-East", "North-West",
                 "South", "South-East", "South-West", "West"]
    mean7_df["Geography Detailed"] = Geography2
    #st.write(mean_df)
    figure7 = px.bar(mean7_df, x = "Geography Detailed", y = "Price",
               labels={
                   "Price": "Average price (£)",
                   "Geography Detailed": "Region"})
    figure7.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    figure7.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    mean7_df["Affordability percentage"] = mean7_df["Affordability"]*100
    mean7_df = mean7_df.sort_values('Tube DistanceMiles', ascending=False)
    Geography_sort13 = [str(mean7_df['Geography Detailed'].iloc[0]), str(mean7_df['Geography Detailed'].iloc[1]),
                        str(mean7_df['Geography Detailed'].iloc[2]), str(mean7_df['Geography Detailed'].iloc[3]),
                        str(mean7_df['Geography Detailed'].iloc[4]), str(mean7_df['Geography Detailed'].iloc[5]),
                        str(mean7_df['Geography Detailed'].iloc[6]), str(mean7_df['Geography Detailed'].iloc[7]),
                        str(mean7_df['Geography Detailed'].iloc[8])]
    figure13 = make_subplots(specs=[[{"secondary_y": True}]])
    figure13.add_trace(
    go.Bar(x=Geography_sort13, y=mean7_df['Tube DistanceMiles'], name="Distance"),
    secondary_y=False,
    )

    figure13.add_trace(
    go.Scatter(x=Geography_sort13, y=mean7_df['Affordability percentage'], name="Affordability percentage"),
    secondary_y=True,
    )
    figure13.update_yaxes(title_text="Distance (miles)", secondary_y=False)
    figure13.update_yaxes(title_text="Affordability percentage", secondary_y=True)
    #figure13 = px.bar(mean7_df, x = "Geography Detailed", y= "Tube DistanceMiles",
                      #labels={
                          #"Tube DistanceMiles": "Distance (miles)",
                          #"Geography Detailed": "Region"})
    #figure13.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
 
else:
    #grouped7_df = df.groupby("2")
    #median7_df = grouped7_df.median()
    Geography2 = ["Central", "East", "North", "North-East", "North-West",
                 "South", "South-East", "South-West", "West"]
    median7_df["Geography Detailed"] = Geography2
    #st.write(median_df)
    figure7 = px.bar(median7_df, x = "Geography Detailed", y = "Price",
               labels={
                   "Price": "Median price (£)",
                   "Geography Detailed": "Region"})
    figure7.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    figure7.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    median7_df["Affordability percentage"] = median7_df["Affordability"]*100
    median7_df = median7_df.sort_values('Tube DistanceMiles', ascending=False)
    Geography_sort13 = [str(median7_df['Geography Detailed'].iloc[0]), str(median7_df['Geography Detailed'].iloc[1]),
                        str(median7_df['Geography Detailed'].iloc[2]), str(median7_df['Geography Detailed'].iloc[3]),
                        str(median7_df['Geography Detailed'].iloc[4]), str(median7_df['Geography Detailed'].iloc[5]),
                        str(median7_df['Geography Detailed'].iloc[6]), str(median7_df['Geography Detailed'].iloc[7]),
                        str(median7_df['Geography Detailed'].iloc[8])]
    figure13 = make_subplots(specs=[[{"secondary_y": True}]])
    figure13.add_trace(
    go.Bar(x=Geography_sort13, y=median7_df['Tube DistanceMiles'], name="Distance"),
    secondary_y=False,
    )

    figure13.add_trace(
    go.Scatter(x=Geography_sort13, y=median7_df['Affordability percentage'], name="Affordability percentage"),
    secondary_y=True,
    )
    figure13.update_yaxes(title_text="Distance (miles)", secondary_y=False)
    figure13.update_yaxes(title_text="Affordability percentage", secondary_y=True)
    #figure13 = px.bar(median7_df, x = "Geography Detailed", y= "Tube DistanceMiles",
                      #labels={
                          #"Tube DistanceMiles": "Distance (miles)",
                          #"Geography Detailed": "Region"})
    #figure13.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})


#Mean vs median area stacked
groupednew_df = df.groupby("2")
meannew_df = groupednew_df.mean()
mediannew_df = groupednew_df.median()
figure_area = go.Figure()
figure_area.add_trace(go.Scatter(x=Geography2, y=mediannew_df["Price"], fill='tozeroy', name='Median'))
figure_area.add_trace(go.Scatter(x=Geography2, y=meannew_df["Price"], fill='tonexty', name='Mean'))
st.subheader('Comparison of median and average property price')
st.write(figure_area)

###(Pie chart) number of properties by detailed region
grouped10_df = df.groupby("2")
sum10_df = grouped10_df.sum()
Geography2 = ["Central", "East", "North", "North-East", "North-West",
             "South", "South-East", "South-West", "West"]
sum10_df["Geography Detailed"] = Geography2
figure10 = px.pie(sum10_df, values = "One", names = "Geography Detailed",
                  labels={
                   "One": "Count"})


###(Pie chart) number of properties by borough 
grouped11_df = df.groupby("Borough")
sum11_df = grouped11_df.sum()
Borough = ["Barking and Dagenham", "Barnet", "Bexley", "Brent",
               "Bromley", "Camden", "City of London", "Croydon",
               "Ealing", "Enfield", "Greenwich", "Hackney",
               "Hammersmith and Fulham", "Haringey", "Harrow",
               "Havering", "Hillingdon", "Hounslow", "Islington",
               "Kensington and Chelsea", "Kingston upon Thames",
               "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
               "Richmond upon Thames", "Southwark", "Sutton",
               "Tower Hamlets", "Waltham Forest", "Wandsworth",
               "Westminster"]
sum11_df["Borough"] = Borough
figure11 = px.bar(sum11_df, x = "Borough", y = "One",
               labels={
                   "One": "Count"})
figure11.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})


###Average/median price by borough
if which == "Average":
    grouped2_df = df.groupby("Borough")
    mean2_df = grouped2_df.mean()
    Borough = ["Barking and Dagenham", "Barnet", "Bexley", "Brent",
               "Bromley", "Camden", "City of London", "Croydon",
               "Ealing", "Enfield", "Greenwich", "Hackney",
               "Hammersmith and Fulham", "Haringey", "Harrow",
               "Havering", "Hillingdon", "Hounslow", "Islington",
               "Kensington and Chelsea", "Kingston upon Thames",
               "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
               "Richmond upon Thames", "Southwark", "Sutton",
               "Tower Hamlets", "Waltham Forest", "Wandsworth",
               "Westminster"]
    mean2_df["Borough"] = Borough
    #st.write(mean_df)
    figure4 = px.bar(mean2_df, x = "Borough", y = "Price",
               labels={
                   "Price": "Average price (£)"})
    figure4.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    figure4.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    mean2_df["Affordability percentage"] = mean2_df["Affordability"]*100
    mean2_df = mean2_df.sort_values('Tube DistanceMiles', ascending=False)
    Borough_sort12 = [str(mean2_df['Borough'].iloc[0]), str(mean2_df['Borough'].iloc[1]),
                      str(mean2_df['Borough'].iloc[2]), str(mean2_df['Borough'].iloc[3]),
                      str(mean2_df['Borough'].iloc[4]), str(mean2_df['Borough'].iloc[5]),
                      str(mean2_df['Borough'].iloc[6]), str(mean2_df['Borough'].iloc[7]),
                      str(mean2_df['Borough'].iloc[8]), str(mean2_df['Borough'].iloc[9]),
                      str(mean2_df['Borough'].iloc[10]), str(mean2_df['Borough'].iloc[11]),
                      str(mean2_df['Borough'].iloc[12]), str(mean2_df['Borough'].iloc[13]),
                      str(mean2_df['Borough'].iloc[14]), str(mean2_df['Borough'].iloc[15]),
                      str(mean2_df['Borough'].iloc[16]), str(mean2_df['Borough'].iloc[17]),
                      str(mean2_df['Borough'].iloc[18]), str(mean2_df['Borough'].iloc[19]),
                      str(mean2_df['Borough'].iloc[20]), str(mean2_df['Borough'].iloc[21]),
                      str(mean2_df['Borough'].iloc[22]), str(mean2_df['Borough'].iloc[23]),
                      str(mean2_df['Borough'].iloc[24]), str(mean2_df['Borough'].iloc[25]),
                      str(mean2_df['Borough'].iloc[26]), str(mean2_df['Borough'].iloc[27]),
                      str(mean2_df['Borough'].iloc[28]), str(mean2_df['Borough'].iloc[29]),
                      str(mean2_df['Borough'].iloc[30]), str(mean2_df['Borough'].iloc[31]),
                      str(mean2_df['Borough'].iloc[32])]
    figure12 = make_subplots(specs=[[{"secondary_y": True}]])
    figure12.add_trace(
    go.Bar(x=Borough_sort12, y=mean2_df['Tube DistanceMiles'], name="Distance"),
    secondary_y=False,
    )

    figure12.add_trace(
    go.Scatter(x=Borough_sort12, y=mean2_df['Affordability percentage'], name="Affordability percentage"),
    secondary_y=True,
    )
    figure12.update_layout(xaxis = dict(tickfont = dict(size=10)))
    figure12.update_yaxes(title_text="Distance (miles)", secondary_y=False)
    figure12.update_yaxes(title_text="Affordability percentage", secondary_y=True)
    #figure12 = px.bar(mean2_df, x = "Borough", y= "Tube DistanceMiles",
                      #labels={
                          #"Tube DistanceMiles": "Distance (miles)"})
    #figure12.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
else:
    grouped2_df = df.groupby("Borough")
    median2_df = grouped2_df.median()
    Borough = ["Barking and Dagenham", "Barnet", "Bexley", "Brent",
               "Bromley", "Camden", "City of London", "Croydon",
               "Ealing", "Enfield", "Greenwich", "Hackney",
               "Hammersmith and Fulham", "Haringey", "Harrow",
               "Havering", "Hillingdon", "Hounslow", "Islington",
               "Kensington and Chelsea", "Kingston upon Thames",
               "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
               "Richmond upon Thames", "Southwark", "Sutton",
               "Tower Hamlets", "Waltham Forest", "Wandsworth",
               "Westminster"]
    median2_df["Borough"] = Borough
    #st.write(median_df)
    figure4 = px.bar(median2_df, x = "Borough", y = "Price",
               labels={
                   "Price": "Median price (£)"})
    figure4.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    figure4.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
    median2_df["Affordability percentage"] = median2_df["Affordability"]*100
    median2_df = median2_df.sort_values('Tube DistanceMiles', ascending=False)
    Borough_sort12 = [str(median2_df['Borough'].iloc[0]), str(median2_df['Borough'].iloc[1]),
                      str(median2_df['Borough'].iloc[2]), str(median2_df['Borough'].iloc[3]),
                      str(median2_df['Borough'].iloc[4]), str(median2_df['Borough'].iloc[5]),
                      str(median2_df['Borough'].iloc[6]), str(median2_df['Borough'].iloc[7]),
                      str(median2_df['Borough'].iloc[8]), str(median2_df['Borough'].iloc[9]),
                      str(median2_df['Borough'].iloc[10]), str(median2_df['Borough'].iloc[11]),
                      str(median2_df['Borough'].iloc[12]), str(median2_df['Borough'].iloc[13]),
                      str(median2_df['Borough'].iloc[14]), str(median2_df['Borough'].iloc[15]),
                      str(median2_df['Borough'].iloc[16]), str(median2_df['Borough'].iloc[17]),
                      str(median2_df['Borough'].iloc[18]), str(median2_df['Borough'].iloc[19]),
                      str(median2_df['Borough'].iloc[20]), str(median2_df['Borough'].iloc[21]),
                      str(median2_df['Borough'].iloc[22]), str(median2_df['Borough'].iloc[23]),
                      str(median2_df['Borough'].iloc[24]), str(median2_df['Borough'].iloc[25]),
                      str(median2_df['Borough'].iloc[26]), str(median2_df['Borough'].iloc[27]),
                      str(median2_df['Borough'].iloc[28]), str(median2_df['Borough'].iloc[29]),
                      str(median2_df['Borough'].iloc[30]), str(median2_df['Borough'].iloc[31]),
                      str(median2_df['Borough'].iloc[32])]
    figure12 = make_subplots(specs=[[{"secondary_y": True}]])
    figure12.add_trace(
    go.Bar(x=Borough_sort12, y=median2_df['Tube DistanceMiles'], name="Distance"),
    secondary_y=False,
    )

    figure12.add_trace(
    go.Scatter(x=Borough_sort12, y=median2_df['Affordability percentage'], name="Affordability percentage"),
    secondary_y=True,
    )
    figure12.update_layout(xaxis = dict(tickfont = dict(size=10)))
    figure12.update_yaxes(title_text="Distance (miles)", secondary_y=False)
    figure12.update_yaxes(title_text="Affordability percentage", secondary_y=True)
    #figure12 = px.bar(median2_df, x = "Borough", y= "Tube DistanceMiles",
                      #labels={
                          #"Tube DistanceMiles": "Distance (miles)"})
    #figure12.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    

###Average/median price by tube zone
if which == "Average":
    grouped3_df = df.groupby("Tube Zone")
    mean3_df = grouped3_df.mean()
    Tube_Zone = ["1","2","3","4","5","6","7"]
    mean3_df["Tube Zone"] = Tube_Zone
    #st.write(mean_df)
    figure6 = px.bar(mean3_df, x = "Tube Zone", y = "Price",
               labels={
                   "Price": "Average price (£)"})
    #figure6.update_xaxes(range=[0, 6])
    figure6.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")
else:
    grouped3_df = df.groupby("Tube Zone")
    median3_df = grouped3_df.median()
    Tube_Zone = ["1","2","3","4","5","6","7"]
    median3_df["Tube Zone"] = Tube_Zone
    #st.write(median_df)
    figure6 = px.bar(median3_df, x = "Tube Zone", y = "Price",
               labels={
                   "Price": "Median price (£)"})
    #figure6.update_xaxes(range=[0, 6])
    figure6.add_hline(y=Price_parameter, line_width =3,
                      line_dash = "dash", line_color="black",
                      annotation_text="Affordability line",
                      annotation_position="top right")


###Affordability by tube zone
grouped14_df = df.groupby("Tube Zone").agg({'Latitude':'count', 'Affordability': 'sum'}).reset_index()
sum14_df = grouped14_df.sum()
Tube_Zone = ["1","2","3","4","5","6","7"]
sum14_df["Tube Zone"] = Tube_Zone
grouped14_df["Affordability fraction"] = grouped14_df["Affordability"]/grouped14_df["Latitude"]
figure14 = px.bar(grouped14_df, x = "Tube Zone", y = "Affordability fraction",
            labels={
                "Price": "Average price (£)"})


###Affordability by detailed region
grouped8_df = df.groupby('2').agg({'Latitude':'count', 'Affordability': 'sum'}).reset_index()
Geography2 = ["Central", "East", "North", "North-East", "North-West",
              "South", "South-East", "South-West", "West"]
grouped8_df["Geography Detailed"] = Geography2
grouped8_df["Affordability fraction"] = grouped8_df["Affordability"]/grouped8_df["Latitude"]
grouped8_df = grouped8_df.astype({'Geography Detailed': str})
#st.write(mean_df)
figure8 = px.line(grouped8_df, x = "Geography Detailed", y = "Affordability fraction",
            labels={
                "Price": "Average price (£)"})
#st.write(grouped8_df)


###Affordability by region for combined line and bar chart
attempt_df = df.groupby(["2","Affordable?"]).agg({'One': ['count']})
#st.write(attempt_df)
length_attempt = attempt_df.index
#st.write(attempt_df)
Geographyattempt = ["Central", "Central", "East", "East", "North", "North", "North-East", "North-East", "North-West", "North-West",
                 "South", "South", "South-East", "South-East", "South-West", "South-West", "West", "West"]
Affordable = ["Affordable", "Not Affordable", "Affordable", "Not Affordable", "Affordable", "Not Affordable",
               "Affordable", "Not Affordable", "Affordable", "Not Affordable", "Affordable", "Not Affordable",
               "Affordable", "Not Affordable", "Affordable", "Not Affordable", "Affordable", "Not Affordable"]
attempt_df["Geography Detailed"] = Geographyattempt
attempt_df["Affordable?"] = Affordable
selected_columns = attempt_df[["Geography Detailed","Affordable?","One"]]
new_df = selected_columns.copy()
new_df.columns = new_df.columns.droplevel(-1)
new_df = new_df.astype({'One': float})
new_df = new_df.astype({'Geography Detailed': str})
new_df = new_df.astype({'Affordable?': str})
index2 = new_df.index
limit = len(index2)/2
#for i in range (0, int(limit)):
    #if i == 0:
        #one = (new_df.at[0, 'One']/df.at[1, 'One'])/2
    #if i == 1:
        #two = (new_df.at[2, 'One']/df.at[3, 'One'])/2
    #if i == 2:
        #three = (new_df.at[4, 'One']/df.at[5, 'One'])/2
    #if i == 3:
        #four = (new_df.at[6, 'One']/df.at[7, 'One'])/2
    #if i == 4:
        #five = (new_df.at[8, 'One']/df.at[9, 'One'])/2
    #if i == 5:
        #six = (new_df.at[10, 'One']/df.at[11, 'One'])/2
    #if i == 6:
        #seven = (new_df.at[12, 'One']/df.at[13, 'One'])/2
    #if i == 7:
        #eight = (new_df.at[14, 'One']/df.at[15, 'One'])/2
    #if i == 8:
        #nine = (new_df.at[16, 'One']/new_df.at[17, 'One'])/2
#affordability = [one, one, two, two, three, three, four, four, five,
                 #five, six, six, seven, seven, eight, eight, nine, nine]
#new_df['affordability'] = affordability
#figuretry = px.line(grouped8_df, x = "Geography Detailed", y = "Affordability fraction")
affordabilityf = [grouped8_df.at[0, 'Affordability fraction'], grouped8_df.at[0, 'Affordability fraction'],
                  grouped8_df.at[1, 'Affordability fraction'], grouped8_df.at[1, 'Affordability fraction'],
                  grouped8_df.at[2, 'Affordability fraction'], grouped8_df.at[2, 'Affordability fraction'],
                  grouped8_df.at[3, 'Affordability fraction'], grouped8_df.at[3, 'Affordability fraction'],
                  grouped8_df.at[4, 'Affordability fraction'], grouped8_df.at[4, 'Affordability fraction'],
                  grouped8_df.at[5, 'Affordability fraction'], grouped8_df.at[5, 'Affordability fraction'],
                  grouped8_df.at[6, 'Affordability fraction'], grouped8_df.at[6, 'Affordability fraction'],
                  grouped8_df.at[7, 'Affordability fraction'], grouped8_df.at[7, 'Affordability fraction'],
                  grouped8_df.at[8, 'Affordability fraction'], grouped8_df.at[8, 'Affordability fraction']]

#affordabilityf = [grouped8_df.at[0, 'Affordability fraction'], NaN,
                  #grouped8_df.at[1, 'Affordability fraction'], NaN,
                  #grouped8_df.at[2, 'Affordability fraction'], NaN,
                  #grouped8_df.at[3, 'Affordability fraction'], NaN,
                  #grouped8_df.at[4, 'Affordability fraction'], NaN,
                  #grouped8_df.at[5, 'Affordability fraction'], NaN,
                  #grouped8_df.at[6, 'Affordability fraction'], NaN,
                  #grouped8_df.at[7, 'Affordability fraction'], NaN,
                  #grouped8_df.at[8, 'Affordability fraction'], NaN]
new_df['affordabilityf'] = affordabilityf
#st.write(new_df)
new_df = new_df.astype({'affordabilityf': float})
#figuretry = px.line(new_df, x = "Geography Detailed", y = "affordabilityf")
print(affordabilityf)
#st.write(new_df)
#st.write(grouped8_df)
print(attempt_df.dtypes)

no_affordable = [new_df['One'].iloc[0], new_df['One'].iloc[2],
                 new_df['One'].iloc[4], new_df['One'].iloc[6],
                 new_df['One'].iloc[8], new_df['One'].iloc[10],
                 new_df['One'].iloc[12], new_df['One'].iloc[14],
                 new_df['One'].iloc[16]]
no_nonaffordable = [new_df['One'].iloc[1], new_df['One'].iloc[3],
                    new_df['One'].iloc[5], new_df['One'].iloc[7],
                    new_df['One'].iloc[9], new_df['One'].iloc[11],
                    new_df['One'].iloc[13], new_df['One'].iloc[15],
                    new_df['One'].iloc[17]]
stacked_df = pd.DataFrame(list(zip(no_affordable, no_nonaffordable)), columns = ['Affordable', 'Non-affordable'])
stacked_df['Affordability'] = (stacked_df['Affordable']/(stacked_df['Non-affordable']+stacked_df['Affordable']))*100
stacked_df['Region'] = Geography2
stackedsort_df = stacked_df.sort_values('Affordability', ascending=False)
Geography_order = [str(stackedsort_df['Region'].iloc[0]), str(stackedsort_df['Region'].iloc[1]),
                   str(stackedsort_df['Region'].iloc[2]), str(stackedsort_df['Region'].iloc[3]),
                   str(stackedsort_df['Region'].iloc[4]), str(stackedsort_df['Region'].iloc[5]),
                   str(stackedsort_df['Region'].iloc[6]), str(stackedsort_df['Region'].iloc[7]),
                   str(stackedsort_df['Region'].iloc[8])]
#st.write(stacked_df)
print(Geography_order)
fig12 = make_subplots(specs=[[{"secondary_y": True}]])

fig12.add_trace(
    go.Bar(x=Geography_order, y=stackedsort_df['Affordable'], name="Non-affordable"),
    secondary_y=False,
)

fig12.add_trace(
    go.Bar(x=Geography_order, y=stackedsort_df['Non-affordable'], name="Affordable"),
    secondary_y=False,
)

fig12.update_layout(barmode='stack')

fig12.add_trace(
    go.Scatter(x=Geography_order, y=stackedsort_df['Affordability'], name="Affordability"),
    secondary_y=True,
)

#fig12.update_layout(
    #title_text="Combined graph"
#)

# Set x-axis title
fig12.update_xaxes(title_text="Region")

# Set y-axes titles
fig12.update_yaxes(title_text="Count", secondary_y=False)
fig12.update_yaxes(title_text="Affordability", secondary_y=True)
###################fig12.update_layout(barmode='stack'), xaxis={'categoryorder':'total descending'})
#figureattempt = px.line(x=Geography2, y = stacked_df['Affordability'], yaxis='y1')
#figureattempt.add_bar(x=Geography2, y = stacked_df['Affordable'], yaxis='y2')
#figureattempt.add_bar(x=Geography2, y = stacked_df['Non-affordable'], yaxis='y2')
#figureattempt.update_layout(barmode='stack')
#figureattempt.update_layout
#st.write(figureattempt)
                      


###Affordability by tube zone combined graph
#df.fillna(0)
attempt2_df = df.groupby(["Tube Zone","Affordable?"]).agg({'One': ['count']})
sizee = len(attempt2_df)
if sizee == 14:
    attempt2_df = attempt2_df[:-2]
else:
    attempt2_df = attempt2_df[:-1]
#st.write(attempt2_df)
#st.write(attempt2_df)
attempt2_df['Tube Zone'] = ['1','1','2','2','3','3','4','4','5','5','6','6']
Affordable2 = ["Affordable", "Not Affordable", "Affordable", "Not Affordable", "Affordable", "Not Affordable",
               "Affordable", "Not Affordable", "Affordable", "Not Affordable", "Affordable", "Not Affordable"]
#st.write(attempt2_df)
attempt2_df['Affordable?'] = Affordable2
selected_columns2 = attempt2_df[["Tube Zone","Affordable?","One"]]
new2_df = selected_columns2.copy()
new2_df.columns = new2_df.columns.droplevel(-1)
no_affordable2 = [new2_df['One'].iloc[0], new2_df['One'].iloc[2],
                 new2_df['One'].iloc[4], new2_df['One'].iloc[6],
                 new2_df['One'].iloc[8], new2_df['One'].iloc[10]]
                 #new2_df['One'].iloc[12]]
no_nonaffordable2 = [new2_df['One'].iloc[1], new2_df['One'].iloc[3],
                    new2_df['One'].iloc[5], new2_df['One'].iloc[7],
                    new2_df['One'].iloc[9], new2_df['One'].iloc[11]]
                    #new2_df['One'].iloc[13]]
stacked2_df = pd.DataFrame(list(zip(no_affordable2, no_nonaffordable2)), columns = ['Affordable', 'Non-affordable'])
stacked2_df['Affordability'] = (stacked2_df['Affordable']/(stacked2_df['Non-affordable']+stacked2_df['Affordable']))*100
#st.write(stacked2_df)
fig13 = make_subplots(specs=[[{"secondary_y": True}]])

fig13.add_trace(
    go.Bar(x=Tube_Zone, y=stacked2_df['Affordable'], name="Non-affordable"),
    secondary_y=False,
)

fig13.add_trace(
    go.Bar(x=Tube_Zone, y=stacked2_df['Non-affordable'], name="Affordable"),
    secondary_y=False,
)

fig13.add_trace(
    go.Scatter(x=Tube_Zone, y=stacked2_df['Affordability'], name="Affordability"),
    secondary_y=True,
)

#fig13.update_layout(
    #title_text="Combined graph 2"
#)

# Set x-axis title
fig13.update_xaxes(title_text="Tube Zone")

# Set y-axes titles
fig13.update_yaxes(title_text="Count", secondary_y=False)
fig13.update_yaxes(title_text="Affordability", secondary_y=True)
fig13.update_layout(barmode='stack')




###Affordability by borough combined graph
attempt3_df = df.groupby(["Borough","Affordable?"]).agg({'One': ['count']})
#st.write(attempt3_df)
#st.write(attempt3_df)
attempt2_df['Affordable?'] = Affordable2
selected_columns3 = attempt3_df[["One"]]
new3_df = selected_columns3.copy()
new3_df.columns = new3_df.columns.droplevel(-1)
no_affordable3 = [new3_df['One'].iloc[0], new3_df['One'].iloc[2],
                  new3_df['One'].iloc[4], new3_df['One'].iloc[6],
                  new3_df['One'].iloc[8], new3_df['One'].iloc[10],
                  new3_df['One'].iloc[12], new3_df['One'].iloc[14],
                  new3_df['One'].iloc[16], new3_df['One'].iloc[18],
                  new3_df['One'].iloc[20], new3_df['One'].iloc[22],
                  new3_df['One'].iloc[24], new3_df['One'].iloc[26],
                  new3_df['One'].iloc[28], new3_df['One'].iloc[30],
                  new3_df['One'].iloc[32], new3_df['One'].iloc[34],
                  new3_df['One'].iloc[36], new3_df['One'].iloc[38],
                  new3_df['One'].iloc[40], new3_df['One'].iloc[42],
                  new3_df['One'].iloc[44], new3_df['One'].iloc[46],
                  new3_df['One'].iloc[48], new3_df['One'].iloc[50],
                  new3_df['One'].iloc[52], new3_df['One'].iloc[54],
                  new3_df['One'].iloc[56], new3_df['One'].iloc[58],
                  new3_df['One'].iloc[60], new3_df['One'].iloc[62],
                  new3_df['One'].iloc[64]]
                 
no_nonaffordable3 = [new3_df['One'].iloc[1], new3_df['One'].iloc[3],
                     new3_df['One'].iloc[5], new3_df['One'].iloc[7],
                     new3_df['One'].iloc[9], new3_df['One'].iloc[11],
                     new3_df['One'].iloc[13], new3_df['One'].iloc[15],
                     new3_df['One'].iloc[17], new3_df['One'].iloc[19],
                     new3_df['One'].iloc[21], new3_df['One'].iloc[23],
                     new3_df['One'].iloc[25], new3_df['One'].iloc[27],
                     new3_df['One'].iloc[29], new3_df['One'].iloc[31],
                     new3_df['One'].iloc[33], new3_df['One'].iloc[35],
                     new3_df['One'].iloc[37], new3_df['One'].iloc[39],
                     new3_df['One'].iloc[41], new3_df['One'].iloc[43],
                     new3_df['One'].iloc[45], new3_df['One'].iloc[47],
                     new3_df['One'].iloc[49], new3_df['One'].iloc[51],
                     new3_df['One'].iloc[53], new3_df['One'].iloc[55],
                     new3_df['One'].iloc[57], new3_df['One'].iloc[59],
                     new3_df['One'].iloc[61], new3_df['One'].iloc[63],
                     new3_df['One'].iloc[65]]
stacked3_df = pd.DataFrame(list(zip(no_affordable3, no_nonaffordable3)), columns = ['Affordable', 'Non-affordable'])
stacked3_df['Affordability'] = (stacked3_df['Affordable']/(stacked3_df['Non-affordable']+stacked3_df['Affordable']))*100
stacked3_df["Borough"] = Borough
stackedsort2_df = stacked3_df.sort_values('Affordability', ascending=False)
Borough_order = [str(stackedsort2_df['Borough'].iloc[0]), str(stackedsort2_df['Borough'].iloc[1]),
                 str(stackedsort2_df['Borough'].iloc[2]), str(stackedsort2_df['Borough'].iloc[3]),
                 str(stackedsort2_df['Borough'].iloc[4]), str(stackedsort2_df['Borough'].iloc[5]),
                 str(stackedsort2_df['Borough'].iloc[6]), str(stackedsort2_df['Borough'].iloc[7]),
                 str(stackedsort2_df['Borough'].iloc[8]), str(stackedsort2_df['Borough'].iloc[9]),
                 str(stackedsort2_df['Borough'].iloc[10]), str(stackedsort2_df['Borough'].iloc[11]),
                 str(stackedsort2_df['Borough'].iloc[12]), str(stackedsort2_df['Borough'].iloc[13]),
                 str(stackedsort2_df['Borough'].iloc[14]), str(stackedsort2_df['Borough'].iloc[15]),
                 str(stackedsort2_df['Borough'].iloc[16]), str(stackedsort2_df['Borough'].iloc[17]),
                 str(stackedsort2_df['Borough'].iloc[18]), str(stackedsort2_df['Borough'].iloc[19]),
                 str(stackedsort2_df['Borough'].iloc[20]), str(stackedsort2_df['Borough'].iloc[21]),
                 str(stackedsort2_df['Borough'].iloc[22]), str(stackedsort2_df['Borough'].iloc[23]),
                 str(stackedsort2_df['Borough'].iloc[24]), str(stackedsort2_df['Borough'].iloc[25]),
                 str(stackedsort2_df['Borough'].iloc[26]), str(stackedsort2_df['Borough'].iloc[27]),
                 str(stackedsort2_df['Borough'].iloc[28]), str(stackedsort2_df['Borough'].iloc[29]),
                 str(stackedsort2_df['Borough'].iloc[30]), str(stackedsort2_df['Borough'].iloc[31])]
#st.write(stacked3_df)
fig14 = make_subplots(specs=[[{"secondary_y": True}]])

fig14.add_trace(
    go.Bar(x=Borough_order, y=stackedsort2_df['Affordable'], name="Non-affordable"),
    secondary_y=False,
)

fig14.add_trace(
    go.Bar(x=Borough_order, y=stackedsort2_df['Non-affordable'], name="Affordable"),
    secondary_y=False,
)

fig14.add_trace(
    go.Scatter(x=Borough_order, y=stackedsort2_df['Affordability'], name="Affordability"),
    secondary_y=True,
)

#fig14.update_layout(
    #title_text="Combined graph 3"
#)

# Set x-axis title
fig14.update_xaxes(title_text="Borough")

# Set y-axes titles
fig14.update_yaxes(title_text="Count", secondary_y=False)
fig14.update_yaxes(title_text="Affordability", secondary_y=True)
fig14.update_layout(barmode='stack')#, xaxis={'categoryorder':'total descending'})
fig14.update_layout(xaxis = dict(tickfont = dict(size=10)))


Geography3 = ["Central", "East", "North", "North East", "North West",
                 "South", "South East", "South West", "West"]

###Affordability by distance from tube
#1
trail1_df = df[df['Geography Detailed']==Geography3[0]]
range1 = len(trail1_df.index)
trail1_df.index = range(range1)
#st.write(trail1_df)
trail01_df = trail1_df.groupby(pd.cut(trail1_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail01_df)
trail01_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail01_df["Affordability fraction"] = (trail01_df["Affordability"]/(trail01_df["One"]+trail01_df["Affordability"]))*100
#trail01 = px.bar(trail01_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail01)
#2
trail2_df = df[df['Geography Detailed']==Geography3[1]]
range2 = len(trail2_df.index)
trail2_df.index = range(range2)
#st.write(trail2_df)
trail02_df = trail2_df.groupby(pd.cut(trail2_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail02_df)
trail02_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail02_df["Affordability fraction"] = (trail02_df["Affordability"]/(trail02_df["One"]+trail02_df["Affordability"]))*100
#trail02 = px.bar(trail02_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail02)
#3
trail3_df = df[df['Geography Detailed']==Geography3[2]]
range3 = len(trail3_df.index)
trail3_df.index = range(range3)
#st.write(trail3_df)
trail03_df = trail3_df.groupby(pd.cut(trail3_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail03_df)
trail03_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail03_df["Affordability fraction"] = (trail03_df["Affordability"]/(trail03_df["One"]+trail03_df["Affordability"]))*100
#trail03 = px.bar(trail03_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail03)
#4
trail4_df = df[df['Geography Detailed']==Geography3[3]]
range4 = len(trail4_df.index)
trail4_df.index = range(range4)
#st.write(trail4_df)
trail04_df = trail4_df.groupby(pd.cut(trail4_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail04_df)
trail04_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail04_df["Affordability fraction"] = (trail04_df["Affordability"]/(trail04_df["One"]+trail04_df["Affordability"]))*100
#trail04 = px.bar(trail04_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail04)
#5
trail5_df = df[df['Geography Detailed']==Geography3[4]]
range5= len(trail5_df.index)
trail5_df.index = range(range5)
#st.write(trail5_df)
trail05_df = trail5_df.groupby(pd.cut(trail5_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail05_df)
trail05_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail05_df["Affordability fraction"] = (trail05_df["Affordability"]/(trail05_df["One"]+trail05_df["Affordability"]))*100
#trail05 = px.bar(trail05_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail05)
#6
trail6_df = df[df['Geography Detailed']==Geography3[5]]
range6 = len(trail6_df.index)
trail6_df.index = range(range6)
#st.write(trail6_df)
trail06_df = trail6_df.groupby(pd.cut(trail6_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail06_df)
trail06_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail06_df["Affordability fraction"] = (trail06_df["Affordability"]/(trail06_df["One"]+trail06_df["Affordability"]))*100
#trail06 = px.bar(trail06_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail06)
#7
trail7_df = df[df['Geography Detailed']==Geography3[6]]
range7 = len(trail7_df.index)
trail7_df.index = range(range7)
#st.write(trail7_df)
trail07_df = trail7_df.groupby(pd.cut(trail7_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail07_df)
trail07_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail07_df["Affordability fraction"] = (trail07_df["Affordability"]/(trail07_df["One"]+trail07_df["Affordability"]))*100
#trail07 = px.bar(trail07_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail07)
#8
trail8_df = df[df['Geography Detailed']==Geography3[7]]
range8 = len(trail8_df.index)
trail8_df.index = range(range8)
#st.write(trail8_df)
trail08_df = trail8_df.groupby(pd.cut(trail8_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail08_df)
trail08_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail08_df["Affordability fraction"] = (trail08_df["Affordability"]/(trail08_df["One"]+trail08_df["Affordability"]))*100
#trail08 = px.bar(trail08_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail08)
#9
trail9_df = df[df['Geography Detailed']==Geography3[8]]
range9 = len(trail9_df.index)
trail9_df.index = range(range9)
#st.write(trail9_df)
trail09_df = trail9_df.groupby(pd.cut(trail9_df["Tube DistanceMiles"], np.arange(0, 3.0+0.1, 0.1))).sum()
#st.write(trail09_df)
trail09_df["Distance from tube"] = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                                     "0.6" ,"0.7", "0.8", "0.9", "1.0",
                                     "1.1" ,"1.2", "1.3", "1.4", "1.5",
                                     "1.6" ,"1.7", "1.8", "1.9", "2.0",
                                     "2.1" ,"2.2", "2.3", "2.4", "2.5",
                                     "2.6" ,"2.7", "2.8", "2.9", "3.0"]
trail09_df["Affordability fraction"] = (trail09_df["Affordability"]/(trail09_df["One"]+trail09_df["Affordability"]))*100
#trail09 = px.bar(trail09_df, x = "Distance from tube", y = "Affordability fraction")
#st.write(trail09)


tube_distance = ["0.1" ,"0.2", "0.3", "0.4", "0.5",
                 "0.6" ,"0.7", "0.8", "0.9", "1.0",
                 "1.1" ,"1.2", "1.3", "1.4", "1.5",
                 "1.6" ,"1.7", "1.8", "1.9", "2.0",
                 "2.1" ,"2.2", "2.3", "2.4", "2.5",
                 "2.6" ,"2.7", "2.8", "2.9", "3.0"]

figure_combine = make_subplots(rows=3, cols=3, start_cell="top-left")
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail01_df["Affordability fraction"], name = Geography2[0], dy = 25),
              row=1, col=1)
figure_combine.add_trace(go.Scatter(x=tube_distance, y =[trail01_df["Affordability fraction"].max()]*len(trail01_df), mode='lines', line_color='red'))
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail02_df["Affordability fraction"], name = Geography2[1], dy = 25),
              row=1, col=2)
#figure_combine.add_trace(go.Scatter(x=tube_distance, yaxis2 =[trail02_df["Affordability fraction"].max()]*len(trail02_df), mode='lines', line_color='red'))
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail03_df["Affordability fraction"], name = Geography2[2], dy = 25),
              row=1, col=3)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail04_df["Affordability fraction"], name = Geography2[3], dy = 25),
              row=2, col=1)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail05_df["Affordability fraction"], name = Geography2[4], dy = 25),
              row=2, col=2)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail06_df["Affordability fraction"], name = Geography2[5], dy = 25),
              row=2, col=3)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail07_df["Affordability fraction"], name = Geography2[6], dy = 25),
              row=3, col=1)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail08_df["Affordability fraction"], name = Geography2[7], dy = 25),
              row=3, col=2)
figure_combine.add_trace(go.Scatter(x=tube_distance, y=trail09_df["Affordability fraction"], name = Geography2[8], dy = 25),
              row=3, col=3)
figure_combine.update_layout(yaxis = dict(range=[0, 100]))
figure_combine.update_layout(yaxis2 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis3 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis4 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis5 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis6 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis7 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis8 = dict(range=[0, 100]))
figure_combine.update_layout(yaxis9 = dict(range=[0, 100]))
#st.write(figure_combine)



figure_combine2 = make_subplots(rows=5, cols=2, start_cell="top-left")
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail01_df["Affordability fraction"], name = Geography2[0]),
              row=1, col=1)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail02_df["Affordability fraction"], name = Geography2[1]),
              row=1, col=2)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail03_df["Affordability fraction"], name = Geography2[2]),
              row=2, col=1)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail04_df["Affordability fraction"], name = Geography2[3]),
              row=2, col=2)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail05_df["Affordability fraction"], name = Geography2[4]),
              row=3, col=1)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail06_df["Affordability fraction"], name = Geography2[5]),
              row=3, col=2)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail07_df["Affordability fraction"], name = Geography2[6]),
              row=4, col=1)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail08_df["Affordability fraction"], name = Geography2[7]),
              row=4, col=2)
figure_combine2.add_trace(go.Scatter(x=tube_distance, y=trail09_df["Affordability fraction"], name = Geography2[8]),
              row=5, col=1)
#st.write(figure_combine2)


figure_lines = make_subplots(specs=[[{"secondary_y": False}]])

figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail01_df["Affordability fraction"], name = Geography2[0]),
    secondary_y=False,
)
#figure_lines.add_trace(go.Scatter(x=tube_distance, y =[trail01_df["Affordability fraction"].min()]*len(trial01_df), mode='lines', line_color='red'))
#figure_lines.add_hline(y=Price_parameter, line_width =3,
                      #line_dash = "dash", line_color="black",
                      #annotation_text="Affordability line",
                      #annotation_position="top right")
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail02_df["Affordability fraction"], name = Geography2[1]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail03_df["Affordability fraction"], name = Geography2[2]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail04_df["Affordability fraction"], name = Geography2[3]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail05_df["Affordability fraction"], name = Geography2[4]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail06_df["Affordability fraction"], name = Geography2[5]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail07_df["Affordability fraction"], name = Geography2[6]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail08_df["Affordability fraction"], name = Geography2[7]),
    secondary_y=False,
)
figure_lines.add_trace(
    go.Scatter(x=tube_distance, y=trail09_df["Affordability fraction"], name = Geography2[8]),
    secondary_y=False,
)
st.write(figure_lines)

figure_box = px.box(df, x="Geography Detailed", y="Price") #, points = False)
figure_box.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
figure_box.update_yaxes(range=[0, 5500000])
#figure_box.update_traces(boxpoints=False)
#st.write(figure_box)


figure_box2 = go.Figure()
figure_box2.add_trace(
    go.Box(x=df["Geography Detailed"], y=df["Price"], 
    marker_color='darkblue',
    boxmean=True 
))
figure_box2.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
figure_box2.update_yaxes(range=[0, 5500000])
#st.write(figure_box2)

image = Image.open('Screenshot 2022-03-31 214437.jpg')

st.image(image, caption='Ridgeplot')




#n_rows = 3
#n_cols = 3
#n_graphs = 3
#rows = [st.container() for _ in range(n_rows)]
#cols_per_row = [r.columns(n_cols) for r in rows]
#cols = [column for row in cols_per_row for column in row]
#graphs = ["trail01","trail02","trail03","trail04","trail05","trail06","trail07","trail08","trail09"]
#for image_index, graph in enumerate(graphs):
    #cols[image_index].image(graph)


###Violin plots
#figure_violin = sns.violinplot(x=df["Geography Detailed"], y=df["Price"]) #hue="smoker",
#st.write(figure_violin)


###Ridge plot
#sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

#data = sns.load_dataset(df)
#pal = sns.cubehelix_palette(len(df["Geography Detailed"].unique()), start=1.4, rot=-.25, light=.7, dark=.4)
#g = sns.FacetGrid(flights, row="year", hue="year", aspect=20, height=.5, palette=pal)

#g.map(sns.kdeplot, "passengers", bw_adjust=.6, cut=5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
#g.map(sns.kdeplot, "passengers", bw_adjust=.6, cut=5, clip_on=False, color="w", lw=2)
#g.map(plt.axhline, y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

#def label(x, color, label):
    #ax = plt.gca()
    #ax.text(0, .1, label, fontweight="bold", color=color,
            #ha="left", va="center", transform=ax.transAxes)

#g.map(label, "year")
#g.fig.subplots_adjust(hspace=-.7)
#g.set(yticks=[], xlabel="", ylabel="", xlim=(None, 680), title="")
#g.despine(bottom=True, left=True)
#plt.show()



###simple map
#df.rename({'Longitude':'lon'}, axis='columns', inplace=True)
#df.rename({'Latitude':'lat'}, axis='columns', inplace=True)
#st.map(df.dropna(subset=['lon', 'lat']))


###Affordability write out
st.subheader("How the affordability changes by salary:")  
st.write(figure2)
st.subheader("Stamp duty needed for " + stamp_duty)
st.write(figurestamp)
st.subheader('The location density of available properties:')
map(df)
st.subheader('Lets look at the affordability by region: ')
st.write(fig12)
st.subheader('Lets looks at the distribution of property prices in each region (Outliers are removed and plotted as indivdual points)')
st.write(figure_box2)
st.subheader('Breaking this down further to the borough level: ')
st.write(fig14)
st.subheader('This is how the affordability changes by tube zone: ')
st.write(fig13)
st.subheader('How the affordability by distance from a tbe station varies by region')
st.write(figure_combine)



###Appendix write-out 
st.subheader("How your budget compares: ")
if which == "Average":
    st.subheader("Average price by region")
else:
    st.subheader("Median price by region")
st.write(figure7)
if which == "Average":
    st.subheader("Average price by borough")
else:
    st.subheader("Median price by borough")
st.write(figure4)
if which == "Average":
    st.subheader("Average price by tube zone")
else:
    st.subheader("Median price by tube zone")
st.write(figure6)
#st.subheader("Number of properties by region")
#st.write(figure10)
#st.subheader("Number of properties by Borough")
#st.write(figure11)
if which == "Average":
    st.subheader("Average distance from tube by region")
else:
    st.subheader("Average distance from tube by region")
st.write(figure13)
if which == "Average":
    st.subheader("Average distance from tube by borough")
else:
    st.subheader("Average distance from tube by borough")
st.write(figure12)
    


