eq_simple_cases = [
    {
        "query": "A/B/C",
        "operator": "=",
        "matches": [
            "A/B/C",
        ],
        "no_matches": [
            "A/B/D",
            "B/C/D",
            "A/B",
            "A",
            "B",
            "C",
            "A/B/C/D",
        ]
    }, {
        "query": "B/C",
        "operator": "=",
        "matches": [
            "B/C"
        ],
        "no_matches": [
            "A/B",
            "C/D",
            "B",
            "A",
            "C",
            "A/B/C",
            "A/B/C/D",
            "B/C/D",
        ],
    }, {
        "query": "C",
        "operator": "=",
        "matches": [
            "C",
            "A/B/C",
        ],
        "no_matches": [
            "A/B",
            "C/D",
            "B",
            "A",
            "A/B/C/D",
            "B/C/D",
        ],
    }
]
