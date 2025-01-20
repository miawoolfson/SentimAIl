-- Table: sentimail.emails

create table if not exists sentimail.emails
(
    id serial primary key,
    sender text,
    recipient text,
    sent_time timestamp,
    received_time timestamp,
    email text,
    sentiment_score numeric,
);
