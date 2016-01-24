-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- initial drops from database recreation if needed

drop view if exists summary;
drop view if exists omw;
drop view if exists standings_wins;
drop view if exists standings_defeats;
drop table if exists matches;
drop table if exists players;

create table players (
    id serial primary key,
    name varchar(100)
);

create table matches (
    id serial primary key,
    winner_id integer references players(id),
    loser_id integer references players(id)
);

-- the 3 following views are needed to support the main one, called summary
create view standings_wins as
    select players.id, players.name, count(matches.winner_id) as wins
        from players left join matches
        on players.id = matches.winner_id
        group by players.id
        order by wins desc;

create view standings_defeats as
    select players.id, players.name, count(matches.loser_id) as defeats
        from players left join matches
        on players.id = matches.loser_id
        group by players.id
        order by defeats desc;

create view omw as
    select s1.id, coalesce(sum(s2.wins), 0) as omw_value
        from standings_wins s1 left join matches m1
        on s1.id = m1.winner_id
        left join matches m2
        on m2.winner_id = m1.loser_id
        left join standings_wins s2
        on m2.winner_id = s2.id
        group by s1.id;

-- summary is the main view, which sorts the players by both number of wins
-- and opponent wins
create view summary as 
    select standings_wins.id, standings_wins.name, standings_wins.wins,
    omw.omw_value as omw,
    (standings_wins.wins + standings_defeats.defeats) as matches
    from standings_wins join standings_defeats
    on standings_wins.id = standings_defeats.id
    left join omw
    on standings_wins.id = omw.id
    order by wins desc, omw desc;
