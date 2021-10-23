# Rigol to AWG430


## Specify an input file:
`python rigol_to_awg430.py [filename]`

The output filename is the same as the input filename with a ".wfm" file extension.

## Specify an input and an output file:
`python rigol_to_awg430.py [filename] --output [output filename]`

This uses the specified output filename.

## Plot the data from the Rigol file to verify it's correct
`python rigol_to_awg430.py [filename] --plot`
