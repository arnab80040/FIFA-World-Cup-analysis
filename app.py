import pandas as pd
import streamlit
import streamlit as st
import preprocesor, helper
import plotly.express as px
import plotly.graph_objects as go




merged_table = preprocesor.preprocess()
match = preprocesor.preprocess_match()
goals = preprocesor.preprocess_goals()
goals_all_editions = preprocesor.preprocess_goals_all_editions()
all_matches_1930_2022 = preprocesor.preprocess_all_edition_matches()
matches_2022 = preprocesor.get_matches_played_2022()

st.sidebar.title("FIFA World Cup analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overview 2022 WC', 'Goals per team WC 2022', 'Golden boot WC 2022', 'Own goals WC 2022', 'Teams head to head comparison', 'Discipline WC 2022', 'All editions overview')
)





if user_menu == 'Goals per team WC 2022':
    teams = helper.all_teams_list(match)
    selected_team = st.sidebar.selectbox("Select Team", teams)
    if selected_team == "All":
        st.header("Goals Per Team in FIFA World Cup 2022")
    else:
        st.title("Goals scored by " + selected_team)
    result = helper.fetch_goal_tally(merged_table, selected_team)
    st.table(result)

elif user_menu == 'Golden boot WC 2022':
    players = helper.all_goalscorer_list(goals)
    selected_player = st.sidebar.selectbox("Select Player", players)
    if selected_player == "All":
        st.header("Golden Boot List FIFA WC 2022")
    elif selected_player == "Golden boot winner":
        st.title("Golden Boot Winner")
    else:
        st.title("Goals scored by " + selected_player)
    result = helper.fetch_goal_tally_players(goals, selected_player)
    st.table(result)

elif user_menu == 'Own goals WC 2022':
    st.header("All Own Goals in FIFA WC 2022")
    result = helper.own_goals(merged_table)
    st.table(result)



elif user_menu == "All editions overview":
    number_matches = all_matches_1930_2022['Tournament Id'].count()
    number_editions = all_matches_1930_2022['Tournament Id'].unique().shape[0]
    number_goals = goals_all_editions['player_team_name'].count()
    t1 = all_matches_1930_2022['Home Team Name'].unique().tolist()
    t2 = all_matches_1930_2022['Away Team Name'].unique().tolist()
    hosts = all_matches_1930_2022['Country Name'].unique().shape[0]

    res = t1 + t2
    r = len([*set(res)])
    col1, col2, col3= st.columns(3)
    with col1:
        st.header("Editions")
        st.title(number_editions)
    with col2:
        st.header("Goals")
        st.title(number_goals)
    with col3:
        st.header("Matches")
        st.title(number_matches)

    st.header("\n\n\n\n\n\n\n\n\n\n\n")

    col4, col5 = st.columns(2)
    with col4:
        st.header("Nations")
        st.header("qualified")
        st.title(r)
    with col5:
        st.header("Hosting")
        st.header("nations")
        st.title(hosts)

    st.header("\n\n\n\n\n\n\n\n\n\n\n")

    st.header("Host names and number of times they have hosted")
    temp100 = all_matches_1930_2022.drop_duplicates(subset=['Tournament Id', 'Country Name'], keep='last')[
        'Country Name'].value_counts()
    host_names = temp100.reset_index().rename(columns={'Country Name': 'Host country', 'count': 'times hosted'})
    fig2 = px.bar(host_names, x="Host country", y="times hosted")
    st.plotly_chart(fig2)


    st.header("Winning countries and times they have won")
    all_editions_list = helper.get_list_all_editions(all_matches_1930_2022)
    editions_and_winner = []
    for i in range(len(all_editions_list)):
        editions_and_winner.append(
            (all_editions_list[i], helper.get_match_winner(all_matches_1930_2022, all_editions_list[i])))

    editions_and_winner_table = pd.DataFrame(editions_and_winner, columns=['Edition', 'Champions'])
    new_table = editions_and_winner_table['Champions'].value_counts().reset_index().rename(
        columns={'Champions': 'Country', 'count': 'Times Won'})
    fig6 = px.bar(new_table, y="Country", x="Times Won", orientation='h')
    st.plotly_chart(fig6)
    st.text(
        "**West Germany and East Germany united to form Germany since October 3, 1990,\nsince then both the teams have participated as a single country named \"Germany\"")

    st.header("Finals of all editions")
    st.table(helper.get_finals(all_matches_1930_2022))

    st.header("All time top 15 goalscorers")
    st.table(goals_all_editions[goals_all_editions['own_goal'] == 0][['given_name', 'family_name', 'player_team_name']].value_counts().reset_index().rename(columns={'given_name': 'First name', 'family_name': 'Last name', 'count': 'Goals scored', 'player_team_name':'Country'}).head(15))

    st.header("Total matches played per edition")
    matches_per_edition = helper.get_matches_per_edition(all_matches_1930_2022)
    fig11 = px.line(matches_per_edition, x = "Edition", y = "Total matches played")
    st.plotly_chart(fig11)

    st.header("Matches played by countries in FIFA World Cups:")
    all_teams_1930_2022 = helper.get_1930_2022_teams(all_matches_1930_2022)
    selected_nation = st.selectbox("Select Country", all_teams_1930_2022)
    matches_played_1930_2022 = helper.get_matches_played_1930_2022(all_matches_1930_2022, selected_nation)
    if(matches_played_1930_2022 != 1):
        st.text(selected_nation + " played " + str(matches_played_1930_2022) + " matches in FIFA World cups since 1930.")
    else:
        st.text(selected_nation + " played only " + str(matches_played_1930_2022) + " match in FIFA World cups since 1930.")


    st.header("Goals scored per edition")
    goals_per_edition = helper.goals_scored_per_edition(goals_all_editions)
    fig8 = px.line(goals_per_edition, x="Edition", y="Goals scored")
    st.plotly_chart(fig8)

    st.header("Top 5 countries with most goals scored")
    temp1000 = goals_all_editions['player_team_name'].value_counts()
    all_country_goals = temp1000.reset_index().rename(columns={'player_team_name': 'Country', 'count': 'Goals scored'})
    fig3 = px.bar(all_country_goals.head(5), y="Country", x="Goals scored", orientation='h')
    st.plotly_chart(fig3)


    st.header("Goal ratio per edition of FIFA World Cups")
    goal_ratios = helper.get_goal_ratios(goals_all_editions, all_matches_1930_2022)
    fig = px.line(goal_ratios, x = 'index', y = 'Goal ratio')
    st.plotly_chart(fig)





elif user_menu == "Overview 2022 WC":
    number_teams_2022 = matches_2022['Home Team Name'].unique().shape[0]
    number_matches_2022 = matches_2022['Match Id'].count()
    number_cities_2022 = matches_2022['City Name'].unique().shape[0]
    number_stadiums_2022 = matches_2022['Stadium Name'].unique().shape[0]
    number_goals_scored = merged_table['goal_id'].count()
    temp50 = matches_2022.drop_duplicates(subset=['Country Name'], keep='first')['Country Name']
    host_country = temp50.tolist()[0]


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Nations")
        st.title(number_teams_2022)
    with col2:
        st.header("Matches")
        st.title(number_matches_2022)
    with col3:
        st.header("Goals")
        st.title(number_goals_scored)

    st.header("\n\n\n\n\n\n\n\n\n\n\n")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Host")
        st.title(host_country)
    with col5:
        st.header("Cities")
        st.title(number_cities_2022)
    with col6:
        st.header("Stadiums")
        st.title(number_stadiums_2022)

    st.header("\n\n\n\n\n\n\n\n\n\n\n")

    cities_hosts = helper.cities_hosted(matches_2022)
    fig4 = px.pie(cities_hosts, values = 'Matches hosted', names = 'City', title="Percentage of matches hosted per city")
    streamlit.plotly_chart(fig4)

    st.header("\n\n\n\n\n\n\n\n\n\n\n")

    stadiums_hosts = helper.stadiums_hosted(matches_2022)
    fig5 = px.pie(stadiums_hosts, values='Matches hosted', names='Stadium', title="Percentage of matches hosted per stadium")
    st.plotly_chart(fig5)

    st.header("Average ball possession per team")
    teams_2022 = helper.only_teams_list(match)
    selected_country_team = st.selectbox("Select team", teams_2022)
    avg_poss = helper.find_possession(match, selected_country_team)
    st.text("Average ball possession of " + selected_country_team + " in 2022 WC was " + str(avg_poss) +"%.")




    st.header("Attempts taken and on target per team")

    teams_and_shot_sonversion = []
    teams_in_2022 = helper.only_teams_list(match)
    for i in range(len(teams_in_2022)):
        teams_and_shot_sonversion.append((teams_in_2022[i], helper.shot_conversion_rate(match, goals, teams_in_2022[i]),helper.get_attempts_taken(match, teams_in_2022[i]), helper.attempts_on_goal_by(match, teams_in_2022[i])))



    temp60 = pd.DataFrame(teams_and_shot_sonversion, columns=['Team', 'Shot conversion rate(%)', 'Shots taken', 'On target'])
    shot_conversion = temp60.sort_values('Shot conversion rate(%)', ascending=False)
    fig12 = px.bar(shot_conversion, y = ["Shots taken", "On target"], x = "Team")
    st.plotly_chart(fig12)
    st.header("Shot conversion rates per team")
    shot_conversion.drop(['Shots taken'], axis=1, inplace=True)
    shot_conversion.drop(['On target'], axis=1, inplace=True)
    st.table(shot_conversion)

elif user_menu == 'Teams head to head comparison':
    teams_in_2022 = helper.only_teams_list((match))
    selected_team1 = st.sidebar.selectbox("Select team 1", teams_in_2022)
    selected_team2 = st.sidebar.selectbox("Select team 2", teams_in_2022)
    fig15 = go.Figure()
    st.header("Attacking stats")
    categories = ["Shots taken", "Shots on target", "Goals scored", "Average ball possession", "Shot conversion rate"]
    fig15.add_trace(go.Scatterpolar(
        r=[helper.get_attempts_taken(match, selected_team1), helper.attempts_on_goal_by(match,selected_team1), helper.get_goals_scored_individual(goals, selected_team1), helper.find_possession(match, selected_team1), helper.shot_conversion_rate(match, goals, selected_team1)],
        theta=categories,
        fill='toself',
        name=selected_team1
    ))
    fig15.add_trace(go.Scatterpolar(
        r=[helper.get_attempts_taken(match, selected_team2), helper.attempts_on_goal_by(match, selected_team2), helper.get_goals_scored_individual(goals, selected_team2), helper.find_possession(match, selected_team2), helper.shot_conversion_rate(match, goals, selected_team2)],
        theta=categories,
        fill='toself',
        name=selected_team2
    ))
    st.plotly_chart(fig15)

    fig16 = go.Figure()
    st.header("Defensive/in possession stats")
    categories2 = ["Forced turnovers", "Defensive pressures applied", "Goal preventions", "Average infront offers to receive", "Average passes completed"]
    fig16.add_trace(go.Scatterpolar(
        r=[helper.forced_turnovers_by(match, selected_team1), helper.defensive_pressures_applied_by(match, selected_team1), helper.goal_preventions_by(match, selected_team1), helper.average_infront_offers_to_receive_by(match, selected_team1), helper.average_passes_completed_by(match, selected_team1)],
        theta=categories2,
        fill='toself',
        name=selected_team1
    ))
    fig16.add_trace(go.Scatterpolar(
        r=[helper.forced_turnovers_by(match, selected_team1), helper.defensive_pressures_applied_by(match, selected_team2), helper.goal_preventions_by(match, selected_team2), helper.average_infront_offers_to_receive_by(match, selected_team2), helper.average_passes_completed_by(match, selected_team2)],
        theta=categories2,
        fill='toself',
        name=selected_team2
    ))
    st.plotly_chart(fig16)

elif user_menu == "Discipline WC 2022":
    st.header("Yellow and Red cards per team")
    yellow_and_red_cards = []
    teams_2022 = helper.only_teams_list(match)
    for i in range(len(teams_2022)):
        yellow_and_red_cards.append((teams_2022[i], helper.get_yellow_cards(match, teams_2022[i]), helper.get_red_cards(match, teams_2022[i])))
    yellow_red_cards = pd.DataFrame(yellow_and_red_cards, columns = ['Team', 'Yellow cards', 'Red cards'])
    fig7 = px.bar(yellow_red_cards, x='Team', y=['Red cards', 'Yellow cards'])
    st.plotly_chart(fig7)
    fair_play_award_winner = yellow_red_cards.sort_values(['Red cards', 'Yellow cards']).head(1)['Team'].tolist()[0]
    st.header("Fair Play Award")
    st.title(fair_play_award_winner)

