# %% Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pybaseball import batting_stats

# --- Define the list of players ---
players_list = [
    "William Contreras",
    "Luis Robert Jr.",
    "Jarren Duran",
    "Kyle Tucker",
    "Josh Naylor",
    "Ronald Acuña Jr.",
    "Jazz Chisholm Jr.",
    "Adley Rutschman",
    "Luis Arraez",
    "Ozzie Albies",
    "Gleyber Torres",
    "Alex Verdugo",
    "Lane Thomas",
    "Tyler O'Neill",
    "Cody Bellinger",
    "Average MLB Player"  # ✅ Added here
]

# --- Load career batting stats ---
@st.cache_data
def load_data():
    # Pull all batting stats from 2019 to 2024 (covers their careers)
    all_stats = batting_stats(2019, 2024)
    return all_stats

raw_data = load_data()

# --- Data Preparation ---
# Filter only the players we want (excluding "Average MLB Player" for now)
filtered_data = raw_data[raw_data['Name'].isin(players_list[:-1])]

# Count how many seasons each player has
season_counts = filtered_data.groupby('Name')['Season'].count().reset_index()
season_counts.rename(columns={'Season': 'Seasons'}, inplace=True)

# Group by player and sum/average stats
career_summary = filtered_data.groupby('Name').agg({
    'H': 'sum',
    'AB': 'sum',
    'OPS': 'mean',
    'WAR': 'sum',
    'HR': 'sum',
    'RBI': 'sum',
    'SB': 'sum',
    'G': 'sum'
}).reset_index()

# Merge season counts
career_summary = career_summary.merge(season_counts, on='Name')

# Calculate career Batting Average
career_summary['AVG'] = career_summary['H'] / career_summary['AB']

# Calculate per season stats
career_summary['HR per Season'] = career_summary['HR'] / career_summary['Seasons']
career_summary['RBI per Season'] = career_summary['RBI'] / career_summary['Seasons']
career_summary['SB per Season'] = career_summary['SB'] / career_summary['Seasons']
career_summary['Games per Season'] = career_summary['G'] / career_summary['Seasons']

# Round for clean display
career_summary = career_summary.round({
    'AVG': 3,
    'OPS': 3,
    'WAR': 2,
    'HR per Season': 1,
    'RBI per Season': 1,
    'SB per Season': 1,
    'Games per Season': 1
})

# --- Add "Average MLB Player" manually ---
average_mlb_player = pd.DataFrame([{
    'Name': 'Average MLB Player',
    'H': None,
    'AB': None,
    'OPS': 0.733,
    'WAR': 0.8,
    'HR': None,
    'RBI': None,
    'SB': None,
    'G': None,
    'Seasons': 1,
    'AVG': 0.243,
    'HR per Season': 18,
    'RBI per Season': 68,
    'SB per Season': 12,
    'Games per Season': 140
}])

# Combine with career data
full_summary = pd.concat([career_summary, average_mlb_player], ignore_index=True)

# --- Streamlit UI ---
st.title("⚾ MLB Career Stats and Season Averages Comparison")

st.sidebar.header("Select Players and Statistic")

# Sidebar: Select players
selected_players = st.sidebar.multiselect(
    "Select Players (now including Average MLB Player):",
    options=players_list,
    default=players_list[:5]
)

# Sidebar: Select statistic
stat_options = {
    "Batting Average (AVG)": "AVG",
    "On-base Plus Slugging (OPS)": "OPS",
    "Wins Above Replacement (WAR)": "WAR",
    "Average Home Runs per Season": "HR per Season",
    "Average RBIs per Season": "RBI per Season",
    "Average Stolen Bases per Season": "SB per Season",
    "Average Games Played per Season": "Games per Season"
}
selected_stat_label = st.sidebar.selectbox(
    "Select Statistic to Compare:",
    options=list(stat_options.keys())
)
selected_stat = stat_options[selected_stat_label]

# --- Filter Selected Players ---
plot_data = full_summary[full_summary['Name'].isin(selected_players)]

# --- Display Table ---
st.subheader(f"Career {selected_stat_label} Comparison")
st.dataframe(plot_data[['Name', selected_stat]].set_index('Name'))

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(plot_data['Name'], plot_data[selected_stat], edgecolor='black')
ax.set_xlabel(selected_stat_label)
ax.set_title(f"Career {selected_stat_label} Comparison")
ax.invert_yaxis()
st.pyplot(fig)







