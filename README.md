# Usage

```bash
# load samples first
python main.py -v=1 --image_outputs resources/samples/byrd_07.png
```

```json
{
    "attributes": {
        "clef": {
            "sign": "",
            "line": "",
            "octave-change": false
        },
        "key": {
            "mode": null,
            "fifths": 0,
            "cancel": 0
        },
        "time": {
            "beats": 4,
            "beat-type": 4,
            "time-symbol": null
        }
    },
    "measures": [
        {
            "number": 1,
            "attributes": null,
            "objects": [
                {
                    "duration": "quarter",
                    "voice": 0,
                    "type-component": {
                        "type": "rest"
                    },
                    "primitive-component": {
                        "x1": 0,
                        "y1": 0,
                        "x2": 0,
                        "y2": 0
                    }
                },
                {
                    "duration": "quarter",
                    "voice": 0,
                    "type-component": {
                        "type": "note",
                        "pitch": {
                            "step": "c",
                            "alteration": 0,
                            "octave": 4
                        },
                        "is-chord": false,
                        "is-grace": false,
                        "is-dotted": false,
                        "stem": "up",
                        "beam": null,
                        "tie": null

                    },
                    "primitive-component": {
                        "x1": 0,
                        "y1": 0,
                        "x2": 0,
                        "y2": 0
                    }
                }
            ],
            "primitive-component": {
                "x1": 0,
                "y1": 0,
                "x2": 0,
                "y2": 0
            }
        }
    ],
    "primitive-component": {
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0
    }
}

```
