# CSV to AWG430

## Supported Manufacturers:
1. rigol
2. lecroy
3. rohde

## Specify an input file:
`python csv_to_awg430.py [filename] [manufacturer]`

The output filename is the same as the input filename with a ".wfm" file extension.

## Specify an input and an output file:
`python csv_to_awg430.py [filename] [manufacturer] --output [output filename]`

This uses the specified output filename.

## Plot the data from the Rigol file to verify it's correct
`python csv_to_awg430.py [filename] [manufacturer] --plot`
