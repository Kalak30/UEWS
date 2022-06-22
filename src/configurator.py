"""Get configuration data.

Allows for configuration data to be passed in by
A YAML file, or by command line arguments. A YAML
file provides more customization and is easier to
use."""

# Python Package imports
import locale
from os import path
import argparse
import logging
import logging.config
import yaml


# Local imports
import statics

logger = logging.getLogger(__name__)


# Gets the configuration variables from the args namespace and loads additional variables from the default config
def load_conf_file(args):
    """
    Loads additional config variables from the specified config file into the args namespace
    Defaults to "../config/config.yaml if no file given
    :param args namespace object containing args
    :return updated values within args
    """
    cli_dict = vars(args)

    if cli_dict["config"] is not None:
        statics.CONFIG_PATH = cli_dict["config"]
    else:
        cli_dict["config"] = statics.CONFIG_PATH

    with open(cli_dict["config"], mode='r', encoding=locale.getpreferredencoding()) as file:
        file_dict = yaml.load(file, Loader=yaml.FullLoader)

        log_file_path = path.join(path.dirname(path.abspath('')), statics.LOGGER_CONFIG_PATH)
        logging.config.fileConfig(log_file_path)

        for arg in file_dict:
            if arg in cli_dict:
                # Only overwrite the values that have not been specified on command line
                if cli_dict[arg] is None:
                    cli_dict[arg] = file_dict[arg]
            else:
                # Alert params cannot yet be specified on cli
                if arg == "alert_params":
                    for param in file_dict[arg]:
                        cli_dict[param] = file_dict[arg][param]
                else:
                    logger.warning(f" Argument \"{arg}\" in  \"{cli_dict['config']}\" not a recognised argument. "
                                   f"Proceeding with loading.")


def parser_setup():
    """
    Sets arguments that UEWS will use.
    Determines allowable names in the config.yaml file and dictionary keys
    (ex: parser.add_argument('--a') will make the 'a' value valid in the yaml file)
    :returns an argparse parser
    """
    parser = argparse.ArgumentParser(description="The Underwater Emergency Warning System (UEWS).")
    parser.add_argument('--ip', type=str, help='IP address that UEWS system should connect to.')
    parser.add_argument('--port', type=int, help='Port number that UEWS system should connect to.')
    parser.add_argument('--ttl', type=float, help='Value in seconds that a TSPI object should be kept alive. ')
    parser.add_argument('--dt', type=float, help='Value in seconds in the future that the position of submarine '
                                                 'should be calculated.')
    parser.add_argument('--config', type=argparse.FileType('r', encoding='utf-8'),
                        help='Path to configuration file in YAML format. Uses default path when no path is supplied. ('
                             '../conifg/conifg.yaml)')
    parser.add_argument('--debug', action="store_const", dest="loglevel", const=logging.DEBUG,
                        help="Display lots of debug info.")
    parser.add_argument('--verbose', action="store_const", dest="loglevel", const=logging.INFO,
                        help="Display more info")
    return parser


def get_config():
    """
    Uses argparse to get arguments from the command line and then
    loads arguments from a yaml specification.
    :return a dictionary containing keys based on cli argument names
    """
    parser = parser_setup()
    args = parser.parse_args()
    load_conf_file(args)

    argv = vars(args)
    return argv
