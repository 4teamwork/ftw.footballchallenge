POINT_MAPPING_STRIKER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow':-6,
    'yellow': -2,
    'goal': 6,
    'assist': 4,
    'penalty': 4
}

POINT_MAPPING_MIDFIELD = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow':-6,
    'yellow': -2,
    'goal': 6,
    'assist': 4,
    'penalty': 4
}

POINT_MAPPING_DEFENDER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow':-6,
    'yellow': -2,
    'goal': 8,
    'assist': 6,
    'penalty': 4,
    'no_goals': 4,
    '3_goals': -4 
}

POINT_MAPPING_KEEPER = {
    'victory': 4,
    'draw': 2,
    'loss': -2,
    'red': -8,
    'second_yellow':-6,
    'yellow': -2,
    'goal': 20,
    'assist': 10,
    'penalty': 6,
    'no_goals': 4,
    '3_goals': -4,
    'save': 4 
}
POSITION_MAPPING={
    u'Torwart':'keeper',
    u'Abwehr - Rechter Verteidiger':'defender',
    u'Abwehr - Linker Verteidiger':'defender',
    u'Abwehr - Innenverteidiger':'defender',
    u'Mittelfeld - Defensives Mittelfeld':'midfield',
    u'Mittelfeld - Zentrales Mittelfeld':'midfield',
    u'Mittelfeld - Offensives Mittelfeld':'midfield',
    u'Mittelfeld - Linksau\xdfen':'midfield',
    u'Mittelfeld - Rechtsau\xdfen':'midfield',
    u'Sturm - Mittelst\xfcrmer':'striker',
    u'Sturm - Rechtsau\xdfen':'striker',
    u'Sturm - Linksau\xdfen':'striker',
    u'Sturm - H\xe4ngende Spitze':'striker',
    u'Mittelfeld - Linkes Mittelfeld':'midfield',
    u'Mittelfeld - Rechtes Mittelfeld':'midfield'
}

PROJECTNAME = 'ftw.footballchallenge'