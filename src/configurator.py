# Python Package imports
from os import path
import argparse
import yaml
import logging
import logging.config

# Local imports
import statics

logger = logging.getLogger(__name__)


# Gets the configuration variables from the args namespace and loads additional variables from the default config
def get_configurations(args):
    # Set working directory to top level in directory tree
    arg_dict = vars(args)

    if arg_dict["config"] is not None:
        statics.config_path = arg_dict["config"]
    else:
        arg_dict["config"] = statics.config_path

    with open(arg_dict["config"]) as file:
        loaded_dict = yaml.load(file, Loader=yaml.FullLoader)

        log_file_path = path.join(path.dirname(path.abspath('')), statics.logger_config_path)
        logging.config.fileConfig(log_file_path)

        for arg in loaded_dict:
            if arg in arg_dict:
                # Only overwrite the values that have not been specified on command line
                if arg_dict[arg] is None:
                    arg_dict[arg] = loaded_dict[arg]
            else:
                logger.warning(f" Argument \"{arg}\" in  \"{arg_dict['config']}\" not a recognised argument. Proceeding "
                               f"with loading.")


def parser_setup():
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
    parser = parser_setup()
    args = parser.parse_args()
    get_configurations(args)
    return args


if __name__ == "__main__":
    get_config()
