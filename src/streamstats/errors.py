class StreamStatsError(Exception):
    pass
class UnsupportedFormatError(StreamStatsError):
    pass
class IncorrectEventError(StreamStatsError):
    pass
class IncorrectTimeStampError(StreamStatsError):
    pass
class ConfigurationOfCLIError(StreamStatsError):
    pass
