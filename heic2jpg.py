import os
import errno
import argparse
import time
import subprocess
import shutil


# ############################# Methods ###############################


def create_directory(directory):
    ''' Creates a directory if it does not already exist.
    '''
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def vprint(verbose, *args, **kwargs):
    ''' Prints only if verbose is True.
    '''
    if verbose:
        print(*args, **kwargs)


def convert(inp, outp, quality, rec=False, verbose=False):
    ''' Converts images from HEIC to JPG.

    Args:
        inp: Input file/directory.
        outp: Output file/directory.
        quality: JPG quality in [0, 100]. Default is 90.
        rec: If True, subdirectories are parsed recursively, else
            they are copied.
        verbose: Verbosity. Default = False.
    '''
    if os.path.isfile(inp):
        pre, ext = os.path.splitext(inp)
        if ext.lower() in ['.heic', '.heif']:
            if outp is None:
                outp = pre + '.jpg'
            else:
                assert not os.path.isdir(outp), "Both inp and outp should be files"
                pre, ext = os.path.splitext(outp)
                assert ext.lower() in ['.jpg']
                dirname = os.path.dirname(outp)
                create_directory(dirname)
            vprint(verbose, 'Converting {} into {}'.format(inp, outp))
            subprocess.call('heif-convert -q {} "{}" "{}"'.format(quality, inp, outp), shell=True)
        else:
            outp = inp if outp is None else outp
            vprint(verbose, 'Copying {} directly to {}'.format(inp, outp))
            shutil.copy2(src=inp, dst=outp, follow_symlinks=True)

    elif os.path.isdir(inp):
        if outp is None:
            outp = inp
        else:
            create_directory(outp)
        for name in os.listdir(inp):
            inpath = os.path.join(inp, name)
            outpath = os.path.join(outp, name)
            if os.path.isfile(inpath):
                pre, ext = os.path.splitext(name)
                outpath = os.path.join(outp, pre + '.jpg') if ext.lower() in ['.heic', '.heif'] else outpath
                convert(inpath, outpath, quality, rec, verbose)
            elif os.path.isdir(inpath) and rec:
                convert(inpath, outpath, quality, rec, verbose)
            elif os.path.isdir(inpath) and not rec:
                shutil.copytree(src=inpath, dst=outpath, symlinks=True,
                                ignore_dangling_symlinks=True)
        vprint(verbose, 'Converted directory {} into {}'.format(inp, outp))


# ############################# Entry Point ###############################


if __name__ == '__main__':
    # Initial time
    t_init = time.time()

    # Parse arguments
    parser = argparse.ArgumentParser(description='Convert HEIC image files \
        to JPG format using libheif (see https://github.com/strukturag/libheif/blob/master/examples/heif_convert.cc).')
    parser.add_argument('-d', '--data',
                        help='Input file/directory.')
    parser.add_argument('-o', '--out',
                        help='Output file/directory. Default: Same as \
                            input directory/file with .jpg extension.',
                        default=None)
    parser.add_argument('-rec', '--recursive',
                        help='Recursively process subdirectories if input \
                            is a directory.',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Increase verbosity.',
                        action='store_true')
    parser.add_argument('-q', '--quality',
                        help='Quality of converted file (integer in [0, 100])',
                        type=int, default=90)
    args = parser.parse_args()

    # Convert files from HEIC to JPG
    convert(args.data, args.out, quality=args.quality, rec=args.recursive,
                verbose=args.verbose)

    # Final time
    t_final = time.time()
    print('Progam finished in {} secs.'.format(t_final - t_init))