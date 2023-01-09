/* This code can be used to create dimension tables.
You can use the provided dimension .txt files to load tables.
Prerequisites: create RDS database
Background info on CAMEO framework here: https://en.wikipedia.org/wiki/Conflict_and_Mediation_Event_Observations
Background info on FIPS standard here: https://en.wikipedia.org/wiki/FIPS_10-4 */

CREATE DATABASE DIM;
USE DIM;

-- Define all dimension tables
CREATE TABLE Country (
    CODE CHAR(2),
    LABEL VARCHAR(64)
);

CREATE TABLE Ethnic (
    CODE CHAR(3),
    LABEL VARCHAR(32)
);

CREATE TABLE Event (
    CAMEOEVENTCODE VARCHAR(4),
    EVENTDESCRIPTION VARCHAR(128)
);

CREATE TABLE KnownGroup (
    CODE CHAR(3),
    LABEL VARCHAR(128)
);

CREATE TABLE Religion (
    CODE CHAR(3),
    LABEL VARCHAR(32)
);

CREATE TABLE Type (
    CODE CHAR(3),
    LABEL VARCHAR(64)
);