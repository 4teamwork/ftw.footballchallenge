# -*- coding: utf-8 -*-
"""Defines some Globals"""

#Pointmappings for every event. We need four because the Points
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
POSITION_MAPPING={
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
    u'Mittelfeld - Rechtes Mittelfeld': 'midfield'}

COUNTRY_CODE_MAPPING = {
    u'Deutschland': 'de',
    u'Dänemark': 'dk',
    u'England': 'uk',
    u'Frankreich': 'fr',
    u'Griechenland': 'gr',
    u'Irland': 'ir',
    u'Italien': 'it',
    u'Kroatien': 'hr',
    u'Niederlande': 'nl',
    u'Polen': 'pl',
    u'Portugal': 'pt',
    u'Russland': 'ru',
    u'Schweden': 'se',
    u'Spanien': 'es',
    u'Tschechien': 'cz',
    u'Ukraine': 'ua',
}



PROJECTNAME = 'ftw.footballchallenge'
