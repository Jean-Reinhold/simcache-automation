# Simcache Automation

Simcache Automation is a tool designed for running a series of cache simulation experiments using SimcacheRunner with different configurations and auto generating series of data, line plots and bar plots.

## Getting Started

These instructions will guide you on how to set up and run the Simcache Automation tool on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose
- Python 3.8 or higher (if running outside Docker)

### Installation

1. **Clone the Repository**

   ```bash
   git clone [URL to the simcache_automation repository]
   cd simcache_automation

2. **Build and Run with Docker Compose**

This project uses Docker Compose to simplify building and running:

```bash
docker-compose up --build
```

## Setting Up and Running Experiments

Simcache Automation uses a JSON configuration file, experiments.json, to define and run a series of cache simulation experiments.

## Structure of experiments.json

The experiments.json file contains an array of experiment objects. Each object should have the following fields:

**base_config**: The base configuration string for the simulation, containing placeholders for parameters.

**target_metrics**: A list of metrics you want to extract from the simulation results.

**experiment_name**: A unique name for the experiment, used for naming output files and directories.

**param_combinations**: An array of objects, each representing a set of parameter values.

**output_directory**: The directory where results for this experiment will be stored.

```json
[
    {
        "base_config": "-cache:il1 il1:64:64:{il1_assoc}:l -cache:dl1 dl1:64:64:{dl1_assoc}:l benchmarks/gcc/cc1.ss benchmarks/gcc/gcc.i",
        "target_metrics": ["il1.miss_rate", "dl1.miss_rate"],
        "experiment_name": "Experiment1",
        "param_combinations": [
            {"il1_assoc": 8, "dl1_assoc": 8},
            {"il1_assoc": 16, "dl1_assoc": 16}
        ],
        "output_directory": "./data/experiment1"
    },
    {
        "base_config": "-cache:il1 il1:32:32:{il1_assoc}:l -cache:dl1 dl1:32:32:{dl1_assoc}:l benchmarks/gcc/cc1.ss benchmarks/gcc/gcc.i",
        "target_metrics": ["il1.miss_rate", "dl1.miss_rate"],
        "experiment_name": "Experiment2",
        "param_combinations": [
            {"il1_assoc": 4, "dl1_assoc": 4},
            {"il1_assoc": 8, "dl1_assoc": 8}
        ],
        "output_directory": "./data/experiment2"
    }
]

```

## Running the Experiments

Create or Modify experiments.json:

Create or modify the experiments.json file in the root directory of the project based on your simulation requirements.

## Results
Visual Plots: Graphs showing various metrics as PNG files.
JSON Files: Raw metrics data in JSON format.

