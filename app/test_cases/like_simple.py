like_simple_cases = [
    {
        "query": "A/B/C",
        "operator": "~",
        "matches": [
            "A/B/C",
            "A/B/C/D",
        ],
        "no_matches": [
            "A/B/D",
            "B/C/D",
            "A/B",
            "A",
            "B",
            "C"
        ]
    }, {
        "query": "B/C",
        "operator": "~",
        "matches": [
            "A/B/C",
            "A/B/C/D",
            "B/C/D",
            "B/C"
        ],
        "no_matches": [
            "A/B",
            "C/D",
            "B",
            "A",
            "C"
        ]
    }, {
        "query": "C",
        "operator": "~",
        "matches": [
            "A/B/C",
            "A/B/C/D",
            "B/C/D",
            "B/C",
            "C/D",
        ],
        "no_matches": [
            "A/B",
            "B",
            "A"
        ]
    }, {
        "query": "Мытая картошка",
        "operator": "~",
        "matches": [
            "Мытая картошка",
            "Овощи на развес/Сырые овощи/Мытая картошка",
            "Сырые овощи/Мытая картошка",
            "Мытая картошка/Сырые овощи",
        ],
        "no_matches": [
            "A/B",
            "Овощи на развес/Сырые овощи/Мытая картошка 2",
            "Овощи на развес/Сырые овощи/Мытая картошка2",
            "Мытая картошка 2",
        ],
    }
]