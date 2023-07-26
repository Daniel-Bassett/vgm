import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu


@st.cache_data
def load_data():
    vgm = pd.read_csv('vgm_instruments.csv')
    vgm = vgm.rename(columns={'Date.1': 'Release_Year'})
    vgm['Release_Year'] = vgm['Release_Year'].astype('str')
    vgm = vgm.drop(['Date'], axis=1)

    years_list = vgm['Release_Year'].unique()
    games_list = vgm['Game'].unique()
    composers_list = vgm['Composer(s)'].unique()
    sources_list = vgm['Source'].unique()
    samples_list = vgm['Sample'].unique()
    return (vgm, years_list, games_list, composers_list, sources_list, samples_list)

vgm, years_list, games_list, composers_list, sources_list, samples_list = load_data()

years_list = vgm['Release_Year'].unique()
games_list = vgm['Game'].unique()
composers_list = vgm['Composer(s)'].unique()
sources_list = vgm['Source'].unique()
samples_list = vgm['Sample'].unique()

st.header('G-Boy\'s VGM Instrument Sources')
st.write('[data source](https://docs.google.com/spreadsheets/d/1brPjhDt2pW3H1nfThFMHVldDX9qzPRXujVGGwTZfgN8/edit#gid=0)')

selected = option_menu(
    menu_title=None,
    menu_icon='cast',
    default_index=0,
    options=['Data', 'Composer Stats'],
    orientation='horizontal',
    icons=['filter-square', 'graph-up'],
    styles= {'container': {
                'font-size': '12px'
    }}
)

df_container = st.container()

filter_container = st.container()

col1, col2, col3, col4, col5 = st.columns([4, 4, 4, 4, 4])


if selected == 'Data':
    with filter_container:
        with col1:
            game = st.multiselect(label='Game', options=games_list, placeholder='')
        with col2:
            composer = st.multiselect('Composer(s)', options=composers_list, placeholder='')
        with col3:
            year = st.multiselect('Release Year', options=years_list, placeholder='')
        with col4:
            source = st.multiselect('Source', sources_list, placeholder='')
        with col5:
            sample = st.multiselect('Sample', options=samples_list, placeholder='')
        if len(game) > 0:
            game_filter = vgm['Game'].isin(game)   
            vgm = vgm[game_filter]
        if len(composer) > 0:
            composer_filter = vgm['Composer(s)'].isin(composer)
            vgm = vgm[composer_filter]
        if len(year) > 0:
            year_filter = vgm['Release_Year'].isin(year)
            vgm = vgm[year_filter]
        if len(source) > 0:
            source_filter = vgm['Source'].isin(source)
            vgm = vgm[source_filter]
        if len(sample) > 0:
            sample_filter = vgm['Sample'].isin(sample)
            vgm = vgm[sample_filter]

    with df_container:
        st.dataframe(vgm)

if selected == 'Composer Stats':
    start_year, end_year = st.select_slider('select year range:', options=years_list, value=[years_list.min(), years_list.max()])
    temp_df = vgm.query('Release_Year.between(@start_year, @end_year)').groupby(['Composer(s)'])['Game'].nunique().sort_values(ascending=False).reset_index().rename(columns={'Game': 'Number of Games'})
    fig = px.bar(data_frame=temp_df.head(5), x='Composer(s)', y='Number of Games', title=f'Top 5 Composers: {start_year} to {end_year}')
    st.plotly_chart(fig, use_container_width=True)
