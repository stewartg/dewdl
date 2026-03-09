from datetime import datetime

from dewdl.enums import UDLQueryType
from dewdl.enums._udl_base_data_type import UDLBaseDataType
from dewdl.enums._udl_date_fields import UDLDateFields
from dewdl.udl_actions import UDLBaseAction


class UDLQuery(UDLBaseAction):
    DEFAULT_MAX_RESULTS = 10000

    def __init__(self, udl_data_type: UDLBaseDataType) -> None:
        super().__init__(UDLQueryType[udl_data_type.name].value)
        self.base_data_type = udl_data_type
        self.time_key = UDLDateFields.get(self.base_data_type)
        self.dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        self._time: str = ""
        self._source: str = ""
        self._max_results: str = f"maxResults={UDLQuery.DEFAULT_MAX_RESULTS}"
        self._descriptor: str = ""

    def after(self, epoch: datetime) -> "UDLQuery":
        epoch_str = epoch.strftime(self.dt_format)
        self._time = f"{self.time_key}=%3E{epoch_str}"
        return self._regenerate()

    def before(self, epoch: datetime) -> "UDLQuery":
        epoch_str = epoch.strftime(self.dt_format)
        self._time = f"{self.time_key}=%3C{epoch_str}"
        return self._regenerate()

    def between(self, start: datetime, end: datetime) -> "UDLQuery":
        start_str = start.strftime(self.dt_format)
        end_str = end.strftime(self.dt_format)
        self._time = f"{self.time_key}={start_str}..{end_str}"
        return self._regenerate()

    def with_uuid(self, uuid: str) -> "UDLQuery":
        api = "/".join([self._build_base_url(), uuid])
        self.data = api
        return self

    def from_source(self, source: str) -> "UDLQuery":
        self._source = f"source={source}"
        return self._regenerate()

    def max_results(self, max_results: int) -> "UDLQuery":
        self._max_results = f"maxResults={max_results}"
        return self._regenerate()

    def with_descriptor(self, descriptor: str) -> "UDLQuery":
        self._descriptor = f"descriptor={descriptor}"
        return self._regenerate()

    def _regenerate(self) -> "UDLQuery":
        base_str = self._build_base_url()
        valid_queries = [val for val in [self._time, self._source, self._descriptor, self._max_results] if val]
        query_str = "&".join(valid_queries)
        full_str = "?".join([base_str, query_str])
        self.data = full_str
        return self
