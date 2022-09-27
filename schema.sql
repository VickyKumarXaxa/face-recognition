DROP TABLE IF EXISTS face_image;
DROP TABLE IF EXISTS image_data;

CREATE TABLE face_image(
    id serial PRIMARY KEY,
    face_encoding BYTEA NOT NULL,
);

CREATE TABLE image_data(
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    version numeric,
    date_created date DEFAULT,
    location varchar(50) 
);