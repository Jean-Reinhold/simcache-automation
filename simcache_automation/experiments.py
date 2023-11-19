import plotly.graph_objects as go
import plotly.io as pio
import json
import os
from typing import Any

from simcache_automation.logger import get_logger

logger = get_logger(__name__)


class SimcacheExperiment:
    def __init__(
        self, base_config: str, target_metrics: list[str], experiment_name: str, runner
    ):
        self.base_config = base_config
        self.target_metrics = target_metrics
        self.runner = runner
        self.experiment_name = experiment_name
        self.results = []
        logger.info("SimcacheExperiment initialized")

    def generate_configs(self, param_combinations: list[dict[str, Any]]) -> list[str]:
        logger.debug("Generating configurations")
        configs = [
            self.base_config.format(**combination) for combination in param_combinations
        ]
        return configs

    def run_simulations(self, configs: list[str]):
        logger.info("Running simulations")
        for config in configs:
            logger.debug(f"Running simulation with config: {config}")
            stats = self.runner.run_with_config(config)
            self.results.append(stats)
        logger.info("Simulations completed")

    def extract_metrics(self) -> dict[str, list[Any]]:
        logger.debug("Extracting metrics")
        extracted_data = {metric: [] for metric in self.target_metrics}
        for result in self.results:
            for metric in self.target_metrics:
                extracted_data[metric].append(result.get(metric, None))
        return extracted_data

    def save_metrics_to_json(self, data: dict[str, Any], directory: str):
        filepath = os.path.join(directory, self.experiment_name + ".json")
        logger.info(f"Saving metrics to JSON file: {filepath}")
        with open(filepath, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def plot_bar_chart(
        self,
        data: dict[str, list[Any]],
        x_values: list[str],
        title: str,
        directory: str,
    ):
        logger.info("Plotting bar chart")
        fig = go.Figure()
        for metric, values in data.items():
            fig.add_trace(go.Bar(x=x_values, y=values, name=metric))

        fig.update_layout(title=title, xaxis_title="Configuration", yaxis_title="Value")
        filepath = os.path.join(directory, self.experiment_name + "_bar.png")
        logger.info(f"Saving bar chart as PNG: {filepath}")
        pio.write_image(fig, filepath, format="png", width=1600, height=900)

    def plot_lines(
        self,
        data: dict[str, list[Any]],
        x_values: list[str],
        title: str,
        directory: str,
    ):
        logger.info("Plotting lines")
        fig = go.Figure()
        for metric, values in data.items():
            fig.add_trace(
                go.Scatter(x=x_values, y=values, mode="lines+markers", name=metric)
            )

        fig.update_layout(title=title, xaxis_title="Configuration", yaxis_title="Value")
        filepath = os.path.join(directory, self.experiment_name + "_lines.png")
        logger.info(f"Saving plot as PNG: {filepath}")
        pio.write_image(fig, filepath, format="png", width=1600, height=900)

    def run_experiment(self, param_combinations: list[dict[str, Any]], directory: str):
        logger.info("Experiment started")
        configs = self.generate_configs(param_combinations)
        self.run_simulations(configs)
        metrics_data = self.extract_metrics()

        self.save_metrics_to_json(metrics_data, directory)

        x_values = [str(combination) for combination in param_combinations]

        self.plot_lines(metrics_data, x_values, self.experiment_name, directory)
        self.plot_bar_chart(
            metrics_data, x_values, self.experiment_name + " Bar Chart", directory
        )
        logger.info("Experiment completed")
