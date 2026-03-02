from flask import Flask, request, render_template,redirect,url_for
import matplotlib.pyplot as plt
#import seborn as sns
import pandas as pd
import numpy as np

app = Flask(__name__)

Team_1=  []
Team_2 = []
Team1_Squad = {}
Team2_Squad = {}

# Importing basic libraries
# Reading files
byb=pd.read_csv('IPl Ball-by-Ball 2008-2023.csv')
match= pd.read_csv('IPL Mathces 2008-2023.csv')
byb.head()

# Fantasy Points

Batsman_points = {'Run':1, 'bFour':1, 'bSix':2, '30Runs':4,
        'Half_century':8, 'Century':16, 'Duck':-2, '170sr':6,
                 '150sr':4, '130sr':2, '70sr':-2, '60sr':-4, '50sr':-6}

Bowling_points = {'Wicket':25, 'LBW_Bowled':8, '3W':4, '4W':8, 
                  '5W':16, 'Maiden':12, '5rpo':6, '6rpo':4, '7rpo':2, '10rpo':-2,
                 '11rpo':-4, '12rpo':-6}

Fielding_points = {'Catch':8, '3Cath':4, 'Stumping':12, 'RunOutD':12,
                  'RunOutInd':6}

# Storing team players
# Here I have to do manual work... choosing the players after the toss and putting them here
# TEAM 1: SRH
srh = [
    'A Manohar', 'A Zampa', 'Abhishek Sharma', 'Aniket Verma', 'Atharva Taide', 'E Malinga',
    'H Klaasen', 'HV Patel', 'Harsh Dubey', 'Ishan Kishan', 'JD Unadkat', 'Mohammed Shami',
    'Nithish Kumar Reddy', 'PHKD Mendis', 'PJ Cummins', 'PWA Mulder', 'RD Chahar',
    'Simarjeet Singh', 'TM Head', 'Zeeshan Ansari'
]

srh_fp = {player: 111 for player in srh}

# TEAM 2: PBKS
pbks = [
    'Arshdeep Singh', 'Azmatullah Omarzai', 'GJ Maxwell', 'Harpreet Brar', 'JP Inglis',
    'KA Jamieson', 'LH Ferguson', 'M Jansen', 'MJ Owen', 'MP Stoinis', 'Musheer Khan',
    'N Wadhera', 'P Dubey', 'P Simran Singh', 'Priyansh Arya', 'SS Iyer', 'Shashank Singh',
    'Suryansh Shedge', 'Vijaykumar Vyshak', 'XC Bartlett', 'YS Chahal', 'Yash Thakur'
]

pbks_fp = {player: 111 for player in pbks}

# TEAM 3: CSK
csk = [
    'A Kamboj', 'A Mhatre', 'D Brevis', 'DJ Hooda', 'DP Conway', 'J Overton', 'KK Ahmed',
    'M Pathirana', 'MS Dhoni', 'Mukesh Choudhary', 'NT Ellis', 'Noor Ahmad', 'R Ashwin',
    'R Ravindra', 'RA Jadeja', 'RA Tripathi', 'RD Gaikwad', 'S Dube', 'SK Rasheed',
    'SM Curran', 'Urvil Patel', 'V Shankar'
]

csk_fp = {player: 111 for player in csk}

# TEAM 4: DC
dc = [
    'AR Patel', 'Abishek Porel', 'Ashutosh Sharma', 'D Ferreira', 'F du Plessis',
    'J Fraser-McGurk', 'KK Nair', 'KL Rahul', 'Kuldeep Yadav', 'M Tiwari', 'MA Starc',
    'MM Sharma', 'Mukesh Kumar', 'Mustafizur Rahman', 'PVD Chameera', 'Sameer Rizvi',
    'Sediqullah Atal', 'T Natarajan', 'T Stubbs', 'V Nigam'
]

dc_fp = {player: 111 for player in dc}

# TEAM 5: GT
gt = [
    'Arshad Khan', 'B Sai Sudharsan', 'BKG Mendis', 'G Coetzee', 'I Sharma', 'JC Buttler',
    'K Khejroliya', 'K Rabada', 'Karim Janat', 'M Prasidh Krishna', 'M Shahrukh Khan',
    'Mohammed Siraj', 'R Sai Kishore', 'R Tewatia', 'Rashid Khan', 'SE Rutherford',
    'Shubman Gill', 'Washington Sundar'
]

gt_fp = {player: 111 for player in gt}

# TEAM 6: KKR
kkr = [
    'A Nortje', 'A Raghuvanshi', 'AD Russell', 'AM Rahane', 'AS Roy', 'C Sakariya',
    'CV Varun', 'Harshit Rana', 'MK Pandey', 'MM Ali', 'Q de Kock', 'R Powell', 'RK Singh',
    'Rahmanullah Gurbaz', 'Ramandeep Singh', 'SH Johnson', 'SP Narine', 'VG Arora', 'VR Iyer'
]

kkr_fp = {player: 111 for player in kkr}

# TEAM 7: LSG
lsg = [
    'A Badoni', 'AK Markram', 'Abdul Samad', 'Akash Deep', 'Akash Singh', 'Avesh Khan',
    'DA Miller', 'DS Rathi', 'M Siddharth', 'MP Breetzke', 'MP Yadav', 'MR Marsh',
    'N Pooran', 'Prince Yadav', 'RR Pant', 'Ravi Bishnoi', 'SN Thakur', 'Shahbaz Ahmed',
    'W O\'Rourke'
]

lsg_fp = {player: 111 for player in lsg}

# TEAM 8: Ashwani Kumar (MI)
mi = [
    'C Bosch', 'DL Chahar', 'HH Pandya', 'JJ Bumrah', 'JM Bairstow', 'KV Sharma', 'MJ Santner',
    'Mujeeb Ur Rahman', 'Naman Dhir', 'PVSN Raju', 'R Minz', 'RA Bawa', 'RD Rickelton',
    'RG Sharma', 'RJ Gleeson', 'RJW Topley', 'SA Yadav', 'TA Boult', 'Tilak Varma',
    'V Puthur', 'WG Jacks'
]

mi_fp = {player: 111 for player in mi}

# TEAM 9: Akash Madhwal
rr = [
    'Dhruv Jurel', 'Fazalhaq Farooqi', 'JC Archer', 'K Kartikeya', 'KS Rathore', 'KT Maphaka',
    'M Theekshana', 'N Rana', 'PWH de Silva', 'R Parag', 'SB Dubey', 'SO Hetmyer',
    'SV Samson', 'Sandeep Sharma', 'TU Deshpande', 'V Suryavanshi', 'YBK Jaiswal',
    'Yudhvir Singh'
]

rr_fp = {player: 111 for player in rr}

# TEAM 10: RCB
rcb = [
    'B Kumar','D Padikkal','JG Bethell','JM Sharma','JR Hazlewood','KH Pandya','L Ngidi',
    'LS Livingstone','MA Agarwal','MS Bhandage','N Thushara','PD Salt','R Shepherd','RM Patidar',
    'Rasikh Salam','Suyash Sharma','TH David','V Kohli','Yash Dayal'
]

rcb_fp = {player: 111 for player in rcb}


'''
team1 = lsg; team2 = gt              #team1 v Team2

for i in range(len(team1)):
    ffp = []
    for j in range(len(team2)):
        bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
        bowls_played = len(bat_vs_bowl.batsman_runs)
        runs_scored = sum(bat_vs_bowl.batsman_runs)
        fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
        sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
        wicket = sum(bat_vs_bowl.is_wicket)
        if bowls_played <=6*10 and wicket >=5:
            penalty = -16
            k =  print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*8 and wicket >=4:
            penalty = -8
            l = print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*6 and wicket >=3:
            penalty = -4
            p =print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        else:
            penalty = 0
        try:    
            strike_rate = int(runs_scored/bowls_played*100)
        except: 
            strike_rate = 'NA'

        if bowls_played >=8 and strike_rate!='NA':
            if strike_rate >=170:
               n =  print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
            elif strike_rate >=150:
               m =  print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                        
        bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
        wicket_took = sum(bowl_vs_bat.is_wicket)
        fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty
        pd.DataFrame(ffp.append(fantasy_points1))
        #print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
        #     "bowls",bowls_played,"strike rate", strike_rate,
         #      'Out',wicket,'times', "Fours", fours,"Sixes", sixes)

team1 = gt; team2 = lsg                     #Team2 v Team1

for i in range(len(team1)):
    ffp=[]
    for j in range(len(team2)):
        bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
        bowls_played = len(bat_vs_bowl.batsman_runs)
        runs_scored = sum(bat_vs_bowl.batsman_runs)
        fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
        sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
        wicket = sum(bat_vs_bowl.is_wicket)
        if bowls_played <=6*10 and wicket >=5:
            penalty = -16
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*8 and wicket >=4:
            penalty = -8
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*6 and wicket >=3:
            penalty = -4
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        else:
            penalty = 0
        try:    
            strike_rate = int(runs_scored/bowls_played*100)
        except: 
            strike_rate = 'NA'

        if bowls_played >=8 and strike_rate!='NA':
            if strike_rate >=170:
                print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
            elif strike_rate >=150:
                print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                        
        bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
        wicket_took = sum(bowl_vs_bat.is_wicket)
        fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty
        ffp.append(fantasy_points1)
        #print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
             #   "bowls",bowls_played,"strike rate", strike_rate,
              # 'Out',wicket,'times', "Fours", fours,"Sixes", sixes, 'fantasy_points', fantasy_points1)

'''

def get_players(team1,team2,team1_fp):
    fantasy_team_players = []

    for i in range(len(team1)):
        unq_ids = byb[byb["batsman"]==team1[i]]['id'].unique()
        mathces_played = len(unq_ids)
#         print ( "Number of matches played" , len(unq_ids),team1[i])
        bbr = []
        for x in unq_ids:
            bat_run = sum(byb[(byb["batsman"]==team1[i])&(byb['id']==x)]['batsman_runs'])
            bbr.append(bat_run)

        r30,r50,r100 =0,0,0
        for m in bbr:
            if m>=100:
                r100+=1
            elif m>=50:
                r50+=1
            elif m>=30:
                r30+=1
        try:
            catches = len(byb[(byb['fielder']==team1[i]) & (byb['dismissal_kind']=='caught')])/mathces_played
            run_outs = len(byb[(byb['fielder']==team1[i]) & (byb['dismissal_kind']=='run out')])/mathces_played
            extra_points = r30/mathces_played*Batsman_points['30Runs'] +r50/mathces_played*Batsman_points['Half_century'] +r100/mathces_played*Batsman_points['Century'] +catches*Fielding_points['Catch']+run_outs*Fielding_points['RunOutInd']
        except:
            catches, run_outs, extra_points = 0,0,0
        
        # Extra Points for bowlers to be estimated here
        wickets_taken = []
        for x in unq_ids:
            twx = sum(byb[(byb["bowler"]==team1[i]) & (byb['id']==x)]['is_wicket'])
            wickets_taken.append(twx)

        w3,w4,w5 = 0,0,0
        for z in wickets_taken:
            if z>=5:
                w5+=1
            elif z>=4:
                w4+=1
            elif z>=3:
                w3+=1
        try:
            lbws = len((byb[(byb['bowler']==team1[i]) & (byb['dismissal_kind']=='lbw')]))/mathces_played      
            bowled = len((byb[(byb['bowler']==team1[i]) & (byb['dismissal_kind']=='bowled')]))/mathces_played      
            wexp = w3/mathces_played*Bowling_points['3W'] + w4/mathces_played*Bowling_points['4W'] + w5/mathces_played*Bowling_points['5W'] + lbws*Bowling_points['LBW_Bowled'] + bowled*Bowling_points['LBW_Bowled']
        except:
            lbws, bowled, wexp = 0,0,0
        
        ffp = []
        for j in range(len(team2)):
            bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
            bowls_played = len(bat_vs_bowl.batsman_runs)
            runs_scored = sum(bat_vs_bowl.batsman_runs)
            fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
            sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
            wicket = sum(bat_vs_bowl.is_wicket)
            if bowls_played <=6*10 and wicket >=5:
                penalty = -16
                print (team1[i], "ka wicket taken",wicket,"times by", team2[j])
            elif bowls_played <=6*8 and wicket >=4:
                penalty = -8
                print (team1[i], "ka wicket taken",wicket,"times by", team2[j])
            elif bowls_played <=6*6 and wicket >=3:
                penalty = -4
                print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
            else:
                penalty = 0

            try:    
                strike_rate = int(runs_scored/bowls_played*100)
            except: 
                strike_rate = 'NA'            
            if bowls_played >=10 and strike_rate!='NA':
                if strike_rate >=170:
                    print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                elif strike_rate >=150:
                    print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
   
            bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
            wicket_took = sum(bowl_vs_bat.is_wicket)
            fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty 
            ffp.append(fantasy_points1)
            print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
                     "bowls",bowls_played,"strike rate", strike_rate,
                     'Out',wicket,'times', "Fours", fours,"Sixes", sixes, "fatansy points",fantasy_points1)
        sum_ffp = sum(ffp)
        if team1_fp[team1[i]] > 0:
            recent_performace_points = np.log(team1_fp[team1[i]])
        elif team1_fp[team1[i]] <0:
            recent_performace_points = -np.log(abs(team1_fp[team1[i]]))
        else:
            recent_performace_points = 0
        # Trying a new method for recent performancec point
        recent_performace_points = team1_fp[team1[i]]/3
        weight1 = 0.5
        weight2 = 1 - weight1
        final_fantasy_point = (sum_ffp + extra_points + wexp)*weight1 + recent_performace_points*weight2
        final_fantasy_point = round(final_fantasy_point,2)
        fantasy_team_players.append((final_fantasy_point,team1[i]))
        fantasy_team_players.sort(reverse=True)
#         print ("Fatasy points of",team1[i],final_fantasy_point)
    return fantasy_team_players

'''
def selection1():
    players_df = pd.read_excel('{Team_1}.xlsx')
    players = players_df['player_name'].tolist()
    selected_players = request.form.getlist('player')
    # Ensure exactly 11 players are selected
    if len(selected_players) == 11:
        # Store selected players in the Team list
        Team_1 = selected_players

def selection2(Team_2):
    players_df = pd.read_excel('{Team_2}.xlsx')
    players = players_df['player_name'].tolist()
'''

@app.route('/')
def home():
    # Render the 'login.html' template
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    # Process the login form data (replace this with your actual login logic)
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform login validation here (replace this with your actual validation logic)

    # For demonstration purposes, let's assume successful login
    if email == "user@example.com" and password == "password":
        # Redirect to the '/index' route upon successful login
        return redirect(url_for('index'))

    # If login fails, you can render the login template again with an error message
    return render_template('login.html', login_error=True)

@app.route('/index', methods=['GET', 'POST'])

def select_team():
    
    global Team_1, Team_2, Team1_Squad, Team2_Squad,user_choice1,user_choice2
    if request.method == 'POST':
        if 'team1' in request.form:
            user_choice1 = request.form['team1']
    # rest of your code
        else:
    # handle the case where 'team1' is not present in the form
            error_message = 'Please select a team for Team 1.'
            print(error_message)
    
        if 'team2' in request.form:
            user_choice2 = request.form['team2']
    # rest of your code
        else:
    # handle the case where 'team1' is not present in the form
            error_message = 'Please select a team for Team 2.'
            print(error_message)

        p1 = f'Teams\{user_choice1}.xlsx'
        p1_df = pd.read_excel(p1)
        players1 = p1_df['player_name'].tolist()

        p2 = f'Teams\{user_choice2}.xlsx'
        p2_df = pd.read_excel(p2)
        players2 = p2_df['player_name'].tolist()

        if user_choice1 == 'SRH':
            Team1_Squad = srh_fp
        elif user_choice1 == 'PBKS':
            Team1_Squad = pbks_fp
        elif user_choice1 == 'CSK':
            Team1_Squad = csk_fp
        elif user_choice1 == 'KKR':
            Team1_Squad = kkr_fp
        elif user_choice1 == 'DC':
            Team1_Squad = dc_fp
        elif user_choice1 == 'RCB':
            Team1_Squad = rcb_fp
        elif user_choice1 == 'MI':
            Team1_Squad = mi_fp
        elif user_choice1 == 'RR':
            Team1_Squad = rr_fp
        elif user_choice1 == 'GT':
            Team1_Squad = gt_fp
        elif user_choice1 == 'LSG':
            Team1_Squad = lsg_fp
        else:
            print("Invalid choice.")

        if user_choice2 == 'SRH':
            Team2_Squad = srh_fp
        elif user_choice2 == 'PBKS':
            Team2_Squad = pbks_fp
        elif user_choice2 == 'CSK':
            Team2_Squad = csk_fp
        elif user_choice2 == 'KKR':
            Team2_Squad = kkr_fp
        elif user_choice2 == 'DC':
            Team2_Squad = dc_fp
        elif user_choice2 == 'RCB':
            Team2_Squad = rcb_fp
        elif user_choice2 == 'MI':
            Team2_Squad = mi_fp
        elif user_choice2 == 'RR':
            Team2_Squad = rr_fp
        elif user_choice2 == 'GT':
            Team2_Squad = gt_fp
        elif user_choice2 == 'LSG':
            Team2_Squad = lsg_fp
        else:
            print("Invalid choice.")

        selected_players1 = request.form.getlist('player1')
        selected_players2 = request.form.getlist('player2')
        print(selected_players1)
        print(selected_players2)

        if len(selected_players1) == 11 and len(selected_players2) == 11:
            Team_1 = selected_players1
            Team_2 = selected_players2
              
        else:
            error_message = 'Please select exactly 11 players for both teams.'
            return render_template('player.html', players1=players1, players2=players2, error_message=error_message)

        t1 = get_players(Team_1, Team_2, Team1_Squad)
        t2 = get_players(Team_2, Team_1, Team2_Squad)

        t3 = t1 + t2
        t3.sort(reverse=True)
        Team = pd.DataFrame(t3)
        Result = Team[1].head(11)
        Result = pd.DataFrame(Result)
        print('\nFinal Predicted Team',Result)

        predicted_team = Result.to_html()  # Convert the result to HTML

        return render_template('result.html', predicted_team=predicted_team)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
