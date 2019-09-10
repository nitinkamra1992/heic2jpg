# heic2jpg

This is an image conversion tool built on top of libheif (see https://github.com/strukturag/libheif/blob/master/examples/heif_convert.cc) to convert HEIC files to JPG.

## Compatibility
The tool has been written for Ubuntu and tested on Python v3.5 and above but may be compatible with other versions of python too.

## Dependencies
Requires python3 (mostly present by default).

## Usage

The tool can be run as a Python script, e.g.:
```
python3 heic2jpg.py -d <data_dir> -o <out_dir> -m 1000000 -rec -v -resize 50% -quality 50%
```
It supports all arguments for the `imagemagick convert` tool, and additionally the following arguments:
```
-d, --data: Input file/directory
-o, --out: Output file/directory. Default: Same as input directory/file with .jpg extension.
-rec, --recursive: Recursively process subdirectories if input is a directory.
-v, --verbose: Increase verbosity.
-q, --quality: Quality of converted file (integer in [0, 100]). Default = 90.
```

Note that the tool only processes image files with extension `.heic` or `.heif`. All other unsupported files are copied over directly. If `-rec` is not specified, all subdirectories are copied directly to the output directory.