from datetime import datetime

from mockito import unstub, when  # type: ignore

from dewdl.enums import UDLEnvironment, UDLQueryType
from dewdl.requests import UDLQuery


def test_udl_query_factor():
    eo_str = UDLQuery(UDLQueryType.EO_OBSERVATION, UDLEnvironment.TEST).to_string()
    assert eo_str == "https://test.unifieddatalibrary.com/udl/eoobservation"


def test_after():
    when(UDLQuery)._build_base_url().thenReturn("test_base")
    epoch = datetime(2015, 9, 16)
    eo_str = UDLQuery(UDLQueryType.EO_OBSERVATION, UDLEnvironment.TEST).after(epoch).to_string()
    unstub()
    assert eo_str == "test_base?obTime=%3E2015-09-16T00:00:00.000000Z&maxResults=10000"


def test_between():
    when(UDLQuery)._build_base_url().thenReturn("test_base")
    start = datetime(2015, 9, 16)
    end = datetime(2018, 6, 12)
    eo_str = UDLQuery(UDLQueryType.EO_OBSERVATION, UDLEnvironment.TEST).between(start, end).to_string()
    unstub()
    assert eo_str == "test_base?obTime=2015-09-16T00:00:00.000000Z..2018-06-12T00:00:00.000000Z&maxResults=10000"


def test_with_uuid():
    when(UDLQuery)._build_base_url().thenReturn("test_base")
    eo_str = UDLQuery(UDLQueryType.EO_OBSERVATION, UDLEnvironment.TEST).with_uuid("1234").to_string()
    unstub()
    assert eo_str == "test_base/1234"
