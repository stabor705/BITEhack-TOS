DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

DROP TABLE IF EXISTS integrals;
DROP TABLE IF EXISTS user_windows;
DROP TABLE IF EXISTS ans_windows;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS game_data;
DROP TABLE IF EXISTS game_data_details;

CREATE TABLE integrals (
    id integer PRIMARY KEY,
    integral_string text NOT NULL,
    integral_type text,
    integral_level integer
);

CREATE TABLE user_windows (
    id integer NOT NULL,
    proposed_answers integer NOT NULL,
    FOREIGN KEY (id) REFERENCES integrals (id),
    CONSTRAINT user_windows_PK PRIMARY KEY(id, proposed_answers)
);

CREATE TABLE ans_windows (
    id integer NOT NULL,
    window_id integer NOT NULL,
    window_number integer NOT NULL,
    FOREIGN KEY (id) REFERENCES integrals (id),
    CONSTRAINT ans_windows PRIMARY KEY(id, window_id)

);

CREATE TABLE users (
    id integer NOT NULL PRIMARY KEY,
    user_name text
);

CREATE TABLE game_data (
    user_id integer NOT NULL, --FOREIGN KEY REFERENCES('users.id'),
    id integer PRIMARY KEY,
    score_in_game integer NOT NULL,
    longest_series integer NOT NULL,
    game_start_time integer NOT NULL,
    game_finish_time integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE game_data_details (
    game_id integer NOT NULL,
    integral_id integer NOT NULL,
    number_of_trials integer NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game_data (id),
    FOREIGN KEY (integral_id) REFERENCES integrals (id),
    CONSTRAINT game_data_details_PK PRIMARY KEY(game_id, integral_id)
);