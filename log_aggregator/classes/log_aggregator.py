import concurrent.futures
from datetime import datetime, timedelta
import statistics
from classes.http_codes import HttpCodes
from classes.config import LogAggregatorConfig

class LogAggregator:
    """
    Aggregates log file data by processing log chunks in parallel
    """
    def __init__(self, config_path, http_codes = HttpCodes()):
        """
        Initialize the LogAggregator class
        
        Parameters:
            config_path (str): Path to the config file
            http_codes (HttpCodes, optional): An instance of HttpCodes, if not provided a new one is created
        """
        self.config = LogAggregatorConfig(config_path)
        # Allows dependcy injection for HttpCodes
        self.http_codes = http_codes if http_codes is not None else HttpCodes()
        self._aggregated_data = {}

    def get_time_key(self, timestamp):
        """
        Extract a time key from a timestamp based on the aggregation interval
        The expected timestamp format is "YYYY-MM-DDTHH:MM:SS"
        The key is the timestamp of the start of the bucket
        
        Parameters:
            timestamp (str): Timestamp string in the format YYYY-MM-DDTHH:MM:SS
        
        Returns:
            int: timestamp representing the start of the time bucket
        
        Raises:
            ValueError: If an unsupported time interval is specified
        """
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        if self.config.time_interval == "minute":
            dt_floored = dt.replace(second=0, microsecond=0)
        elif self.config.time_interval == "hour":
            dt_floored = dt.replace(minute=0, second=0, microsecond=0)
        elif self.config.time_interval == "day":
            dt_floored = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.config.time_interval == "week":
            # Floor to the most recent Sunday
            offset = (dt.weekday() + 1) % 7
            dt_floored = dt - timedelta(days=offset)
            dt_floored = dt_floored.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.config.time_interval == "month":
            dt_floored = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif self.config.time_interval == "year":
            dt_floored = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError("Unsupported time interval")
        return int(dt_floored.timestamp())

    def process_chunk(self, chunk):
        """
        Process a list of log lines and aggregate metrics per time bucket
        Tracks total requests, error counts, most requested routes, and response code distribution
        
        Parameters:
            chunk (List[str]): List of log lines
        
        Returns:
            dict: Aggregation dict:
                {
                    "time_aggregation": {
                        <time_bucket_key>: {"total": int, "errors": int},
                        ...
                    },
                    "most_requested_routes": {<route>: count, ...},
                    "response_code_distribution": {<code>: count, ...}
                }
        """
        aggregation = {
            "time_aggregation": {},
            "most_requested_routes": {},
            "response_code_distribution": {}
        }

        for line in chunk:
            parts = line.strip().split()
            if len(parts) < 4:
                continue

            timestamp, _, route, code = parts[:4]
            key = self.get_time_key(timestamp)
            code_int = int(code)

            # Initialize the time bucket if necessary
            if key not in aggregation["time_aggregation"]:
                aggregation["time_aggregation"][key] = {"total": 0, "errors": 0}

            aggregation["time_aggregation"][key]["total"] += 1
            if self.http_codes.code_is_error(code_int):
                aggregation["time_aggregation"][key]["errors"] += 1

            # Update most requested routes
            aggregation["most_requested_routes"][route] = aggregation["most_requested_routes"].get(route, 0) + 1

            # Update response code distribution
            aggregation["response_code_distribution"][code] = aggregation["response_code_distribution"].get(code, 0) + 1

        return aggregation

    def merge_aggregations(self, base, new):
        """
        Merge two aggregation dictionaries
        
        Parameters:
            base (dict): The base aggregation dictionary
            new (dict): The new aggregation dictionary to merge
        
        Returns:
            dict: The merged aggregation dictionary
        """
        # Merge time_aggregation
        for ts, counts in new.get("time_aggregation", {}).items():
            if ts not in base["time_aggregation"]:
                base["time_aggregation"][ts] = counts
            else:
                base["time_aggregation"][ts]["total"] += counts["total"]
                base["time_aggregation"][ts]["errors"] += counts["errors"]

        # Merge most_requested_routes
        for route, count in new.get("most_requested_routes", {}).items():
            base["most_requested_routes"][route] = base["most_requested_routes"].get(route, 0) + count

        # Merge response_code_distribution
        for code, count in new.get("response_code_distribution", {}).items():
            base["response_code_distribution"][code] = base["response_code_distribution"].get(code, 0) + count

        return base

    def aggregate(self):
        """
        Aggregate log data using multiprocessing
        Heavier on memory than multithreading, but multithreading in Python does not play well with heavy CPU load tasks
        
        Returns:
            dict: final aggregation data:
                {
                    "time_aggregation": {
                        <timestamp_str>: {"total": int, "errors": int},
                        ...
                    },
                    "most_requested_routes": {<route>: count, ...},
                    "response_code_distribution": {<code>: count, ...},
                    "spikes": {"requests": {...}, "errors": {...}} 
                }
        """
        aggregated = {
            "time_aggregation": {},
            "most_requested_routes": {},
            "response_code_distribution": {}
        }
        futures = []

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
            with open(self.config.file_path, "r") as f:
                chunk = []
                for line in f:
                    chunk.append(line)
                    if len(chunk) >= self.config.chunk_size:
                        futures.append(executor.submit(self.process_chunk, chunk))
                        chunk = []
                if chunk:
                    futures.append(executor.submit(self.process_chunk, chunk))

            for future in concurrent.futures.as_completed(futures):
                try:
                    aggregated = self.merge_aggregations(aggregated, future.result())
                except Exception as e:
                    #  Would pass this error to a logging class in a real life scenario
                    print(f"Error merging aggregation: {e}")

        # Sort the time buckets based on the sort order defined in the config
        time_agg = aggregated.get("time_aggregation", {})
        reverse_sort = (self.config.sort_order.lower() == "desc")
        sorted_time_items = sorted(time_agg.items(), key=lambda x: x[0], reverse=reverse_sort)

        sorted_time_agg = {
            datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S"): data
            for ts, data in sorted_time_items
        }

        self._aggregated_data = {
            "time_aggregation": sorted_time_agg,
            "most_requested_routes": aggregated["most_requested_routes"],
            "response_code_distribution": aggregated["response_code_distribution"]
        }

        self.detect_spikes()
        return self._aggregated_data

    def detect_spikes(self):
        """
        Detect spikes in total requests and errors per time bucket
        
        Returns:
            dict: spike data:
                {
                    "requests": {
                        <timestamp_str>: int,
                        ...
                    },
                    "errors": {
                        <timestamp_str>: int,
                        ...
                    },
                }
        
        Raises:
            ValueError: If no aggregated data is available
        """

        time_agg = self._aggregated_data.get("time_aggregation", {})
        if not time_agg:
            return {}

        total_requests = [data.get("total", 0) for data in time_agg.values()]
        total_errors = [data.get("errors", 0) for data in time_agg.values()]

        if not total_requests:
            return {}

        request_average = statistics.mean(total_requests)
        error_average = statistics.mean(total_errors) if any(total_errors) else 0

        spikes = {"requests": {}, "errors": {}}

        for time_bucket, data in time_agg.items():
            total = data.get("total", 0)
            errors = data.get("errors", 0)

            if total > request_average * self.config.timing_spike_threshold:
                spikes["requests"][time_bucket] = total
            if errors > error_average * self.config.error_spike_threshold:
                spikes["errors"][time_bucket] = errors

        self._aggregated_data["spikes"] = spikes
        return spikes

    @property
    def data(self):
        """
        Get the aggregated data
        
        Returns:
            dict: The aggregated log data
        """
        return self._aggregated_data
