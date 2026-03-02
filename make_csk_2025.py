import pandas as pd

# Step 1 — Load CSVs
ball_df = pd.read_csv("IPl Ball-by-Ball 2008-2023.csv", dtype=str)  # read all as string
matches_df = pd.read_csv("IPL Mathces 2008-2023.csv", dtype=str)

# Step 2 — Replace 'Bangalore' with 'Bengaluru' in all string columns
for df in [ball_df, matches_df]:
    for col in df.columns:
        df[col] = df[col].str.replace("Bangalore", "Bengaluru", regex=False)

# Step 3 — Convert date to datetime and extract year
matches_df['date'] = pd.to_datetime(matches_df['date'], dayfirst=True, errors='coerce')
matches_df['year'] = matches_df['date'].dt.year

# Step 4 — Define RCB team name
rcb_names = ['Royal Challengers Bengaluru']

# Step 5 — Get all match IDs for RCB in 2025
rcb_matches_2025 = matches_df[
    (matches_df['year'] == 2025) &
    ((matches_df['team1'].isin(rcb_names)) | (matches_df['team2'].isin(rcb_names)))
]['id'].unique()

# Step 6 — Filter ball-by-ball data for these match IDs
rcb_ball_2025 = ball_df[ball_df['id'].isin(rcb_matches_2025)]

# Step 7 — Get rows where RCB was batting or bowling
rcb_batting = rcb_ball_2025[rcb_ball_2025['batting_team'].isin(rcb_names)]
rcb_bowling = rcb_ball_2025[rcb_ball_2025['bowling_team'].isin(rcb_names)]

# Step 8 — Collect all unique player names
players = set(rcb_batting['batsman']).union(
    set(rcb_batting['non_striker']),
    set(rcb_bowling['bowler']),
    set(rcb_batting['player_dismissed'].dropna())
)

# Step 9 — Clean and sort
players = sorted([p for p in players if pd.notna(p)])

# Step 10 — Save to Excel
df_players = pd.DataFrame(players, columns=['Player'])
df_players.to_excel("rcb.xlsx", index=False)

print("✅ Saved all RCB 2025 players to rcb.xlsx")
