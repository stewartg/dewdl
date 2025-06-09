from datetime import datetime

from dewdl.enums import UDLEnvironment, UDLQueryType
from dewdl.udl_actions import UDLBaseAction


class UDLQuery(UDLBaseAction):
    TIME_MAP = {UDLQueryType.EO_OBSERVATION.value: "obTime"}
    DEFAULT_TIME_KEY = "epoch"

    DEFAULT_MAX_RESULTS = 10000

    def __init__(self, data_endpoint: UDLQueryType, udl_environment: UDLEnvironment) -> None:
        super().__init__(data_endpoint.value, udl_environment.value)
        self._time: str = ""
        self._source: str = ""
        self._max_results: str = f"maxResults={UDLQuery.DEFAULT_MAX_RESULTS}"
        self._descriptor: str = ""

    def after(self, epoch: datetime) -> "UDLQuery":
        time_key = UDLQuery.TIME_MAP.get(self._end_point, UDLQuery.DEFAULT_TIME_KEY)
        epoch_str = epoch.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self._time = f"{time_key}=%3E{epoch_str}"
        return self._regenerate()

    def between(self, start: datetime, end: datetime) -> "UDLQuery":
        time_key = UDLQuery.TIME_MAP.get(self._end_point, UDLQuery.DEFAULT_TIME_KEY)
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self._time = f"{time_key}={start_str}..{end_str}"
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
