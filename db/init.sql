-- db/init.sql
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    nickname VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    year_founded INT
);

CREATE TABLE nba_players (
    player_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    year_start INT,
    year_end INT,
    position VARCHAR(10),
    height VARCHAR(10),
    weight DECIMAL,
    birth_date DATE,
    hall_of_fame BOOLEAN,
    draft_overall DECIMAL,
    draft_info VARCHAR(50)
);

CREATE TABLE rs_player_stats (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(20) REFERENCES nba_players(player_id),
    team_id INT REFERENCES teams(team_id),
    season INT,
    age DECIMAL,
    games_played DECIMAL,
    games_started DECIMAL,
    minutes_played DECIMAL,
    fg DECIMAL,
    fga DECIMAL,
    fg_pct DECIMAL,
    three_p DECIMAL,
    three_pa DECIMAL,
    three_p_pct DECIMAL,
    two_p DECIMAL,
    two_pa DECIMAL,
    two_p_pct DECIMAL,
    efg_pct DECIMAL,
    ft DECIMAL,
    fta DECIMAL,
    ft_pct DECIMAL,
    orb DECIMAL,
    drb DECIMAL,
    trb DECIMAL,
    ast DECIMAL,
    stl DECIMAL,
    blk DECIMAL,
    tov DECIMAL,
    pf DECIMAL,
    pts DECIMAL,
    league VARCHAR(10),
    position VARCHAR(10)
);
