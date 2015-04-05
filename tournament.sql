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
CREATE TABLE IF NOT EXISTS matches ( id SERIAL,
					winner INTEGER references players(id),
					loser INTEGER references players(id),
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
					);
-- sql view representing players with wins and number of matches
CREATE VIEW player_standings as 
					select p.id,
					p.name,
					sum(case when p.id=m.winner then 1 else 0 end) as wins,
					count(m.id) as matches
					from  players as p left join matches as m  
						on p.id=m.winner OR
						   p.id = m.loser
					group by p.id 
					order by wins DESC;
					  