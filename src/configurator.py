# Python Package imports
from os import path
import argparse
import yaml
import logging
import logging.config

# Local imports
import statics

logger = logging.getLogger(__name__)


# Loads the configuration data from the YAML file specified at path
# Checks each option specified against valid command line arguments in the arguments_dict
# Updates the arguments_dict to contain the new config values
def load_config(config_path, arguments_dict):
    config_path = path.join(path.dirname(path.abspath('')), config_path)
    with open(config_path) as file:
        loaded_dict = yaml.load(file, Loader=yaml.FullLoader)

        # Use the logger config supplied by cli, or by config file. If neither exist, use default in statics
        if "logger_config" in arguments_dict and arguments_dict["logger_config"] is not None:
            statics.logger_config_path = arguments_dict["logger_config"]
        elif "logger_config" in loaded_dict and loaded_dict["logger_config"] is not None:
            statics.logger_config_path = loaded_dict["logger_config"]
            arguments_dict["logger_config"] = statics.logger_config_path

        log_file_path = path.join(path.dirname(path.abspath('')), statics.logger_config_path)
        logging.config.fileConfig(log_file_path)

        for arg in loaded_dict:
            if arg in arguments_dict:
                # Only overwrite the values that have not been specified on command line
                if arguments_dict[arg] is None:
                    arguments_dict[arg] = loaded_dict[arg]
            else:
                logger.warning(f" Argument \"{arg}\" in  \"{config_path}\" not a recognised argument. Proceeding "
                                f"with loading.")


# Gets the configuration variables from the args namespace and loads additional variables from the default config
def get_configurations(args):
    # Set working directory to top level in directory tree
    arg_dict = vars(args)

    if arg_dict["config"] is not None:
        statics.config_path = arg_dict["config"]
    else:
        arg_dict["config"] = statics.config_path

    load_config(statics.config_path, arg_dict)

    for arg_index in arg_dict:
        if arg_dict[arg_index] is None:
            pass
            #print(arg_dict[arg_index])


def parser_setup():
    parser = argparse.ArgumentParser(description="The Underwater Emergency Warning System (UEWS).")
    parser.add_argument('--ip', type=str, help='IP address that UEWS system should connect to.')
    parser.add_argument('--port', type=int, help='Port number that UEWS system should connect to.')
    parser.add_argument('--ttl', type=float, help='Value in seconds that a TSPI object should be kept alive. ')
    parser.add_argument('--dt', type=float, help='Value in seconds in the future that the position of sub should be '
                                                 'calculated.')
    parser.add_argument('--config', type=argparse.FileType('r', encoding='utf-8'), help='Path to configuration file '
                                                                                        'in YAML format. Uses default '
                                                                                        'path when no path is '
                                                                                        'supplied. ('
                                                                                        '../conifg/conifg.yaml)')
    parser.add_argument('--logger-config', type=argparse.FileType('r', encoding='utf-8'), help='Path to configuration '
                                                                                               'file for the logging '
                                                                                               'module in python.')
    parser.add_argument('--debug', action='store_true')
    return parser


def main():
    parser = parser_setup()
    args = parser.parse_args()
    get_configurations(args)


if __name__ == "__main__":
    main()
