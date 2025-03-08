from log_generator import LogGenerator
from log_aggregator import LogAggregator

if __name__ == "__main__":
    # Comment out the follwing 2 lines if you don't need a new log file
    log_generator = LogGenerator(config_path="./log_generator_config.json")
    log_generator.generate_and_save_to_file()

    aggregator = LogAggregator(config_path="./log_aggregator_config.json")
    aggregator.aggregate()

    insights = aggregator.data
    
    print("Requests Per Hour:")
    for time_key, count in insights["time_aggregation"].items():
        print(f"{time_key}: {count["total"]}")
    
    print("\n")

    print("Most Requested Resources:")
    for route, count in insights["most_requested_routes"].items():
        print(f"{route}: {count}")
        
    print("\n")
    
    print("Response Code Distribution:")
    for code, count in insights["response_code_distribution"].items():
        print(f"{code}: {count}")

    print("\n")

    print("Detected Anomalies:")
    spikes = insights.get("spikes", {})
    if spikes:
        for anomaly_type, spike_data in spikes.items():
            for time_key, count in spike_data.items():
                print(f"{time_key}: {count} {anomaly_type}")
    else:
        print("No anomalies detected.")
            