from enum import Enum


class UDLSecureMessageType(Enum):
    TOPICS = "sm/listTopics"
    DESCRIBE_TOPIC = "sm/describeTopic"
    LATEST_OFFSET = "sm/getLatestOffset"
    MESSAGES = "sm/getMessages"
