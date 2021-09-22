import yaml
import argparse
import rigol
import wfm
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWG400 WFM file writer')
    parser.add_argument('csv_file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    try:
        with args.csv_file as f:
            # parse Rigol csv input file
            pass
    except wfm.FormatError as e:
        print("Format does not follow the known file format.", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit()

    # Read the yaml file
    with open("example.yaml", "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)