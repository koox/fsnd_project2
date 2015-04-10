-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DATABASE tournament;

-- drop the tables before creating them
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- create the players table 
CREATE TABLE IF NOT EXISTS players ( id SERIAL PRIMARY KEY,
					name TEXT
                	);

-- create the matches table 
CREATE TABLE IF NOT EXISTS matches ( id SERIAL PRIMARY KEY,
					winner INTEGER references players(id) ON DELETE CASCADE,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
					);

-- create the matches table 
CREATE TABLE IF NOT EXISTS players_to_matches ( id SERIAL,
					player_id INTEGER references players(id) ON DELETE CASCADE,
					match_id INTEGER references matches(id) ON DELETE CASCADE
					);

-- sql view representing players with wins and number of matches
CREATE VIEW player_standings as 
					select p.id,
					p.name,
					sum(case when p.id=m.winner then 1 else 0 end) as wins,
					count(p_m.player_id) as matches
					from  players as p 
					left join players_to_matches as p_m
						on p.id = p_m.player_id 
                    left join matches as m on
                         m.id = p_m.match_id
					group by p.id 
					order by wins DESC;             