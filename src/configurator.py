# Python Package imports
import argparse
import yaml

# Local imports
import statics


def load_config(path, arguments_dict):
    with open(path) as file:
        loaded_dict = yaml.load(file, Loader=yaml.FullLoader)
        print(arguments_dict)

        for arg in loaded_dict:
            if arg in arguments_dict:
                arguments_dict[arg] = loaded_dict[arg]
            else:
                print(f"WARNING: Argument \"{arg}\" in  \"{path}\" not a recognised argument. Proceeding with loading.")

        print(arguments_dict)


def get_configurations(args):
    arg_dict = vars(args)

    if arg_dict["config"] is not None:
        statics.config_path = arg_dict["config"]
    else:
        arg_dict["config"] = statics.config_path

    load_config(statics.config_path, arg_dict)

    for arg_index in arg_dict:
        if arg_dict[arg_index] is None:
            print(arg_dict[arg_index])


def parser_setup():
    parser = argparse.ArgumentParser(description="The Underwater Emergency Warning System (UEWS).")
    parser.add_argument('--ip', type=str, help='IP address that UEWS system should connect to.')
    parser.add_argument('--port', type=int, help='Port number that UEWS system should connect to.')
    parser.add_argument('--ttl', type=int, help='Value in seconds that a TSPI object should be kept alive. ')
    parser.add_argument('--dt', type=int, help='Value in seconds in the future that the position of sub should be '
                                               'calculated.')
    parser.add_argument('--config', type=str, help='Path to configuration file in YAML format. Uses default path when '
                                                   'no path is supplied. (../conifg/conifg.yaml)')
    return parser


def main():
    parser = parser_setup()
    args = parser.parse_args()
    get_configurations(args)


main()
