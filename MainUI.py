import os
import sys
from DynamicsQuantificationScript import DynamicsQuantification
from VideoDynamicsEncoder import DynamicsEncoder
from GUI import start_gui
from Procedures import Procedures as p


if __name__ == '__main__':
    # print(f"Arguments count: {len(sys.argv)}")
    p = p()
    arg_dict = {}
    for i, arg in enumerate(sys.argv):
        if arg.startswith('-'):
            try:
                arg_dict[arg] = sys.argv[i+1]
            except Exception as e:
                pass
        print(f"Argument {i:>6}: {arg}")

    manual_thresholds = None

    if len(sys.argv) > 1 and sys.argv[1] == '-GUI':
        start_gui()
        exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        p.print_help()
        exit(0)
    if len(arg_dict) >= 1:
        if arg_dict.get('-threshold') is not None:
            manual_thresholds = arg_dict['-threshold'].split(',')
            manual_thresholds = int(manual_thresholds[0]), int(manual_thresholds[1])
        else:
            manual_thresholds = None
        if arg_dict.get('-filepath') and arg_dict['-filepath'] is not None:
            file_path = arg_dict['-filepath']
            if file_path == "":
                print("----Wrong usage, to see help pass the '-h' argument----")
            else:
                if arg_dict is not None:
                    p.new_data_procedure(file_path, **arg_dict)
                else:
                    p.new_data_procedure(file_path)

    else:
        print("----No file path detected----\n----Example data selected----")
        p.example_data_procedure()





