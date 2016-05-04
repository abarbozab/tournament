-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';
\c tournament;
CREATE TABLE tournament(
	 id SERIAL PRIMARY KEY
	,name VARCHAR(50)
);
CREATE TABLE player(
	 id SERIAL PRIMARY KEY
	,name VARCHAR(50)
);
CREATE TABLE player_tournament(
	 id SERIAL PRIMARY KEY
	,id_tournament INTEGER REFERENCES tournament(id)
   	,id_player INTEGER REFERENCES player(id)
);
CREATE TABLE match(
	 id SERIAL PRIMARY KEY
	,id_tournament INTEGER REFERENCES tournament(id)
	,winner INTEGER REFERENCES player_tournament(id)
	,loser INTEGER REFERENCES player_tournament(id)
);

CREATE VIEW scoreboard AS
	SELECT
		 play.id
		,play.name
        ,(SELECT COUNT(1) FROM match mat WHERE mat.winner = plat.id) as wins
        ,(SELECT COUNT(1) FROM match mat WHERE mat.loser = plat.id) as loses
        ,plat.id_tournament
        ,plat.id as id_player_tournament
	FROM player_tournament plat
	JOIN player play ON plat.id_player = play.id
	

