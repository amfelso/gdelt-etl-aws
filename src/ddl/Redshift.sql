/* This code defines the final Redshift Events table(s) for analysis.
You can add additional tables based on analysis interests.
For example, adding a EventsbyReligionandType table using the religion and event type dimensions. */

CREATE TABLE EventsbyCountryandType
(
EventID INTEGER,
EventYear INTEGER,
EventCountry VARCHAR(64),
EventType VARCHAR(128),
EventSubtype VARCHAR(128),
QuadClass INTEGER, --primary classification for the event type, allowing analysis at the highest level of aggregation
GoldsteinScale REAL, --a numeric score capturing the theoretical potential impact on the stability of a country
NumMentions INTEGER, --can be used as a method of assessing the “importance” of an event
AvgTone REAL, --average “tone” of documents containing one or more mentions of this event
SourceURL VARCHAR(255)
);