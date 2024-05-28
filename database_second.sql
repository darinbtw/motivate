CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    goal TEXT NOT NULL,
    deadline TIMESTAMP NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
