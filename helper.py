import numpy as np
import streamlit as st

def fetch_medal_tally(df, country, year):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','Games', 'Year', 'City','Sport','Event', 'Medal' ])
    flag = 0
    if country == 'Overall' and year == 'Overall':
        temp_df = medal_df
    if country!= 'Overall' and year=='Overall':
        flag = 1
        temp_df = medal_df[medal_df['region']==country]
    if country=='Overall' and year!='Overall':
        temp_df = medal_df[medal_df['Year']==year]
    if country!='Overall' and year!='Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year']==year)]
    if flag == 1:
        x =  temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year', ascending = True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    x['Total'] = x['Gold']+x['Silver'] + x['Bronze']
    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    medal_tally['Gold']   = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.insert(0, 'Overall')
    return years, countries


def data_over_time(df, col):
    data_over_times = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    data_over_times['Year'] = data_over_times['Year'].astype('int')
    data_over_times['count'] = data_over_times['count'].astype('int')
    data_over_times.sort_values(by='Year', ascending=True, inplace=True)
    return data_over_times


def most_successful(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport !='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on = 'Name', right_on = 'Name')[['Name','region','Sport','count']].drop_duplicates('Name')
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games','Year', 'City','Sport', 'Event', 'Medal'], inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region']==country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on = 'Name', right_on = 'Name')[['Name','region','Sport','count']].drop_duplicates('Name')
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset =['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)
    if sport != 'Overall':
        athlete_df = athlete_df[athlete_df['Sport'] == sport ]
    return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset =['Name', 'region'])
    men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on = 'Year', how = 'left')
    final.rename(columns = {'Name_x':'Male', 'Name_y': 'Female'}, inplace = True)
    final.fillna(0, inplace = True)
    return final

