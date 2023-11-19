import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from simcache_automation.runner import SimcacheRunner
from simcache_automation.experiments import SimcacheExperiment

load_dotenv()


def run_experiment_from_config(config: dict) -> None:
    runner = SimcacheRunner()
    output_directory = f"./data/{config['experiment_name']}"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    experiment = SimcacheExperiment(
        base_config=config["base_config"],
        target_metrics=config["target_metrics"],
        experiment_name=config["experiment_name"],
        runner=runner,
    )

    experiment.run_experiment(config["param_combinations"], output_directory)


def run_experiments_from_json(json_file_path: str) -> None:
    with open(json_file_path, "r") as file:
        experiments_config = json.load(file)

    workers = int(os.environ.get("MAX_WORKERS"))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(run_experiment_from_config, experiments_config)


if __name__ == "__main__":
    run_experiments_from_json(json_file_path=os.environ.get("PATHS_EXPERIMENTS_JSON"))
