# -*- coding: utf-8 -*-
"""Defines some Globals"""

# Pointmappings for every event. We need four because the Points
# defer from Position to Position
POINT_MAPPING_STRIKER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow': -6,
    'yellow': -2,
    'goal': 6,
    'assist': 4,
    'penalty': 4}

POINT_MAPPING_MIDFIELD = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow': -6,
    'yellow': -2,
    'goal': 6,
    'assist': 4,
    'penalty': 4}

POINT_MAPPING_DEFENDER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow': -6,
    'yellow': -2,
    'goal': 8,
    'assist': 6,
    'penalty': 4,
    'no_goals': 4,
    '3_goals': -4}

POINT_MAPPING_KEEPER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow': -6,
    'yellow': -2,
    'goal': 20,
    'assist': 10,
    'penalty': 6,
    'no_goals': 4,
    '3_goals': -4,
    'save': 4}

# This Mapping is required for the playerimport,
# since we need to change the Positions to the one we need.
POSITION_MAPPING = {
    u'Torwart': 'keeper',
    u'Abwehr - Rechter Verteidiger': 'defender',
    u'Abwehr - Linker Verteidiger': 'defender',
    u'Abwehr - Innenverteidiger': 'defender',
    u'Mittelfeld - Defensives Mittelfeld': 'midfield',
    u'Mittelfeld - Zentrales Mittelfeld': 'midfield',
    u'Mittelfeld - Offensives Mittelfeld': 'midfield',
    u'Mittelfeld - Linksau\xdfen': 'midfield',
    u'Mittelfeld - Rechtsau\xdfen': 'midfield',
    u'Sturm - Mittelst\xfcrmer': 'striker',
    u'Sturm - Rechtsau\xdfen': 'striker',
    u'Sturm - Linksau\xdfen': 'striker',
    u'Sturm - H\xe4ngende Spitze': 'striker',
    u'Mittelfeld - Linkes Mittelfeld': 'midfield',
    u'Mittelfeld - Rechtes Mittelfeld': 'midfield',
    u'Rechter Verteidiger': 'defender',
    u'Linker Verteidiger': 'defender',
    u'Innenverteidiger': 'defender',
    u'Defensives Mittelfeld': 'midfield',
    u'Zentrales Mittelfeld': 'midfield',
    u'Offensives Mittelfeld': 'midfield',
    u'Linksau\xdfen': 'midfield',
    u'Rechtsau\xdfen': 'midfield',
    u'Mittelst\xfcrmer': 'striker',
    u'H\xe4ngende Spitze': 'striker',
    u'Linkes Mittelfeld': 'midfield',
    u'Rechtes Mittelfeld': 'midfield',
}

# Official UEFA country codes
# These are *not* the same as ISO-3155-1-alpha3
COUNTRY_CODE_MAPPING = {
    u'Albanien': 'ALB',
    u'Algerien': 'ALG',
    u'Argentinien': 'ARG',
    u'Australien': 'AUS',
    u'Belgien': 'BEL',
    u'Bosnien-Herzegowina': 'BIH',
    u'Brasilien': 'BRA',
    u'Chile': 'CHI',
    u'Costa Rica': 'CRC',
    u'Deutschland': 'GER',
    u'Dänemark': 'DEN',
    u'Ecuador': 'ECU',
    u'Elfenbeinküste': 'CIV',
    u'England': 'ENG',
    u'Frankreich': 'FRA',
    u'Ghana': 'GHA',
    u'Griechenland': 'GRE',
    u'Honduras': 'HON',
    u'Iran': 'IRN',
    u'Irland': 'IRL',
    u'Island': 'ISL',
    u'Italien': 'ITA',
    u'Japan': 'JPN',
    u'Kamerun': 'CMR',
    u'Kolumbien': 'COL',
    u'Kroatien': 'CRO',
    u'Mexiko': 'MEX',
    u'Niederlande': 'NED',
    u'Nigeria': 'NGA',
    u'Nordirland': 'NIR',
    u'Österreich': 'AUT',
    u'Polen': 'POL',
    u'Portugal': 'POR',
    u'Rumänien': 'ROU',
    u'Russland': 'RUS',
    u'Schweden': 'SWE',
    u'Schweiz': 'SUI',
    u'Slowakei': 'SVK',
    u'Spanien': 'ESP',
    u'Südkorea': 'KOR',
    u'Tschechien': 'CZE',
    u'Türkei': 'TUR',
    u'Ukraine': 'UKR',
    u'Ungarn': 'HUN',
    u'Uruguay': 'URU',
    u'Vereinigte Staaten': 'USA',
    u'Wales': 'WAL',
}

MULTIPLIER_MAPPING = {
    u'Mio.': 1000000,
    u'Tsd.': 1000,
}

PROJECTNAME = 'ftw.footballchallenge'
