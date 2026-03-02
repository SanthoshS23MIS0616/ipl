from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

app = Flask(__name__)

Team_1 = []
Team_2 = []
Team1_Squad = {}
Team2_Squad = {}

# ---------- Helper: filter dataset to last N years ----------
def filter_last_n_years(df, years=5, possible_date_cols=None):
    """Try to find a date column in df and return rows within last `years` years.
    If no parsable date column is found, return original df and print a warning.
    """
    if possible_date_cols is None:
        possible_date_cols = ['date', 'match_date', 'start_date', 'starttime', 'start_time']

    today = datetime.today()
    cutoff = today - timedelta(days=365 * years)

    for col in possible_date_cols:
        if col in df.columns:
            # try parsing
            try:
                parsed = pd.to_datetime(df[col], errors='coerce')
                if parsed.notna().sum() == 0:
                    continue
                mask = parsed >= cutoff
                filtered = df[mask].copy()
                print(f"Filtered using column '{col}' for last {years} years: {len(filtered)} rows kept")
                return filtered
            except Exception as e:
                print(f"Could not parse dates in column {col}: {e}")
                continue

    # try to find any column with 'date' in its name
    for col in df.columns:
        if 'date' in col.lower():
            try:
                parsed = pd.to_datetime(df[col], errors='coerce')
                if parsed.notna().sum() == 0:
                    continue
                mask = parsed >= cutoff
                filtered = df[mask].copy()
                print(f"Filtered using heuristic column '{col}' for last {years} years: {len(filtered)} rows kept")
                return filtered
            except Exception as e:
                print(f"Heuristic parse failed for {col}: {e}")
                continue

    print(f"WARNING: No parsable date column found. Returning full dataframe (no last-{years}-years filtering).")
    return df


# ---------- Reading files ----------
# The code expects the ball-by-ball CSV and matches CSV to exist in the same folder as this script
DATA_DIR = os.path.dirname(os.path.realpath(__file__))
BYB_CSV = os.path.join(DATA_DIR, 'IPl Ball-by-Ball 2008-2023.csv')
MATCH_CSV = os.path.join(DATA_DIR, 'IPL Mathces 2008-2023.csv')

try:
    byb = pd.read_csv(BYB_CSV)
    match = pd.read_csv(MATCH_CSV)
    # filter to last 5 years ONLY as requested
    byb_last5 = filter_last_n_years(byb, years=5)
    match_last5 = filter_last_n_years(match, years=5)
except FileNotFoundError as e:
    print("ERROR: CSV files not found. Make sure 'IPl Ball-by-Ball 2008-2023.csv' and 'IPL Mathces 2008-2023.csv' are in the same folder as this script.")
    raise

# Fantasy Points definitions
Batsman_points = {
    'Run': 1,
    'bFour': 1,
    'bSix': 2,
    '30Runs': 4,
    'Half_century': 8,
    'Century': 16,
    'Duck': -2,
    '170sr': 6,
    '150sr': 4,
    '130sr': 2,
    '70sr': -2,
    '60sr': -4,
    '50sr': -6,
}

Bowling_points = {
    'Wicket': 25,
    'LBW_Bowled': 8,
    '3W': 4,
    '4W': 8,
    '5W': 16,
    'Maiden': 12,
    '5rpo': 6,
    '6rpo': 4,
    '7rpo': 2,
    '10rpo': -2,
    '11rpo': -4,
    '12rpo': -6,
}

Fielding_points = {
    'Catch': 8,
    '3Cath': 4,
    'Stumping': 12,
    'RunOutD': 12,
    'RunOutInd': 6,
}

# ---------- Teams and default recent fantasy points ----------
# (These dicts may be updated externally or read from files. Values represent recent_performance baseline.)
# For simplicity we keep the user's provided rosters and default fp of 111.

srh = [
    'A Manohar', 'A Zampa', 'Abhishek Sharma', 'Aniket Verma', 'Atharva Taide', 'E Malinga',
    'H Klaasen', 'HV Patel', 'Harsh Dubey', 'Ishan Kishan', 'JD Unadkat', 'Mohammed Shami',
    'Nithish Kumar Reddy', 'PHKD Mendis', 'PJ Cummins', 'PWA Mulder', 'RD Chahar',
    'Simarjeet Singh', 'TM Head', 'Zeeshan Ansari'
]

srh_fp = {player: 111 for player in srh}

pbks = [
    'Arshdeep Singh', 'Azmatullah Omarzai', 'GJ Maxwell', 'Harpreet Brar', 'JP Inglis',
    'KA Jamieson', 'LH Ferguson', 'M Jansen', 'MJ Owen', 'MP Stoinis', 'Musheer Khan',
    'N Wadhera', 'P Dubey', 'P Simran Singh', 'Priyansh Arya', 'SS Iyer', 'Shashank Singh',
    'Suryansh Shedge', 'Vijaykumar Vyshak', 'XC Bartlett', 'YS Chahal', 'Yash Thakur'
]

pbks_fp = {player: 111 for player in pbks}

csk = [
    'A Kamboj', 'A Mhatre', 'D Brevis', 'DJ Hooda', 'DP Conway', 'J Overton', 'KK Ahmed',
    'M Pathirana', 'MS Dhoni', 'Mukesh Choudhary', 'NT Ellis', 'Noor Ahmad', 'R Ashwin',
    'R Ravindra', 'RA Jadeja', 'RA Tripathi', 'RD Gaikwad', 'S Dube', 'SK Rasheed',
    'SM Curran', 'Urvil Patel', 'V Shankar'
]

csk_fp = {player: 111 for player in csk}

# ... include all other teams

# For brevity we include the same teams defined by the user. Copying remaining lists:

dc = [
    'AR Patel', 'Abishek Porel', 'Ashutosh Sharma', 'D Ferreira', 'F du Plessis',
    'J Fraser-McGurk', 'KK Nair', 'KL Rahul', 'Kuldeep Yadav', 'M Tiwari', 'MA Starc',
    'MM Sharma', 'Mukesh Kumar', 'Mustafizur Rahman', 'PVD Chameera', 'Sameer Rizvi',
    'Sediqullah Atal', 'T Natarajan', 'T Stubbs', 'V Nigam'
]

dc_fp = {player: 111 for player in dc}

gt = [
    'Arshad Khan', 'B Sai Sudharsan', 'BKG Mendis', 'G Coetzee', 'I Sharma', 'JC Buttler',
    'K Khejroliya', 'K Rabada', 'Karim Janat', 'M Prasidh Krishna', 'M Shahrukh Khan',
    'Mohammed Siraj', 'R Sai Kishore', 'R Tewatia', 'Rashid Khan', 'SE Rutherford',
    'Shubman Gill', 'Washington Sundar'
]

gt_fp = {player: 111 for player in gt}

kkr = [
    'A Nortje', 'A Raghuvanshi', 'AD Russell', 'AM Rahane', 'AS Roy', 'C Sakariya',
    'CV Varun', 'Harshit Rana', 'MK Pandey', 'MM Ali', 'Q de Kock', 'R Powell', 'RK Singh',
    'Rahmanullah Gurbaz', 'Ramandeep Singh', 'SH Johnson', 'SP Narine', 'VG Arora', 'VR Iyer'
]

kkr_fp = {player: 111 for player in kkr}

lsg = [
    'A Badoni', 'AK Markram', 'Abdul Samad', 'Akash Deep', 'Akash Singh', 'Avesh Khan',
    'DA Miller', 'DS Rathi', 'M Siddharth', 'MP Breetzke', 'MP Yadav', 'MR Marsh',
    'N Pooran', 'Prince Yadav', 'RR Pant', 'Ravi Bishnoi', 'SN Thakur', 'Shahbaz Ahmed',
    "W O'Rourke"
]

lsg_fp = {player: 111 for player in lsg}

mi = [
    'C Bosch', 'DL Chahar', 'HH Pandya', 'JJ Bumrah', 'JM Bairstow', 'KV Sharma', 'MJ Santner',
    'Mujeeb Ur Rahman', 'Naman Dhir', 'PVSN Raju', 'R Minz', 'RA Bawa', 'RD Rickelton',
    'RG Sharma', 'RJ Gleeson', 'RJW Topley', 'SA Yadav', 'TA Boult', 'Tilak Varma',
    'V Puthur', 'WG Jacks'
]

mi_fp = {player: 111 for player in mi}

rr = [
    'Dhruv Jurel', 'Fazalhaq Farooqi', 'JC Archer', 'K Kartikeya', 'KS Rathore', 'KT Maphaka',
    'M Theekshana', 'N Rana', 'PWH de Silva', 'R Parag', 'SB Dubey', 'SO Hetmyer',
    'SV Samson', 'Sandeep Sharma', 'TU Deshpande', 'V Suryavanshi', 'YBK Jaiswal',
    'Yudhvir Singh'
]

rr_fp = {player: 111 for player in rr}

rcb = [
    'B Kumar', 'D Padikkal', 'JG Bethell', 'JM Sharma', 'JR Hazlewood', 'KH Pandya', 'L Ngidi',
    'LS Livingstone', 'MA Agarwal', 'MS Bhandage', 'N Thushara', 'PD Salt', 'R Shepherd', 'RM Patidar',
    'Rasikh Salam', 'Suyash Sharma', 'TH David', 'V Kohli', 'Yash Dayal'
]

rcb_fp = {player: 111 for player in rcb}

# ---------- Core function: compute fantasy points using last 5 years data ----------

def get_players(team1, team2, team1_fp, byb_df=None):
    """Return list of (fantasy_points, player_name) computed using only last-5-years ball-by-ball data.
    byb_df can be passed to override the default filtered dataset.
    """
    if byb_df is None:
        byb_df = byb_last5

    fantasy_team_players = []

    for i in range(len(team1)):
        player_name = team1[i]

        # Matches played in last-5-years for this batsman
        try:
            unq_ids = byb_df[byb_df['batsman'] == player_name]['id'].unique()
        except Exception:
            # column names may differ in some datasets, try lowercase names
            byb_cols = [c.lower() for c in byb_df.columns]
            if 'batsman' in byb_cols and 'id' in byb_cols:
                unq_ids = byb_df[byb_df.columns[byb_cols.index('batsman')]]['id'].unique()
            else:
                unq_ids = []

        matches_played = len(unq_ids)

        # Batsman runs by match
        bbr = []
        for x in unq_ids:
            bat_run = sum(byb_df[(byb_df['batsman'] == player_name) & (byb_df['id'] == x)]['batsman_runs'])
            bbr.append(bat_run)

        r30, r50, r100 = 0, 0, 0
        for m in bbr:
            if m >= 100:
                r100 += 1
            elif m >= 50:
                r50 += 1
            elif m >= 30:
                r30 += 1

        try:
            catches = len(byb_df[(byb_df['fielder'] == player_name) & (byb_df['dismissal_kind'] == 'caught')]) / max(matches_played, 1)
            run_outs = len(byb_df[(byb_df['fielder'] == player_name) & (byb_df['dismissal_kind'] == 'run out')]) / max(matches_played, 1)
            extra_points = (
                (r30 / max(matches_played, 1)) * Batsman_points['30Runs']
                + (r50 / max(matches_played, 1)) * Batsman_points['Half_century']
                + (r100 / max(matches_played, 1)) * Batsman_points['Century']
                + catches * Fielding_points['Catch']
                + run_outs * Fielding_points['RunOutInd']
            )
        except Exception:
            catches, run_outs, extra_points = 0, 0, 0

        # Bowling extras estimated from last-5-years
        wickets_taken = []
        for x in unq_ids:
            twx = sum(byb_df[(byb_df['bowler'] == player_name) & (byb_df['id'] == x)]['is_wicket'])
            wickets_taken.append(twx)

        w3, w4, w5 = 0, 0, 0
        for z in wickets_taken:
            if z >= 5:
                w5 += 1
            elif z >= 4:
                w4 += 1
            elif z >= 3:
                w3 += 1

        try:
            lbws = len(byb_df[(byb_df['bowler'] == player_name) & (byb_df['dismissal_kind'] == 'lbw')]) / max(matches_played, 1)
            bowled = len(byb_df[(byb_df['bowler'] == player_name) & (byb_df['dismissal_kind'] == 'bowled')]) / max(matches_played, 1)
            wexp = (
                (w3 / max(matches_played, 1)) * Bowling_points['3W']
                + (w4 / max(matches_played, 1)) * Bowling_points['4W']
                + (w5 / max(matches_played, 1)) * Bowling_points['5W']
                + lbws * Bowling_points['LBW_Bowled']
                + bowled * Bowling_points['LBW_Bowled']
            )
        except Exception:
            lbws, bowled, wexp = 0, 0, 0

        # per-opponent fantasy points using last-5-years
        ffp = []
        for j in range(len(team2)):
            opp = team2[j]
            bat_vs_bowl = byb_df[(byb_df['batsman'] == player_name) & (byb_df['bowler'] == opp)]
            bowls_played = len(bat_vs_bowl['batsman_runs']) if 'batsman_runs' in bat_vs_bowl.columns else 0
            runs_scored = bat_vs_bowl['batsman_runs'].sum() if 'batsman_runs' in bat_vs_bowl.columns else 0
            fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs'] == 4]) if 'batsman_runs' in bat_vs_bowl.columns else 0
            sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs'] == 6]) if 'batsman_runs' in bat_vs_bowl.columns else 0
            wicket = bat_vs_bowl['is_wicket'].sum() if 'is_wicket' in bat_vs_bowl.columns else 0

            if bowls_played <= 6 * 10 and wicket >= 5:
                penalty = -16
            elif bowls_played <= 6 * 8 and wicket >= 4:
                penalty = -8
            elif bowls_played <= 6 * 6 and wicket >= 3:
                penalty = -4
            else:
                penalty = 0

            try:
                strike_rate = int(runs_scored / bowls_played * 100) if bowls_played > 0 else 'NA'
            except Exception:
                strike_rate = 'NA'

            # opponent-to-player wicket interactions
            bowl_vs_bat = byb_df[(byb_df['bowler'] == player_name) & (byb_df['batsman'] == opp)]
            wicket_took = bowl_vs_bat['is_wicket'].sum() if 'is_wicket' in bowl_vs_bat.columns else 0

            fantasy_points1 = (
                runs_scored
                + fours * Batsman_points['bFour']
                + sixes * Batsman_points['bSix']
                - wicket * Bowling_points['Wicket']
                + wicket_took * Bowling_points['Wicket']
                + penalty
            )
            ffp.append(fantasy_points1)

        sum_ffp = sum(ffp)

        # recent performance baseline from team1_fp (these are external baseline values provided by the UI or team dict)
        if team1_fp.get(player_name, 0) > 0:
            recent_performace_points = np.log(team1_fp[player_name])
        elif team1_fp.get(player_name, 0) < 0:
            recent_performace_points = -np.log(abs(team1_fp[player_name]))
        else:
            recent_performace_points = 0

        # User's code used a more stable approach: divide baseline by 3
        recent_performace_points = team1_fp.get(player_name, 0) / 3

        # Combine weighted values
        weight1 = 0.5
        weight2 = 1 - weight1
        final_fantasy_point = (sum_ffp + extra_points + wexp) * weight1 + recent_performace_points * weight2
        final_fantasy_point = round(final_fantasy_point, 2)

        fantasy_team_players.append((final_fantasy_point, player_name))

    # Sort by fantasy points descending
    fantasy_team_players.sort(reverse=True)
    return fantasy_team_players


# ---------- Flask routes ----------
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/process_login', methods=['POST'])
def process_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # simple demo credentials
    if email == 'user@example.com' and password == 'password':
        return redirect(url_for('select_team'))
    return render_template('login.html', login_error=True)


@app.route('/index', methods=['GET', 'POST'])
def select_team():
    global Team_1, Team_2, Team1_Squad, Team2_Squad, user_choice1, user_choice2

    if request.method == 'POST':
        user_choice1 = request.form.get('team1')
        user_choice2 = request.form.get('team2')

        if not user_choice1 or not user_choice2:
            error_message = 'Please select both teams.'
            return render_template('index.html', error_message=error_message)

        # read team rosters from Teams folder
        p1 = os.path.join(DATA_DIR, f'Teams\\{user_choice1}.xlsx')
        p2 = os.path.join(DATA_DIR, f'Teams\\{user_choice2}.xlsx')

        try:
            p1_df = pd.read_excel(p1)
            players1 = p1_df['player_name'].tolist()
        except Exception as e:
            players1 = []
            print(f"Could not read {p1}: {e}")

        try:
            p2_df = pd.read_excel(p2)
            players2 = p2_df['player_name'].tolist()
        except Exception as e:
            players2 = []
            print(f"Could not read {p2}: {e}")

        # pick Team1_Squad and Team2_Squad based on selection
        team_map = {
            'SRH': srh_fp, 'PBKS': pbks_fp, 'CSK': csk_fp, 'KKR': kkr_fp,
            'DC': dc_fp, 'RCB': rcb_fp, 'MI': mi_fp, 'RR': rr_fp,
            'GT': gt_fp, 'LSG': lsg_fp
        }

        Team1_Squad = team_map.get(user_choice1, {})
        Team2_Squad = team_map.get(user_choice2, {})

        selected_players1 = request.form.getlist('player1')
        selected_players2 = request.form.getlist('player2')

        if len(selected_players1) == 11 and len(selected_players2) == 11:
            Team_1 = selected_players1
            Team_2 = selected_players2
        else:
            error_message = 'Please select exactly 11 players for both teams.'
            return render_template('player.html', players1=players1, players2=players2, error_message=error_message)

        # compute fantasy using only last-5-years data
        t1 = get_players(Team_1, Team_2, Team1_Squad, byb_df=byb_last5)
        t2 = get_players(Team_2, Team_1, Team2_Squad, byb_df=byb_last5)

        # merge and pick top 11 overall (or show full squads with fantasy points)
        merged = t1 + t2
        merged.sort(reverse=True)

        # Build a friendly display: "Player Name (predicted_points)"
        display_list = [f"{name} ({points})" if isinstance(points, (int, float)) else f"{name} ({points})" for points, name in merged]

        # Make a DataFrame for top 11
        top11 = display_list[:11]
        Result = pd.DataFrame({'predicted_player': top11})
        predicted_team_html = Result.to_html(index=False, header=True, classes='table table-striped')

        return render_template('result.html', predicted_team=predicted_team_html)

    # GET: render selection page
    # try to load default teams list from Teams folder to render dropdowns
    teams_files = []
    teams_dir = os.path.join(DATA_DIR, 'Teams')
    if os.path.exists(teams_dir):
        for f in os.listdir(teams_dir):
            if f.lower().endswith('.xlsx'):
                teams_files.append(os.path.splitext(f)[0])

    return render_template('result.html', available_teams=teams_files)



if __name__ == '__main__':
    # Run app on host 0.0.0.0 if desired, else default
    app.run(debug=True)
