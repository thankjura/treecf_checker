like_complex_cases = [
    {
        "query": "A/*/C",
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
    }
]