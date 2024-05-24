import pandas as pd
from nba_api.stats.endpoints import playercareerstats, playergamelog, TeamGameLogs, commonplayerinfo


def get_player_career_stats(player_id):
    player_stats = playercareerstats.PlayerCareerStats(
        player_id=player_id)

    # gets alll seasons, pick the first for current season
    # print(player_stats.get_data_frames())
    player_stats_df = player_stats.get_data_frames()[0]
    return player_stats_df


def get_team_players_career_stats(player_ids):
    stats_df = []
    for player_id in player_ids:
        player_stats = playercareerstats.PlayerCareerStats(
            player_id=player_id)

        # gets alll seasons, pick the first for current season
        # print(player_stats.get_data_frames())
        player_stats_df = player_stats.get_data_frames()[0]
        stats_df.append(player_stats_df)

    return stats_df


def get_player_last_games(player_id, num_games):
    gamelog_regular = playergamelog.PlayerGameLog(
        player_id=player_id, season='2023-24', season_type_all_star='Regular Season').get_data_frames()[0]
    gamelog_playoffs = playergamelog.PlayerGameLog(
        player_id=player_id, season='2023-24', season_type_all_star='Playoffs').get_data_frames()[0]
    logs = pd.concat([gamelog_playoffs, gamelog_regular])
    return logs.head(num_games)


def get_player_seasons(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(
        player_id=player_id).get_data_frames()[0]
    from_year = player_info['FROM_YEAR'].values[0]
    to_year = player_info['TO_YEAR'].values[0]
    return range(from_year, to_year + 1)


def get_last_n_games_against_team(player_id, opponent_team_name, n):
    # Fetch game logs for all available seasons
    print(player_id, opponent_team_name, n)
    all_game_logs = pd.DataFrame()
    seasons = get_player_seasons(player_id)
    for season in seasons:
        season_str = f"{season}-{str(season + 1)[-2:]}"
        game_logs = playergamelog.PlayerGameLog(
            player_id=player_id, season=season_str).get_data_frames()[0]
        all_game_logs = pd.concat([all_game_logs, game_logs])

    print(all_game_logs)

    # Filter the game logs to only include games against the specified opponent
    games_against_team = all_game_logs[all_game_logs['MATCHUP'].str.contains(
        f'vs. {opponent_team_name}|@ {opponent_team_name}', regex=True)]

    if games_against_team.empty:
        return "Empty"

    # Sort by game date and get the last N games
    games_against_team = games_against_team.sort_values(
        by='GAME_DATE', ascending=False).head(n)

    return games_against_team
