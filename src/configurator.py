# Python Package imports
from os import path
import argparse
import yaml
import logging
import logging.config

# Local imports
import statics
import alert_msgs

logger = logging.getLogger(__name__)


# Gets the configuration variables from the args namespace and loads additional variables from the default config
def get_configurations(args):
    # Set working directory to top level in directory tree
    cli_dict = vars(args)

    if cli_dict["config"] is not None:
        statics.config_path = cli_dict["config"]
    else:
        cli_dict["config"] = statics.config_path

    with open(cli_dict["config"]) as file:
        file_dict = yaml.load(file, Loader=yaml.FullLoader)

        log_file_path = path.join(path.dirname(path.abspath('')), statics.logger_config_path)
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

    argv = vars(args)
    alert_msgs.config_alert_processor(argv["invalid_data_max_count"], argv["depth_violation_max_count"],
                                      argv["proj_pos_violation_max_count"])
    return argv

