nodes = [
    'Alexanderplatz',
    'Alte Münze',
    'Brandenburger Tor',
    'Friedrichstadt-Palast',
    'Führerbunker',
    'Gendarmenmarkt',
    'Haus des Lehrers',
    'Jannowitzbrücke',
    'Jugendpark',
    'KitKat',
    'Marion-Gräfin-Dönhoff-Platz',
    'Marx-Engels-Forum',
    'Michaelkirchplatz',
    'Museum for Communication',
    'Parlament der Bäume',
    'Unter den Linden',
    'Weltzeituhr',
    'Zentral und Landesbibliothek'
]

boundary_nodes = [
    'Alexanderplatz',
    'Brandenburger Tor',
    'Friedrichstadt-Palast',
    'Führerbunker',
    'Haus des Lehrers',
    'Jannowitzbrücke',
    'KitKat',
    'Marion-Gräfin-Dönhoff-Platz',
    'Michaelkirchplatz',
    'Museum for Communication',
    'Parlament der Bäume',
]

edges = [
    [
        'Unter den Linden',
        'Marx-Engels-Forum',
        1.6
    ],
    [
        "Parlament der Bäume",
        "Friedrichstadt-Palast",
        0.55
    ],
    [
        "Parlament der Bäume",
        "Brandenburger Tor",
        0.7
    ],
    [
        "Brandenburger Tor",
        "Unter den Linden",
        0.6
    ],
    [
        "Friedrichstadt-Palast",
        "Unter den Linden",
        0.8
    ],
    [
        "Unter den Linden",
        "Gendarmenmarkt",
        0.26
    ],
    [
        "Führerbunker",
        "Gendarmenmarkt",
        0.5
    ],
    [
        "Führerbunker",
        "Museum for Communication",
        0.5
    ],
    [
        "Museum for Communication",
        "Jugendpark",
        0.4
    ],
    [
        "Gendarmenmarkt",
        "Jugendpark",
        0.45
    ],
    [
        "Jugendpark",
        "Marion-Gräfin-Dönhoff-Platz",
        0.75
    ],
    [
        "Gendarmenmarkt",
        "Zentral und Landesbibliothek",
        0.55
    ],
    [
        "Marion-Gräfin-Dönhoff-Platz",
        "Zentral und Landesbibliothek",
        0.45
    ],
    [
        "Zentral und Landesbibliothek",
        "Alte Münze",
        0.4
    ],
    [
        "Zentral und Landesbibliothek",
        "Michaelkirchplatz",
        1.1
    ],
    [
        "Michaelkirchplatz",
        "KitKat",
        0.35
    ],
    [
        "Jannowitzbrücke",
        "KitKat",
        0.45
    ],
    [
        "Jannowitzbrücke",
        "Alte Münze",
        0.6
    ],
    [
        "Weltzeituhr",
        "Jannowitzbrücke",
        0.75
    ],
    [
        "Weltzeituhr",
        "Alte Münze",
        0.7
    ],
    [
        "Marx-Engels-Forum",
        "Alte Münze",
        0.5
    ],
    [
        "Weltzeituhr",
        "Haus des Lehrers",
        0.2
    ],
    [
        "Haus des Lehrers",
        "Alexanderplatz",
        0.3
    ],
    [
        "Alexanderplatz",
        "Marx-Engels-Forum",
        0.55
    ]
]
