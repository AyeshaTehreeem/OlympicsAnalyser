import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor, helper
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import scipy

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df, region_df)


st.sidebar.title("Olympics Analyser")
st.sidebar.image("olypics.jpg")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')

)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    if selected_year == 'Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country == 'Overall':
        st.title("Medal tally in "+ str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"'s overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title((selected_country) + "'s performance in " + str(selected_year) + " Olympics")

    medal_tally = helper.fetch_medal_tally(df,year = selected_year, country=selected_country)
    st.table(medal_tally)

if user_menu =='Overall Analysis':
    st.title("Top Statistics ")
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    st.title("No of events over time (every sport) ")
    fig, ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True, ax = ax)
    st.pyplot(fig)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Year', y='count')
    st.title("Participating nations over the years")
    fig.update_layout(
        xaxis_title='Editions',
        yaxis_title='No of participating nations'
    )
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='count')
    st.title("Events over the years")
    fig.update_layout(
        xaxis_title='Editions',
        yaxis_title='No of Events'
    )
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='count')
    st.title("Athletes over the years")
    fig.update_layout(
        xaxis_title='Editions',
        yaxis_title='No of Athletes'
    )
    st.plotly_chart(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_Sport = st.selectbox("Select a Sport", sport_list)
    x=helper.most_successful(df, selected_Sport)
    x = x.rename(columns={'count': 'Medals', 'region': 'Country'})
    st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country wise analysis")
    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    default_index = countries.index('USA')
    selected_country = st.sidebar.selectbox("Select a country", countries, index = default_index)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x = 'Year', y = 'Medal')
    st.title("Medal tally over the years for " + (selected_country))
    st.plotly_chart(fig)

    st.title((selected_country) + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize = (20, 20))
    sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + (selected_country))
    x = helper.most_successful_countrywise(df, selected_country)
    x = x.rename(columns={'count': 'Medals', 'region': 'Country'})
    x = x.reset_index(drop=True)
    st.table(x)


if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age','Gold Medalist','Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Rhythmic Gymnastics','Basketball', 'Judo', 'Football', 'Tug-of-war', 'Athletics', 'Swimming', 'Badminton', 'Wrestling',
                     'Shooting', 'Golf', 'Tennis', 'Boxing', 'Cycling', 'Volleyball', 'Archery', 'Baseball']
    for sport in famous_sports:
        temp_df = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]
        if not temp_df.empty:
            age_data = temp_df['Age'].dropna().tolist()  # Convert age data to a list
            x.append(age_data)
            name.append(sport)

    if x and name:  # Check if both lists are not empty
        fig = ff.create_distplot(x, name, show_rug=False, show_hist=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age of Gold medalists for famous sports")
        st.plotly_chart(fig)

    st.title("Height versus Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_Sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_height(df, selected_Sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=75)
    st.pyplot(fig)

    st.title("Men vs Women participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x = 'Year', y =['Male', 'Female'])
    st.plotly_chart(fig)