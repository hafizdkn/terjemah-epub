import configparser
import ast


class ReadConfig:
    def __init__(self, config_file):
        self._parser = configparser.ConfigParser()
        self._parser.read(config_file)

    def read_config(self, section, key):
        return self._parser[section][key]

    def get_value(self, section, key):
        rest = self._parser.get(section, key)
        if section == "Path":
            return rest

        return ast.literal_eval(self._parser.get(section, key))
