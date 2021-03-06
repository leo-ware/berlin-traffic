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

boundary_points = [
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
    'Parlament der Bäume'
]

# these are the empirically derived values i got from the genetic algorithm in parameter_fitting.py
entry_rates = [0.14032044, 0.30658623, 0.10912543, 0.23781625, 0.12085641, 0.10615083, 0.20457665, 0.29638999, 0.80486029, 0.74148195, 0.11672643]
exit_rates = [7, 1, 3, 4, 8, 2, 9, 3, 6, 1, 6]

entry_points = dict(zip(boundary_points, entry_rates))
exit_points = dict(zip(boundary_points, exit_rates))

# each sublist has two intersections on either side of the street, then length (in km), then avg speed
edges_with_data = [
    [
        'Unter den Linden',
        'Marx-Engels-Forum',
        1.6,
        1
    ],
    [
        "Parlament der Bäume",
        "Friedrichstadt-Palast",
        0.55,
        2
    ],
    [
        "Parlament der Bäume",
        "Brandenburger Tor",
        0.7,
        2
    ],
    [
        "Brandenburger Tor",
        "Unter den Linden",
        0.6,
        2
    ],
    [
        "Friedrichstadt-Palast",
        "Unter den Linden",
        0.8,
        4
    ],
    [
        "Unter den Linden",
        "Gendarmenmarkt",
        0.26,
        2
    ],
    [
        "Führerbunker",
        "Gendarmenmarkt",
        0.5,
        2
    ],
    [
        "Führerbunker",
        "Museum for Communication",
        0.5,
        2
    ],
    [
        "Museum for Communication",
        "Jugendpark",
        0.4,
        2
    ],
    [
        "Gendarmenmarkt",
        "Jugendpark",
        0.45,
        2
    ],
    [
        "Jugendpark",
        "Marion-Gräfin-Dönhoff-Platz",
        0.75,
        4
    ],
    [
        "Gendarmenmarkt",
        "Zentral und Landesbibliothek",
        0.55,
        2
    ],
    [
        "Marion-Gräfin-Dönhoff-Platz",
        "Zentral und Landesbibliothek",
        0.45,
        4
    ],
    [
        "Zentral und Landesbibliothek",
        "Alte Münze",
        0.4,
        2
    ],
    [
        "Zentral und Landesbibliothek",
        "Michaelkirchplatz",
        1.1,
        1
    ],
    [
        "Michaelkirchplatz",
        "KitKat",
        0.35,
        2
    ],
    [
        "Jannowitzbrücke",
        "KitKat",
        0.45,
        2
    ],
    [
        "Jannowitzbrücke",
        "Alte Münze",
        0.6,
        1
    ],
    [
        "Weltzeituhr",
        "Jannowitzbrücke",
        0.75,
        2
    ],
    [
        "Weltzeituhr",
        "Alte Münze",
        0.7,
        1
    ],
    [
        "Marx-Engels-Forum",
        "Alte Münze",
        0.5,
        4
    ],
    [
        "Weltzeituhr",
        "Haus des Lehrers",
        0.2,
        1
    ],
    [
        "Haus des Lehrers",
        "Alexanderplatz",
        0.3,
        1
    ],
    [
        "Alexanderplatz",
        "Marx-Engels-Forum",
        0.55,
        1
    ]
]

edges = []
google_maps_speeds = []

for u, v, l, s in edges_with_data:
    edges.append([u, v, l])
    google_maps_speeds.append(s)
