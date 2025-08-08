-- db/seed.sql
INSERT INTO teams (full_name, nickname, city, state, year_founded)
VALUES
('Los Angeles Lakers', 'Lakers', 'Los Angeles', 'CA', 1947),
('Boston Celtics', 'Celtics', 'Boston', 'MA', 1946);

INSERT INTO nba_players (player_id, name, year_start, year_end, position, height, weight, birth_date, hall_of_fame, draft_overall, draft_info)
VALUES
('jamesle01', 'LeBron James', 2004, 2025, 'SF', '6-9', 250.0, '1984-12-30', false, 1.0, '1 (2003)'),
('tatumbu01', 'Jayson Tatum', 2018, 2025, 'SF', '6-8', 210.0, '1998-03-03', false, 3.0, '3 (2017)');

INSERT INTO rs_player_stats (player_id, team_id, season, age, games_played, games_started, minutes_played, pts, ast, trb, fg_pct, three_p, three_pa, three_p_pct, ft, fta, ft_pct, league, position)
VALUES
('jamesle01', 1, 2023, 38, 55, 55, 1950, 1500, 400, 500, 0.51, 100, 300, 0.33, 200, 250, 0.80, 'NBA', 'SF'),
('tatumbu01', 2, 2023, 25, 70, 70, 2450, 2000, 350, 600, 0.47, 180, 500, 0.36, 300, 350, 0.86, 'NBA', 'SF');
