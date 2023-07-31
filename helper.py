import numpy as np


def fetch_goal_tally(merged_table, team):
    not_own_goals = merged_table[merged_table['own_goal'] == 0]
    team_goals = not_own_goals['player_team_name'].value_counts().reset_index()
    if team == "All":
        return team_goals.rename(columns = {'count':'goals scored', 'player_team_name':'Team name'})
    else:
        return team_goals[team_goals['player_team_name'] == team].rename(columns = {'count':'goals scored', 'player_team_name':'Team name'})

def fetch_goal_tally_players(goals, player):
    player_goals = goals[goals['own_goal'] == 0].groupby(['family_name'])['match_name'].count().sort_values(ascending=False).reset_index()

    if (player == "All"):
        return player_goals.rename(columns={'match_name': 'Goals Scored', 'family_name':'player'})
    elif (player == "Golden boot winner"):
        return player_goals['family_name'].head(1).reset_index().rename(columns = {'family_name':'winner'})
    else:
        return player_goals[player_goals['family_name'] == player].rename(columns={'match_name': 'Goals Scored', 'family_name':'player'})

def all_goals_players(merged_table):
    all_goals_2022 = merged_table[['team1', 'team2', 'given_name', 'family_name', 'player_team_name']]
    return all_goals_2022


def goals_by_teams(merged_table):
    not_own_goals = merged_table[merged_table['own_goal'] == 0]
    team_goals = not_own_goals['player_team_name'].value_counts().reset_index()
    return team_goals


def golden_boot(merged_table):
    goals_2022 = merged_table[['given_name', 'family_name']].value_counts().reset_index()
    return goals_2022

def own_goals(merged_table):
    own_goals_2022 = merged_table[merged_table['own_goal'] == 1]
    own_goals = own_goals_2022[['given_name', 'family_name', 'match_name', 'player_team_name']]
    return own_goals

def all_teams_list(match):
    teams = np.unique(match['team1'])
    all_teams_list = teams.tolist()
    all_teams_list.sort()
    all_teams_list.insert(0, "All")
    return all_teams_list

def all_goalscorer_list(goals):
    players = goals[goals['own_goal'] == 0].groupby(['family_name'])['match_name'].count().sort_values(ascending=False)
    goalscorer_list = players.index.tolist()
    goalscorer_list.insert(0, "Golden boot winner")
    goalscorer_list.insert(0, "All")
    return goalscorer_list

def matches_played_by_team(match, team):
    y1 = match.groupby('team1')
    e = y1.get_group(team)['team2'].count()
    y2 = match.groupby('team2')
    f = y2.get_group(team)['team1'].count()
    return e + f

def only_teams_list(match):
    teams = np.unique(match['team1'])
    all_teams_list = teams.tolist()
    all_teams_list.sort()
    return all_teams_list


def find_possession(match, team):
    x1 = match.groupby('team1')
    c = x1.get_group(team)['possession team1'].str.rstrip('%').astype('float').sum()
    x2 = match.groupby('team2')
    d = x2.get_group(team)['possession team2'].str.rstrip('%').astype('float').sum()
    return (c+d)/matches_played_by_team(match, team)


def get_finals(all_matches_1930_2022):
    finals_detailed = all_matches_1930_2022.drop_duplicates(subset = ['Tournament Id'], keep = 'last')
    finals = finals_detailed[['tournament Name', 'Home Team Name', 'Away Team Name', 'Result']].reset_index().rename(columns = {'Home Team Name':'Home Team', 'Away Team Name':'Away Team', 'tournament Name':'Final of Edition'})
    return finals


def get_matches_per_edition(all_matches_1930_2022):
    temp3 = all_matches_1930_2022['tournament Name'].value_counts()
    matches_per_edition = temp3.reset_index()
    res =  matches_per_edition.rename(columns={'tournament Name': 'Edition', 'count': 'Total matches played'}).sort_values("Edition")
    return res


def goals_scored_per_edition(goals_all):
    temp2 = goals_all['tournament_name'].value_counts()
    goals_per_edition = temp2.reset_index()
    return goals_per_edition.rename(columns={'tournament_name': 'Edition', 'count': 'Goals scored'}).sort_values("Edition")

def get_goal_ratios(goals_all, all_matches_1930_2022):
    temporary = goals_all['tournament_id'].value_counts() / all_matches_1930_2022['Tournament Id'].value_counts()
    goal_ratios = temporary.reset_index()
    goal_ratios.rename(columns={'count': 'Goal ratio'}, inplace=True)
    return goal_ratios


def get_1930_2022_teams(all_matches_1930_2022):
    home_teams = all_matches_1930_2022['Home Team Name'].unique().tolist()
    away_teams = all_matches_1930_2022['Away Team Name'].unique().tolist()
    all_teams = home_teams + away_teams
    all_teams_qualified = [*set(all_teams)]
    all_teams_qualified.sort()
    return all_teams_qualified

def get_matches_played_1930_2022(all_matches_1930_2022, team):
    temp20 = all_matches_1930_2022.groupby('Home Team Name')
    temp21 = all_matches_1930_2022.groupby('Away Team Name')
    try:
        res = (temp20.get_group(team)['Match Id'].count() + temp21.get_group(team)['Match Id'].count())
    except:
        res = temp21.get_group(team)['Match Id'].count()
    return res


def cities_hosted(matches_2022):
    cities_hosted = matches_2022['City Name'].value_counts().reset_index()
    cities_hosted.rename(columns={'City Name': 'City', 'count': 'Matches hosted'}, inplace=True)
    return cities_hosted

def stadiums_hosted(matches_2022):
    stadiums_hosted = matches_2022['Stadium Name'].value_counts().reset_index()
    stadiums_hosted.rename(columns={'Stadium Name': 'Stadium', 'count': 'Matches hosted'}, inplace=True)
    return stadiums_hosted

def get_attempts_taken(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')['total attempts team1'].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')['total attempts team2'].sum()
    return (a + b)

def attempts_on_goal_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')['on target attempts team1'].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')['on target attempts team2'].sum()
    return (a + b)

def goals_per_minute(goals_all_editions):
    all_goals_2022 = goals_all_editions[goals_all_editions['tournament_id'] == "WC-2022"]
    goals_per_minute = all_goals_2022["minute_regulation"].value_counts().reset_index()
    goals_per_minute.rename(columns={"minute_regulation": "Minute", "count": "Goals scored"}, inplace=True)
    goals_per_minute.sort_values("Minute", inplace=True)
    return goals_per_minute

def get_goals_scored_individual(goals, team):
    goals2 = goals[goals['own_goal'] == 0]
    res = goals2[goals2['player_team_name'] == team]['goal_id'].count()
    return res

def shot_conversion_rate(match, goals, team):
    res = get_goals_scored_individual(goals, team)*100/get_attempts_taken(match, team)
    return res

def get_red_cards(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')['red cards team1'].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')['red cards team2'].sum()
    return a+b


def get_yellow_cards(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')['yellow cards team1'].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')['yellow cards team2'].sum()
    return a+b

def get_match_winner(all_matches_1930_2022, tournament_name):
    finals = get_finals(all_matches_1930_2022)
    match_individual = finals[finals['Final of Edition'] == tournament_name]
    if match_individual.iloc[0, [2, 3, 4]]['Result'] == "home team win":
        winner =  match_individual.iloc[0, [2, 3, 4]]['Home Team']
    else:
        winner = match_individual.iloc[0, [2, 3, 4]]['Away Team']
    return winner

def get_list_all_editions(all_matches_1930_2022):
    all_editions_list = all_matches_1930_2022['tournament Name'].unique().tolist()
    return all_editions_list


def get_goals_per_minute(goals):
    pt = goals.pivot_table(index='minute_regulation', columns='player_team_name', values='goal_id', aggfunc='count')
    pt.sort_values("minute_regulation")
    pt.rename(volumns = {"player_team_name: Team"})
    return pt

def forced_turnovers_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')["forced turnovers team1"].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')["forced turnovers team2"].sum()
    return a+b

def defensive_pressures_applied_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')["defensive pressures applied team1"].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')["defensive pressures applied team2"].sum()
    return a+b

def goal_preventions_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')["goal preventions team1"].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')["goal preventions team2"].sum()
    return a+b

def average_infront_offers_to_receive_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')["infront offers to receive team1"].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')["infront offers to receive team2"].sum()
    return (a+b)/matches_played_by_team(match, team)

def average_passes_completed_by(match, team):
    cond1 = match.groupby('team1')
    a = cond1.get_group(team).drop_duplicates('team2')["passes completed team1"].sum()
    cond2 = match.groupby('team2')
    b = cond2.get_group(team).drop_duplicates('team1')["passes completed team2"].sum()
    return (a+b)/matches_played_by_team(match, team)
