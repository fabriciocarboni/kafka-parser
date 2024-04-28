# Kafka Principal Parser

This Python script is designed to parse Kafka principal configurations from YAML files within a specified directory. It checks for specific conditions, such as formatting issues and byte rate limits, and prints commands based on those conditions. This utility is particularly useful for managing Kafka configurations in a scalable and efficient manner.

## Features

- **YAML Parsing**: Load and parse YAML configuration files.
- **Configuration Validation**: Validate `kafkaPrincipal` values for formatting issues.
- **Byte Rate Checking**: Compare `producer_byte_rate` and `consumer_byte_rate` against predefined maximums.
- **Command Generation**: Generate and print shell commands based on the parsed configurations.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later installed on your machine.
- Access to a Unix-like operating system (Linux, macOS) or Windows with a Unix-like terminal environment (e.g., Cygwin, WSL).
- YAML files containing Kafka principal configurations placed in a specific directory.

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone repo
   cd kafka-principal-parser

2. pip install pyyaml

### Usage
To use the script, simply run it with Python, specifying the directory containing your YAML configuration files as an argument:

```
python3 parse_kafka_principal.py
```