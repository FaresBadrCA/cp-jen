from jen import StressTester
import argparse


def run():
    parser = argparse.ArgumentParser(
        prog="Jen",
        description="Generates test cases given a configuration file."
    )

    parser.add_argument('config_file', help="TOML configuration file.")
    parser.add_argument('test_prog', nargs='?',
                        help="The test and reference programs.")
    parser.add_argument('ref_prog', nargs='?',
                        help="The test and reference programs.")
    parser.add_argument('-o', '--output', help="Output test case file name.")
    args = parser.parse_args()
    stress_tester = StressTester(args.config_file)

    if args.test_prog and args.ref_prog:
        stress_tester.run(args.test_prog, args.ref_prog, args.output)
    else:
        stress_tester.single_run(args.output)
