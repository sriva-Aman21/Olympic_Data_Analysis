import streamlit as st
import pandas as pd
import numpy as np
import preprocessor , helper 
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import zipfile 

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)


with zipfile.ZipFile('athlete_events.zip') as z:
    with z.open('athlete_events.csv') as f:
        df = pd.read_csv(f)
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://static.vecteezy.com/system/resources/previews/022/823/310/original/paris-2024-official-olympic-games-logo-symbol-abstract-design-illustration-free-vector.jpg', width=300)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Home', 'Medal Tally','Overall Analysis','Country-wise Analysis', 'Athlete-wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Home':
    st.title('🏅 Olympics Analysis Dashboard')
    st.markdown('---')
    
    # Project Description
    st.header('📋 Project Overview')
    st.write("""
    Welcome to the **Olympics Analysis Dashboard**! This comprehensive web application provides deep insights 
    into Olympic Games data spanning multiple decades and countries.
    
    This project analyzes historical Olympic data to uncover patterns, trends, and interesting statistics 
    about participating nations, athletes, and sports.
    """)
    
    st.header('📊 What This Dashboard Offers')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('🥇 Medal Tally')
        st.write("""
        - View overall medal counts by country
        - Filter by specific years
        - Compare country performance across Olympics
        - See historical medal achievements
        """)
    
    with col2:
        st.subheader('📈 Overall Analysis')
        st.write("""
        - Total Olympics editions hosted
        - Number of host cities
        - Sports and events statistics
        - Participating nations over time
        - Most successful athletes
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('🌍 Country-wise Analysis')
        st.write("""
        - Medal performance by year
        - Sport-specific performance
        - Country-wise heatmaps
        - Top athletes per country
        """)
    
    with col2:
        st.subheader('👥 Athlete-wise Analysis')
        st.write("""
        - Age distribution of athletes
        - Age patterns by sport
        - Height vs Weight analysis
        - Gender participation trends
        """)
    
    st.markdown('---')
    
    # Quick Stats
    st.header('⚡ Quick Statistics')
    col1, col2, col3 = st.columns(3)
    
    editions = df['Year'].unique().shape[0] - 1
    nations = df['region'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    
    with col1:
        st.metric(label="Olympic Editions", value=editions)
    with col2:
        st.metric(label="Nations Participated", value=nations)
    with col3:
        st.metric(label="Total Athletes", value=athletes)
    
    st.markdown('---')
    
    # How to Use
    st.header('🚀 How to Use')
    st.write("""
    1. **Select an Analysis** from the sidebar menu
    2. **Customize Your View** using filters and options
    3. **Explore the Data** through interactive charts and tables
    4. **Compare Countries & Athletes** across different Olympics
    
    Click on any section in the sidebar to get started!
    """)
    
    st.markdown('---')
    st.info('💡 Tip: Use the sidebar to navigate between different analysis sections and customize your view.')

elif user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')    
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' - Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':    
        st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics')

    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Host Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)    
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)


    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')  
    st.subheader('Participating Nations over the years')
    st.plotly_chart(fig)
    
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')  
    st.subheader('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')    
    st.subheader('Athletes over the years')
    st.plotly_chart(fig)

    st.title('No. of Events over time for every sport')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis': 
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()  
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal Tally over the years') 
    st.plotly_chart(fig)

    st.title(selected_country + ' Performance in different sports over the years')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    
    st.pyplot(fig)

    st.title('Top 10 most Successful Athletes of ' + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)


elif user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)    


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-of-war', 'Athletics', 'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'wrestling',
    'Water polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    'Tennis', 'Golf', 'Softball', 'Archery','Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',
    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    # Pre-filter for Gold medals and valid ages to keep the loop clean
    gold_df = athlete_df[(athlete_df['Medal'] == 'Gold') & (athlete_df['Age'].notnull())]

    for sport in famous_sports:
        # Get the ages for this specific sport
        subset = gold_df[gold_df['Sport'] == sport]['Age']
        
        # CRITICAL CHECK: 
        # Must have more than 1 entry AND more than 1 unique value to draw a curve
        if len(subset) > 1 and subset.nunique() > 1:
            x.append(subset)
            name.append(sport)
        else:
            print(f"Skipping {sport}: Not enough data points or variance for a KDE curve.")

    # Check if we actually found any valid sports before plotting
    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title('Age Distribution of Gold Medalists by Sport')
        st.plotly_chart(fig)
    else:
        st.warning("No sports met the criteria for plotting.")

    st.title('Height vs Weight of Athletes') 
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
       
    temp_df = helper.weight_v_height(df, selected_sport)   
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data = temp_df, x='Weight', y='Height',hue = temp_df['Medal'],style = temp_df['Sex'],s = 60)
    
    st.pyplot(fig)

    st.title('Men vs Women Participation Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final,x= 'Year',y = ['Male','Female'])
    #fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
