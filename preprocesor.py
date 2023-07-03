import pandas as pd

goals_all = pd.read_csv('FIFA World Cup All Goals 1930-2022 - FIFA World Cup All Goals 1930-2022.csv')
match = pd.read_csv('Matches 2022 FIFA WC - Fifa_world_cup_matches.csv')
all_matches_1930_2022 = pd.read_csv('FIFA World Cup 1930-2022 All Match Dataset.csv')

def preprocess():
    global goals_all, match
    #filtering for 2022 WC
    goals = goals_all[goals_all['tournament_id'] == 'WC-2022']
    merged_table = goals.merge(match, left_on='match_id', right_on='match_id')
    return merged_table

def preprocess_match():
    global match
    match.at[54, 'team2'] = 'Spain'
    match.at[26, 'team1'] = 'Croatia'
    match.at[40, 'team1'] = 'Croatia'
    match.at[8, 'team2'] = 'Croatia'
    match.at[62, 'team1'] = 'Croatia'
    match.at[60, 'team2'] = 'Croatia'
    match.at[56, 'team1'] = 'Croatia'
    match.at[52, 'team2'] = 'Croatia'
    return match


def preprocess_goals():
    global goals_all
    goals = goals_all[goals_all['tournament_id'] == 'WC-2022']
    return goals

def preprocess_goals_all_editions():
    global goals_all
    return goals_all

def preprocess_all_edition_matches():
    global all_matches_1930_2022
    return all_matches_1930_2022

def get_matches_played_2022():
    global all_matches_1930_2022
    return all_matches_1930_2022[all_matches_1930_2022['Tournament Id'] == "WC-2022"]