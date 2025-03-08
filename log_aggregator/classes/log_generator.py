import random
import datetime
from classes.http_codes import HttpCodes  
from classes.config import LogGeneratorConfig

class LogGenerator:
    """
    Log generator class produces a log file - used to develop and test log aggregator
    """
    def __init__(self, config_path, http_codes = None):
        """
        Initialize LogGenerator using a configuration JSON file
        
        Parameters:
            config_path (str): Path to the JSON configuration file
            http_codes (HttpCodes, optional): An instance of HttpCodes, if not provided a new one is created
        """
        self.config = LogGeneratorConfig(config_path)
        self.file_path = self.config.file_path
        # Allows dependcy injection for HttpCodes
        self.http_codes = http_codes if http_codes is not None else HttpCodes()

    def random_datetime(self):
        """
        Generate a random datetime string between start_unix and end_unix
        
        Returns:
            str: Datetime string in the format YYYY-MM-DDTHH:MM:SS
        """
        random_timestamp = random.randint(self.config.start_unix, self.config.end_unix)
        dt = datetime.datetime.fromtimestamp(random_timestamp)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    def random_datetime_from_base(self, base_timestamp):
        """
        Generate a datetime string near the given base_timestamp
        The traffic_spike_intensity controls the narrowness of the time window
        
        Parameters:
            base_timestamp (int): Base UNIX timestamp for generating a clustered time
        
        Returns:
            str: Datetime string in the format YYYY-MM-DDTHH:MM:SS
        """
        # Calculate the maximum offset based on the traffic spike intensity (lower intensity = larger window)
        offset_max = max(1, int((100 - self.config.traffic_spike_intensity) / 10))
        random_offset = random.randint(0, offset_max)
        ts = base_timestamp + random_offset
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    def random_http_method(self):
        """
        Select a random HTTP method 
        
        Returns:
            str: HTTP method string
        """
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        return random.choice(methods)
    
    def random_url(self):
        """
        Select a random URL 
        
        Returns:
            str: URL string
        """
        return random.choice(self.config.url_list)
    
    def random_request_size_number(self):
        """
        Generate a random request size number within range
        
        Returns:
            int: Random request size
        """
        # Unpack the range tuple and generate a random integer in that interval
        return random.randint(self.config.request_size_range[0], self.config.request_size_range[1])
    
    def random_referrer_url(self):
        """
        Generate a random referrer URL string
        
        Returns:
            str: Referrer URL string with random domain
        """
        # Select a random domain from the referrer list and format the URL
        domain = random.choice(self.config.referrer_list)
        return f"http://{domain}.com"
    
    def random_user_agent(self):
        """
        Select a random user agent
        
        Returns:
            str: User agent string
        """
        return random.choice(self.config.user_agent_list)
    
    def generate_http_code(self, error_spike_active=False):
        """
        Generate an HTTP code 
        If error_spike_active is True then with probability error_spike_intensity return an error code, otherwise return a success code
        
        Parameters:
            error_spike_active (bool): Indicates whether error spike logic should be applied
        
        Returns:
            int: HTTP code
        """
        if error_spike_active:
            # Determine if an error code should be generated based on intensity probability
            if random.randint(1, 100) <= self.config.error_spike_intensity:
                return self.http_codes.get_random_code(types=["client_error", "server_error"])
            else:
                return self.http_codes.get_random_code(types=["success"])
        return self.http_codes.get_random_code(types=["success"])
    
    def generate_line(self, error_spike_active=False, traffic_spike_base_timestamp=None):
        """
        Generate a log line
        
        Parameters:
            error_spike_active (bool): Flag to apply error spike logic when generating the HTTP code
            traffic_spike_base_timestamp (int or None): Optional base timestamp for generating clustered time during a traffic spike
        
        Returns:
            str: A complete log line
        """
        # Determine the timestamp: use clustered time if a traffic base is provided
        if traffic_spike_base_timestamp is not None:
            timestamp = self.random_datetime_from_base(traffic_spike_base_timestamp)
        else:
            timestamp = self.random_datetime()
        
        method = self.random_http_method()
        url = self.random_url()
        code = self.generate_http_code(error_spike_active)
        request_size = self.random_request_size_number()
        referrer = self.random_referrer_url()
        user_agent = self.random_user_agent()
        
        components = [
            timestamp,
            method,
            url,
            str(code),
            str(request_size),
            referrer,
            user_agent
        ]
        return " ".join(components)
    
    def generate_and_save_to_file(self):
        """
        Generate log lines based on the loaded configuration and save them to the output file one by one to avoid high memory use.
        Inserts both error and traffic spikes at random positions within the log.
        """
        # Precompute error spike blocks as tuples (start_index, end_index)
        error_spike_blocks = []
        if (self.config.error_spikes and 
            self.config.error_spike_count > 0 and 
            self.config.line_count > self.config.error_spike_length):
            # Generate random blocks where error spikes should occur
            for i in range(self.config.error_spike_count):
                start = random.randint(0, self.config.line_count - self.config.error_spike_length)
                error_spike_blocks.append((start, start + self.config.error_spike_length))
        
        # Precompute traffic spike blocks as tuples (start_index, end_index, base_timestamp)
        traffic_spike_blocks = []
        if (self.config.traffic_spikes and 
            self.config.traffic_spike_count > 0 and 
            self.config.line_count > self.config.traffic_spike_length):
            # Generate random blocks for traffic spikes along with a base timestamp for clustering
            for i in range(self.config.traffic_spike_count):
                start = random.randint(0, self.config.line_count - self.config.traffic_spike_length)
                base_ts = random.randint(self.config.start_unix, self.config.end_unix)
                traffic_spike_blocks.append((start, start + self.config.traffic_spike_length, base_ts))
        
        # Open the file for writing the log lines
        with open(self.file_path, "w") as file:
            for i in range(self.config.line_count):
                # Check if the current line index falls within any error spike block
                error_active = any(start <= i < end for (start, end) in error_spike_blocks)
                # Check if the current line index falls within any traffic spike block and get the base timestamp
                traffic_base = None
                for (start, end, base_ts) in traffic_spike_blocks:
                    if start <= i < end:
                        traffic_base = base_ts
                        break
                # Generate the log line with the appropriate spike settings
                line = self.generate_line(error_spike_active=error_active, traffic_spike_base_timestamp=traffic_base)
                file.write(line + "\n")
