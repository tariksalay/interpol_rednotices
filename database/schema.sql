CREATE TABLE IF NOT EXISTS interpol_rednotices (
    id SERIAL PRIMARY KEY,
    name_surname VARCHAR(100) NOT NULL,
    age VARCHAR(100) NOT NULL,
    nationality VARCHAR(100) NOT NULL
);
