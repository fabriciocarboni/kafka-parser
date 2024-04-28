# -*- coding: utf-8 -*-

import yaml
import re
import os

def parse_kafka_principal(useQuotaBaseDir: str) -> None:
    """
    Parses Kafka principal configurations from YAML files within a specified directory,
    checks for specific conditions, and prints commands based on those conditions.

    Args:
    useQuotaBaseDir (str): The directory path where YAML configuration files are located.

    This function performs the following operations:
    - Finds and loads YAML files from the specified directory.
    - Searches for specific keys within the loaded YAML content.
    - Checks for and corrects formatting issues in kafkaPrincipal values.
    - Compares byte rate values against predefined maximums and constructs command strings accordingly.
    """
    # Predefined keys and maximum byte rate values
    key = "kafkaPrincipal"
    key_producer_byte_rate = "producer_byte_rate"
    key_consumer_byte_rate = "consumer_byte_rate"
    max_producer_byte_rate = 262144
    max_consumer_byte_rate = 262144

    # Check if the directory is not empty and proceed
    if os.listdir(useQuotaBaseDir):
        # List comprehension to filter out YAML files
        yaml_file = [
            file
            for file in os.listdir(useQuotaBaseDir)
            if file.endswith(("yml", "yaml"))
        ]

        # Process each YAML file found
        for f in yaml_file:
            with open(useQuotaBaseDir + f, "r") as f:
                try:
                    yml = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(e)

        def findkeys(node: Union[dict, list], kv: str) -> Generator[Any, None, None]:
            """
            A generator function to find values associated with a given key in a nested data structure.

            Args:
            node (dict or list): The data structure to search through.
            kv (str): The key to search for.

            Yields:
            The value associated with the given key.
            """
            if isinstance(node, list):
                for i in node:
                    for x in findkeys(i, kv):
                        yield x
            elif isinstance(node, dict):
                if kv in node:
                    yield node[kv]
                for j in node.values():
                    for x in findkeys(j, kv):
                        yield x

    # Find and list all kafkaPrincipal items in the YAML file
    kafka_principal_items = list(findkeys(yml, key))

    # Check and correct formatting in kafkaPrincipal values
    for item in kafka_principal_items:
        # Look for spaces after any comma
        match = re.search(r", ", item)
        if match:
            print(f"[WARNING] There are spaces after comma in {key} parameter, please update it")
            clean_spaces = item.replace(", ", ",")
            print(f"[WARNING] it should be like this => {clean_spaces}\n")

    # Find and list byte rate items in the YAML file
    producer_byte_rate_items = list(findkeys(yml, key_producer_byte_rate))
    consumer_byte_rate_items = list(findkeys(yml, key_consumer_byte_rate))

    # Loop through both lists, compare byte rates, and print commands
    for (producer_byte_rate, consumer_byte_rate) in zip(producer_byte_rate_items, consumer_byte_rate_items):
        # Compare and set byte rates based on maximum allowed values
        set_producer_byte_rate = max_producer_byte_rate if int(producer_byte_rate) >= max_producer_byte_rate else producer_byte_rate
        set_consumer_byte_rate = max_consumer_byte_rate if int(consumer_byte_rate) >= max_consumer_byte_rate else consumer_byte_rate

        # Construct and print the command
        cmd = (
            f"kafka-configs.sh  --zookeeper localhost:2181 --alter --add-config 'producer_byte_rate="
            f"{set_producer_byte_rate},consumer_byte_rate={set_consumer_byte_rate}' --entity-type users --entity-name '$userPrinciple'"
        )
        print(cmd)

if __name__ == "__main__":
    # Define the base directory for Kafka YAML configurations
    useQuotaBaseDir = "/home/fabricio/Documents/kafka-parser/"
    # Alternative path example (commented out)
    # useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    # Call the main function
    parse_kafka_principal(useQuotaBaseDir) # type: ignore
    