-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players ( 
    player_id SERIAL PRIMARY KEY, 
    name TEXT, player_wins integer DEFAULT 0, 
    player_matches integer DEFAULT 0
);
CREATE TABLE Matches ( 
    Match_id SERIAL, 
    winner_id integer references Players(player_id) ,
    loser_id integer references Players(player_id)
);

CHECK(winner_id <> loser_id)
