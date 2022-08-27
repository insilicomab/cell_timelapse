from utils.calc_conflu import calc_conflu
from utils.make_plot import make_plot

import argparse


def run(filename, output):

    conflu_list = calc_conflu(filename, output)

    make_plot(conflu_list)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()

    run(
        filename=args.filename,
        output=args.output
    )
