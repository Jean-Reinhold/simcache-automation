import os
from dotenv import load_dotenv

from simcache_automation.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


class SimcacheRunner:
    def run_with_config(self, simcache_config) -> str:
        """
        Runs the SimCache command with the provided configuration.
        :param simcache_config: A string containing the SimCache configuration.
        :return: Output of the SimCache command as a string.
        """
        command = f"{os.environ.get('PATHS_SIMCACHE')} {simcache_config} 2>&1"
        logger.debug(f"----> Running cache simulation with command: {command}")

        try:
            with os.popen(command) as proc:
                result = proc.read()
            logger.debug(f"----> Read simcache pipe: {result}")
            if "sim: ** simulation statistics **" not in result:
                raise RuntimeError("The simulation failed and no stats where outputed")
        except Exception as e:
            logger.error(f"Exception while running cache sim: {e}")
            raise e

        return self.parse_simcache_output(simcache_output=result)

    def parse_simcache_output(self, simcache_output: str) -> dict[str, float]:
        """
        Parses the output of SimCache command to extract simulation statistics.
        :param simcache_output: A string containing the output of the SimCache command.
        :return: A dictionary with simulation statistics.
        """

        # Finds where the stats begin
        raw_sim_stats = simcache_output.split("sim: ** simulation statistics **")[1]
        parsed_stats = dict()

        # For each stat
        for raw_stat in raw_sim_stats.split("\n"):
            raw_stat = raw_stat.split(" # ")[0]  # Remove explanation comment
            raw_stat = raw_stat.strip()  # Removes tailing spaces
            raw_stat = raw_stat.split(" ")  # Splits by spaces between k and v
            key = raw_stat[0]  # Gets key at the left side
            value = raw_stat[-1]  # gets value at the right side

            if key.startswith("ld"):
                continue

            if all([key, value]):
                parsed_stats[key] = self.cast_to_float_with_k(string=value)

        return parsed_stats

    def cast_to_float_with_k(self, string):
        """
        Converts a string to a float, considering 'k' or 'K' as an indicator of 1000.

        :param string: String to be converted.
        :return: Float representation of the string.
        """
        try:
            if string.lower().endswith("k"):
                return float(string[:-1]) * 1000
            else:
                return float(string)
        except ValueError:
            raise ValueError(
                "Invalid input. The string should be a number or end with 'k'."
            )
