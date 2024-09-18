from dewdl.models.notifications._base_notification import BaseNotification
from dewdl.models.notifications._dnd_near_geo_body import DNDNearGeoBody


class DNDNearGeoNotification(BaseNotification):
    msgBody: DNDNearGeoBody  # type: ignore
