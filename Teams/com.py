import pandas as pd
import os

# List of team Excel files
team_files = [
    "rcb.xlsx"
]

# Dictionary to store players per team
team_players = {}

# Loop through each file
for file in team_files:
    # Extract team short name from file name
    team_name = os.path.splitext(file)[0]  # "csk.xlsx" -> "csk"
    
    # Read Excel file
    df = pd.read_excel(file)
    
    # Ensure column name is 'player_name', otherwise try to detect
    if 'player_name' in df.columns:
        players = df['player_name'].dropna().tolist()
    else:
        # If column is not standard, take the first column
        players = df.iloc[:, 0].dropna().tolist()
    
    # Save to dictionary
    team_players[team_name] = players

# Print team-wise players separately
for team, players in team_players.items():
    print(f"\n=== {team.upper()} PLAYERS ===")
    for p in players:
        print(p)

# Optional: Save team-wise TXT files
for team, players in team_players.items():
    with open(f"{team}.txt", "w", encoding="utf-8") as f:
        for p in players:
            f.write(p + "\n")
    print(f"✅ Saved {team}.txt with {len(players)} players")
