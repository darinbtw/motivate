CREATE TABLE users(
	id_user SERIAL PRIMARY KEY,
	mail text not null,
	password text not null,
	first_name text not null,
	secret_question text not null,
	secret_answer text not null
);

CREATE TABLE cards_of_users(
	id_card SERIAL PRIMARY KEY,
	card_number varchar(20),
	time_card varchar(5),
	cvv varchar(3)
);

CREATE TABLE motivatly(
	quest text not null,
	post_date date not null
);