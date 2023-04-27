import datetime


def nanosecond_epoch_to_datetime(timestamp) -> datetime.datetime:
    """Convert a protobuf timestamp to datetime."""
    timestamp = int(timestamp)
    seconds = timestamp // 1000000000
    nanoseconds = timestamp % 1000000000
    return datetime.datetime.fromtimestamp(seconds) + datetime.timedelta(microseconds=nanoseconds // 1000)
