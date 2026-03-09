from dewdl.models import Notification


def test_model_validate():
    Notification.model_validate(
        {
            "msgType": "DnD_near_geo",
            "classificationMarking": "U//DS-SSDP-NOTIF",
            "origin": "DnD",
            "source": "SSDP",
            "dataMode": "TEST",
            "msgBody": {
                "name": "DnD.AeroOCAT.062726",
                "tleLine1": "1 90251U          24187.67591642 0.00000000 +15000-1 +00000+0 4 0000",
                "tleLine2": "2 90251   3.4195  62.2389 5166855 300.7814 309.2249  1.00248566    0",
                "geoScore": 5.5,
            },
        }
    )
