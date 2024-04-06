#!/usr/bin/env python3
import argparse

from jen import StressTester

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="Jen",
            description="Generates test cases given a configuration file."
            )

    parser.add_argument('config_file', help="TOML configuration file.")
    parser.add_argument('test_program', help="Test program.")
    parser.add_argument('ref_program', help="Reference program.")

    args = parser.parse_args()
    tst = StressTester(args.config_file)

    tst.run(args.test_program, args.ref_program)




