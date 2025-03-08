from log_generator import LogGenerator

if __name__ == "__main__":
    log_generator = LogGenerator(config_path="./log_generator_config.json")
    log_generator.generate_and_save_to_file()