from dewdl.models import Elset


def test_model_validate():
    Elset.model_validate(
        {
            "epoch": "2024-07-05T16:13:19.178688Z",
            "classificationMarking": "U//DS-SSDP-ELSET",
            "meanMotion": 1.00248566,
            "eccentricity": 0.5166855,
            "inclination": 3.4195,
            "raan": 62.2389,
            "argOfPerigee": 300.7814,
            "meanAnomaly": 309.2249,
            "ephemType": 4,
            "revNo": 0,
            "source": "SSDP",
            "origin": "DnD",
            "dataMode": "TEST",
            "agom": 0.015,
            "ballisticCoeff": 0.0,
            "algorithm": '{"score": 10.0, "mv": 11.85, "rms": 3.2}',
            "origObjectId": "DnD.AeroOCAT.062726",
            "uct": True,
            "tags": ["dnd_catalog"],
            "descriptor": "test.zip",
        }
    )
