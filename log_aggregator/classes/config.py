import json

class BaseConfig:
    """
    Base configuration class to load a JSON file and provide helper methods for type conversion and validations
    """
    def __init__(self, config_path):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {e}")

    def get_int(self, key, default):
        """
        Retrieve an int value from config
        """
        value = self.config.get(key, default)
        if isinstance(value, str):
            try:
                value = int(value)
            except Exception:
                raise ValueError(f"Configuration key '{key}' must be an int, got invalid string: '{value}'")
        elif not isinstance(value, int):
            raise ValueError(f"Configuration key '{key}' must be an int")
        return value
    
    def get_float(self, key, default):
        """
        Retrieve a float value from config
        """
        value = self.config.get(key, default)
        if isinstance(value, str):
            try:
                value = float(value)
            except Exception:
                raise ValueError(f"Configuration key '{key}' must be a float; got invalid string: '{value}'")
        elif not isinstance(value, (int, float)):
            raise ValueError(f"Configuration key '{key}' must be a float")
        return float(value)

    def get_list(self, key, default):
        """
        Retrieve a list value from config
        """
        value = self.config.get(key, default)
        if not isinstance(value, list):
            raise ValueError(f"Configuration key '{key}' must be a list")
        return value

    def get_bool(self, key, default):
        """
        Retrieve a boolean value from config
        """
        value = self.config.get(key, default)
        if not isinstance(value, bool):
            raise ValueError(f"Configuration key '{key}' must be a boolean")
        return value

    def get_tuple_int_range(self, key, default):
        """
        Retrieve a tuple of two integers from config 
        The value can be provided as a list or tuple, each element is converted to int
        """
        value = self.config.get(key, default)
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"Configuration key '{key}' must be a list or tuple representing a range")
        if len(value) != 2:
            raise ValueError(f"Configuration key '{key}' must have exactly two elements")
        try:
            return (int(value[0]), int(value[1]))
        except Exception as e:
            raise ValueError(f"Both elements in '{key}' must be integers: {e}")

    def get_str(self, key, default):
        """
        Retrieve a string value from config
        """
        value = self.config.get(key, default)
        if not isinstance(value, str):
            raise ValueError(f"Configuration key '{key}' must be a string")
        return value


class LogGeneratorConfig(BaseConfig):
    """
    Config class for the log generator
    Loads settings from a JSON config file and applies defaults if keys are missing
    """
    # Defaults
    DEFAULT_LINE_COUNT = 1000000
    DEFAULT_START_UNIX = 1741392000
    DEFAULT_END_UNIX = 1741416163
    DEFAULT_URL_LIST = ["/index.html", "/news", "/products/123"]
    DEFAULT_REFERRER_LIST = ["example"]
    DEFAULT_USER_AGENT_LIST = ["Mozilla/5.0"]
    DEFAULT_REQUEST_SIZE_RANGE = (100, 10000)
    DEFAULT_ERROR_SPIKES = True
    DEFAULT_TRAFFIC_SPIKES = True
    DEFAULT_ERROR_SPIKE_COUNT = 3
    DEFAULT_TRAFFIC_SPIKE_COUNT = 3
    DEFAULT_ERROR_SPIKE_LENGTH = 1000
    DEFAULT_TRAFFIC_SPIKE_LENGTH = 10000
    DEFAULT_ERROR_SPIKE_INTENSITY = 90
    DEFAULT_TRAFFIC_SPIKE_INTENSITY = 90
    DEFAULT_FILE_PATH = "log.txt"

    def __init__(self, config_path):
        super().__init__(config_path)
        self._validate_and_load()

    def _validate_and_load(self):
        # Numeric validations (ensured to be int)
        self.line_count = self.get_int("line_count", self.DEFAULT_LINE_COUNT)
        self.start_unix = self.get_int("start_unix", self.DEFAULT_START_UNIX)
        self.end_unix = self.get_int("end_unix", self.DEFAULT_END_UNIX)
        
        # List validations
        self.url_list = self.get_list("url_list", self.DEFAULT_URL_LIST)
        self.referrer_list = self.get_list("referrer_list", self.DEFAULT_REFERRER_LIST)
        self.user_agent_list = self.get_list("user_agent_list", self.DEFAULT_USER_AGENT_LIST)
        
        # Tuple range for request size
        self.request_size_range = self.get_tuple_int_range("request_size_range", list(self.DEFAULT_REQUEST_SIZE_RANGE))
        
        # Boolean validations
        self.error_spikes = self.get_bool("error_spikes", self.DEFAULT_ERROR_SPIKES)
        self.traffic_spikes = self.get_bool("traffic_spikes", self.DEFAULT_TRAFFIC_SPIKES)
        
        # Additional numeric validations
        self.error_spike_count = self.get_int("error_spike_count", self.DEFAULT_ERROR_SPIKE_COUNT)
        self.traffic_spike_count = self.get_int("traffic_spike_count", self.DEFAULT_TRAFFIC_SPIKE_COUNT)
        self.error_spike_length = self.get_int("error_spike_length", self.DEFAULT_ERROR_SPIKE_LENGTH)
        self.traffic_spike_length = self.get_int("traffic_spike_length", self.DEFAULT_TRAFFIC_SPIKE_LENGTH)
        self.error_spike_intensity = self.get_int("error_spike_intensity", self.DEFAULT_ERROR_SPIKE_INTENSITY)
        self.traffic_spike_intensity = self.get_int("traffic_spike_intensity", self.DEFAULT_TRAFFIC_SPIKE_INTENSITY)
        
        # File path validation (string)
        self.file_path = self.get_str("file_path", self.DEFAULT_FILE_PATH)


class LogAggregatorConfig(BaseConfig):
    """
    Config class for LogAggregator
    Loads and validates settings from a JSON configuration file
    """
    # Defaults
    DEFAULT_FILE_PATH = "./log.txt"
    DEFAULT_CHUNK_SIZE = 10000
    DEFAULT_MAX_WORKERS = 8
    DEFAULT_TIME_INTERVAL = "hour"
    DEFAULT_SORT_ORDER = "desc"
    ALLOWED_TIME_INTERVALS = {"minute", "hour", "day", "week", "month", "year"}
    ALLOWED_SORT_ORDERS = {"asc", "desc"}
    DEFAULT_TIMING_SPIKE_THRESHOLD = 1.3 
    DEFAULT_ERROR_SPIKE_THRESHOLD = 1.3  

    def __init__(self, config_path):
        super().__init__(config_path)
        self._validate_and_load()

    def _validate_and_load(self):
        # File path validation
        self.file_path = self.get_str("file_path", self.DEFAULT_FILE_PATH)
        
        # Numeric validations
        self.chunk_size = self.get_int("chunk_size", self.DEFAULT_CHUNK_SIZE)
        self.max_workers = self.get_int("max_workers", self.DEFAULT_MAX_WORKERS)
        
        # String validations for time interval and sort order
        self.time_interval = self.config.get("time_interval", self.DEFAULT_TIME_INTERVAL)
        if not isinstance(self.time_interval, str) or self.time_interval not in self.ALLOWED_TIME_INTERVALS:
            raise ValueError(f"time_interval must be one of {self.ALLOWED_TIME_INTERVALS}")
        
        self.sort_order = self.config.get("sort_order", self.DEFAULT_SORT_ORDER)
        if not isinstance(self.sort_order, str) or self.sort_order not in self.ALLOWED_SORT_ORDERS:
            raise ValueError("sort_order must be either 'asc' or 'desc'")
        
        self.timing_spike_threshold = self.get_float("timing_spike_threshold", self.DEFAULT_TIMING_SPIKE_THRESHOLD)
        self.error_spike_threshold = self.get_float("error_spike_threshold", self.DEFAULT_ERROR_SPIKE_THRESHOLD)
