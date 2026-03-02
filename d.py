from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

# Global variables
Team_1 = []
Team_2 = []
Team1_Squad = {}
Team2_Squad = {}
user_choice1 = ''
user_choice2 = ''

# Fantasy Points
Batsman_points = {'Run':1, 'bFour':1, 'bSix':2, '30Runs':4,
        'Half_century':8, 'Century':16, 'Duck':-2, '170sr':6,
        '150sr':4, '130sr':2, '70sr':-2, '60sr':-4, '50sr':-6}

Bowling_points = {'Wicket':25, 'LBW_Bowled':8, '3W':4, '4W':8, 
                  '5W':16, 'Maiden':12, '5rpo':6, '6rpo':4, '7rpo':2, '10rpo':-2,
                  '11rpo':-4, '12rpo':-6}

Fielding_points = {'Catch':8, '3Cath':4, 'Stumping':12, 'RunOutD':12,
                  'RunOutInd':6}

# Teams and fantasy points
srh_fp = {player: 111 for player in ['A Manohar', 'A Zampa', 'Abhishek Sharma', 'Aniket Verma', 'Atharva Taide', 'E Malinga',
                                     'H Klaasen', 'HV Patel', 'Harsh Dubey', 'Ishan Kishan', 'JD Unadkat', 'Mohammed Shami',
                                     'Nithish Kumar Reddy', 'PHKD Mendis', 'PJ Cummins', 'PWA Mulder', 'RD Chahar',
                                     'Simarjeet Singh', 'TM Head', 'Zeeshan Ansari']}

pbks_fp = {player: 111 for player in ['Arshdeep Singh', 'Azmatullah Omarzai', 'GJ Maxwell', 'Harpreet Brar', 'JP Inglis',
                                     'KA Jamieson', 'LH Ferguson', 'M Jansen', 'MJ Owen', 'MP Stoinis', 'Musheer Khan',
                                     'N Wadhera', 'P Dubey', 'P Simran Singh', 'Priyansh Arya', 'SS Iyer', 'Shashank Singh',
                                     'Suryansh Shedge', 'Vijaykumar Vyshak', 'XC Bartlett', 'YS Chahal', 'Yash Thakur']}

csk_fp = {player: 111 for player in ['A Kamboj', 'A Mhatre', 'D Brevis', 'DJ Hooda', 'DP Conway', 'J Overton', 'KK Ahmed',
                                     'M Pathirana', 'MS Dhoni', 'Mukesh Choudhary', 'NT Ellis', 'Noor Ahmad', 'R Ashwin',
                                     'R Ravindra', 'RA Jadeja', 'RA Tripathi', 'RD Gaikwad', 'S Dube', 'SK Rasheed',
                                     'SM Curran', 'Urvil Patel', 'V Shankar']}

dc_fp = {player: 111 for player in ['AR Patel', 'Abishek Porel', 'Ashutosh Sharma', 'D Ferreira', 'F du Plessis',
                                   'J Fraser-McGurk', 'KK Nair', 'KL Rahul', 'Kuldeep Yadav', 'M Tiwari', 'MA Starc',
                                   'MM Sharma', 'Mukesh Kumar', 'Mustafizur Rahman', 'PVD Chameera', 'Sameer Rizvi',
                                   'Sediqullah Atal', 'T Natarajan', 'T Stubbs', 'V Nigam']}

gt_fp = {player: 111 for player in ['Arshad Khan', 'B Sai Sudharsan', 'BKG Mendis', 'G Coetzee', 'I Sharma', 'JC Buttler',
                                   'K Khejroliya', 'K Rabada', 'Karim Janat', 'M Prasidh Krishna', 'M Shahrukh Khan',
                                   'Mohammed Siraj', 'R Sai Kishore', 'R Tewatia', 'Rashid Khan', 'SE Rutherford',
                                   'Shubman Gill', 'Washington Sundar']}

kkr_fp = {player: 111 for player in ['A Nortje', 'A Raghuvanshi', 'AD Russell', 'AM Rahane', 'AS Roy', 'C Sakariya',
                                    'CV Varun', 'Harshit Rana', 'MK Pandey', 'MM Ali', 'Q de Kock', 'R Powell', 'RK Singh',
                                    'Rahmanullah Gurbaz', 'Ramandeep Singh', 'SH Johnson', 'SP Narine', 'VG Arora', 'VR Iyer']}

lsg_fp = {player: 111 for player in ['A Badoni', 'AK Markram', 'Abdul Samad', 'Akash Deep', 'Akash Singh', 'Avesh Khan',
                                    'DA Miller', 'DS Rathi', 'M Siddharth', 'MP Breetzke', 'MP Yadav', 'MR Marsh',
                                    'N Pooran', 'Prince Yadav', 'RR Pant', 'Ravi Bishnoi', 'SN Thakur', 'Shahbaz Ahmed',
                                    "W O'Rourke"]}

mi_fp = {player: 111 for player in ['C Bosch', 'DL Chahar', 'HH Pandya', 'JJ Bumrah', 'JM Bairstow', 'KV Sharma', 'MJ Santner',
                                   'Mujeeb Ur Rahman', 'Naman Dhir', 'PVSN Raju', 'R Minz', 'RA Bawa', 'RD Rickelton',
                                   'RG Sharma', 'RJ Gleeson', 'RJW Topley', 'SA Yadav', 'TA Boult', 'Tilak Varma',
                                   'V Puthur', 'WG Jacks']}

rr_fp = {player: 111 for player in ['Dhruv Jurel', 'Fazalhaq Farooqi', 'JC Archer', 'K Kartikeya', 'KS Rathore', 'KT Maphaka',
                                   'M Theekshana', 'N Rana', 'PWH de Silva', 'R Parag', 'SB Dubey', 'SO Hetmyer',
                                   'SV Samson', 'Sandeep Sharma', 'TU Deshpande', 'V Suryavanshi', 'YBK Jaiswal',
                                   'Yudhvir Singh']}

rcb_fp = {player: 111 for player in ['B Kumar','D Padikkal','JG Bethell','JM Sharma','JR Hazlewood','KH Pandya','L Ngidi',
                                   'LS Livingstone','MA Agarwal','MS Bhandage','N Thushara','PD Salt','R Shepherd','RM Patidar',
                                   'Rasikh Salam','Suyash Sharma','TH David','V Kohli','Yash Dayal']}

# Load ball-by-ball data
byb = pd.read_csv('IPl Ball-by-Ball 2008-2023.csv')

# --------------------- FUNCTIONS ---------------------

def get_players(team1, team2, team1_fp):
    fantasy_team_players = []

    for player in team1:
        unq_ids = byb[byb["batsman"]==player]['id'].unique()
        matches_played = len(unq_ids)
        bbr = [sum(byb[(byb["batsman"]==player) & (byb['id']==x)]['batsman_runs']) for x in unq_ids]

        # Batting extra points
        r30 = sum(1 for m in bbr if m>=30 and m<50)
        r50 = sum(1 for m in bbr if m>=50 and m<100)
        r100 = sum(1 for m in bbr if m>=100)
        try:
            catches = len(byb[(byb['fielder']==player) & (byb['dismissal_kind']=='caught')])/matches_played
            run_outs = len(byb[(byb['fielder']==player) & (byb['dismissal_kind']=='run out')])/matches_played
            extra_points = r30/matches_played*Batsman_points['30Runs'] + r50/matches_played*Batsman_points['Half_century'] + \
                           r100/matches_played*Batsman_points['Century'] + catches*Fielding_points['Catch'] + \
                           run_outs*Fielding_points['RunOutInd']
        except:
            extra_points = 0

        # Bowling extra points
        wickets_taken = [sum(byb[(byb["bowler"]==player) & (byb['id']==x)]['is_wicket']) for x in unq_ids]
        w3 = sum(1 for w in wickets_taken if w==3)
        w4 = sum(1 for w in wickets_taken if w==4)
        w5 = sum(1 for w in wickets_taken if w>=5)
        try:
            lbws = len(byb[(byb['bowler']==player) & (byb['dismissal_kind']=='lbw')])/matches_played
            bowled = len(byb[(byb['bowler']==player) & (byb['dismissal_kind']=='bowled')])/matches_played
            wexp = w3/matches_played*Bowling_points['3W'] + w4/matches_played*Bowling_points['4W'] + \
                   w5/matches_played*Bowling_points['5W'] + lbws*Bowling_points['LBW_Bowled'] + bowled*Bowling_points['LBW_Bowled']
        except:
            wexp = 0

        ffp = []
        for opponent in team2:
            bat_vs_bowl = byb[(byb["batsman"]==player) & (byb["bowler"]==opponent)]
            runs_scored = sum(bat_vs_bowl.batsman_runs)
            fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
            sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
            wicket = sum(bat_vs_bowl.is_wicket)
            penalty = 0
            if len(bat_vs_bowl) <= 60 and wicket>=5:
                penalty = -16
            elif len(bat_vs_bowl) <= 48 and wicket>=4:
                penalty = -8
            elif len(bat_vs_bowl) <=36 and wicket>=3:
                penalty = -4
            ffp.append(runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + penalty)
        sum_ffp = sum(ffp)
        recent_points = team1_fp.get(player,0)/3
        final_points = round((sum_ffp + extra_points + wexp)*0.5 + recent_points*0.5,2)
        fantasy_team_players.append((final_points, player))

    fantasy_team_players.sort(reverse=True)
    return fantasy_team_players

# --------------------- ROUTES ---------------------

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
    if email=="user@example.com" and password=="password":
        return redirect(url_for('index'))
    return render_template('login.html', login_error=True)

@app.route('/index', methods=['GET','POST'])
def select_team():
    global Team_1, Team_2, Team1_Squad, Team2_Squad, user_choice1, user_choice2
    if request.method=='POST':
        user_choice1 = request.form.get('team1')
        user_choice2 = request.form.get('team2')
        p1_df = pd.read_excel(f'Teams\\{user_choice1}.xlsx')
        p2_df = pd.read_excel(f'Teams\\{user_choice2}.xlsx')
        players1 = p1_df['player_name'].tolist()
        players2 = p2_df['player_name'].tolist()

        team_dict = {'SRH':srh_fp,'PBKS':pbks_fp,'CSK':csk_fp,'KKR':kkr_fp,'DC':dc_fp,'RCB':rcb_fp,'MI':mi_fp,'RR':rr_fp,'GT':gt_fp,'LSG':lsg_fp}
        Team1_Squad = team_dict.get(user_choice1,{})
        Team2_Squad = team_dict.get(user_choice2,{})

        selected_players1 = request.form.getlist('player1')
        selected_players2 = request.form.getlist('player2')
        if len(selected_players1)!=11 or len(selected_players2)!=11:
            error_message = 'Please select exactly 11 players for both teams.'
            return render_template('player.html', players1=players1, players2=players2, error_message=error_message)
        Team_1 = selected_players1
        Team_2 = selected_players2

        t1 = get_players(Team_1, Team_2, Team1_Squad)
        t2 = get_players(Team_2, Team_1, Team2_Squad)
        t3 = t1 + t2
        t3.sort(reverse=True)

        # Prepare top 11 DataFrame
        Team_df = pd.DataFrame(t3, columns=['FantasyPoints','Player']).head(11)
        captain = Team_df.iloc[0]['Player']
        vice_captain = Team_df.iloc[1]['Player']
        all_points = [fp for fp, player in t3]
        Team_df['MinPoints'] = min(all_points)
        Team_df['MaxPoints'] = max(all_points)
        Team_df['Role'] = ['Captain' if p==captain else 'Vice-Captain' if p==vice_captain else '' for p in Team_df['Player']]
        predicted_team = Team_df.to_html(index=False, classes='table table-striped table-bordered')

        return render_template('result.html', predicted_team=predicted_team)

    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
