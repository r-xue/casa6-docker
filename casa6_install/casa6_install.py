"""Main module."""

import os
import sys
import glob
import fileinput
import re
import argparse
import subprocess
import copy
import shutil

from wheel.cli import WheelError
from wheel.wheelfile import WheelFile
from wheel.cli.unpack import unpack as whl_unpack

# wheel.prep425tags is gone now: https://github.com/pypa/wheel/pull/346
# from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag

from packaging.tags import interpreter_name as get_abbr_impl
from packaging.tags import interpreter_version as get_impl_ver
from wheel.bdist_wheel import get_abi_tag


#extra_index_url = 'https://casa-pip.nrao.edu/repository/pypi-group/simple'
extra_index_url = 'https://casa-pip.nrao.edu/repository/pypi-casa-release/simple'


def main():
    """Console script function for casa6_install."""
    description = """

casa6_install will download the latest Py36 casatool whl, repack and install it under Py37/38.
Optionally, other casa6 components (casaplotms etc.) can also be installed along the way.
This CLI tools provide a temprory workaround for install casa6 within Py>36 interpreter before the incoming official
support from NRAO. 

Use this with your own risk and full functions of casa6 is not gauraranteed!
tested on macOS10.15 and Ubuntu20.04

"""

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--user',
                        dest="user", action="store_true",
                        help="pass --user to pip")
    parser.add_argument('-u', '--upgrade',
                        dest="upgrade", action="store_true",
                        help="pass --upgrade to pip")
    parser.add_argument('--no-deps', '--no-dependencies',
                        dest="nodeps", action="store_true",
                        help="pass --non-deps to pip")
    parser.add_argument('-c', '--core',
                        dest="core", action="store_true",
                        help="""only install casatools/casatasks
by default, most casa6 components will be installed: 
    casatools,casatask,casashell,casaplotms, etc,
    some of which might not work properly yet""")

    parser.add_argument('-d', '--dir', type=str,
                        dest="workdir", help='select working directory (instead of the default /tmp')

    args = parser.parse_args()
    print("check your platform:")
    platform = '{}{}-{}'.format(get_abbr_impl(), get_impl_ver(), get_abi_tag())
    print('  {}'.format(sys.executable))
    print('  {}'.format(platform))

    if args.workdir is None:
        workdir = '/tmp'
    else:
        workdir = args.workdir

    whl_path = download_casatools(version='latest', workdir='/tmp')
    casatools_path = casatools_repack(whl_path, abi=None, workdir='/tmp')
    if args.core == True:
        select = 'core'
    else:
        select = 'full'
    casa6_install(casatools_path, select=select,
                  user=args.user, upgrade=args.upgrade, nodeps=args.nodeps)

    return 0


def run_subprocess(cmd):
    """
    run a subprocess with realtime output
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = []
    while True:
        line = process.stdout.readline().rstrip()
        if process.poll() is not None:
            break
        if line:
            print(line.decode())
            output.append(line.decode())
    rc = process.poll()
    return rc, output


def download_casatools(version='latest', workdir='/tmp'):
    """
    download py36 casatools whl 
    """
    packagename = 'casatools'
    if version != 'latest':
        packagename += '=='+version

    cmd = sys.executable
    cmd += ' -m pip download'
    cmd += ' -d '+workdir
    cmd += ' --python-version 36'
    cmd += ' --abi cp36m'
    cmd += ' --no-deps'
    cmd += ' --extra-index-url '+extra_index_url
    cmd += ' '+packagename
    print('exe: {}'.format(cmd))
    rc, output = run_subprocess(cmd)

    pattern1 = 'File was already downloaded'
    pattern2 = 'Saved'
    logs = [x for x in output
            if re.search(pattern1+'(.+?).whl|'+pattern2+'(.+?).whl', x)]
    log = logs[-1]
    whlname = log.replace(pattern1, '').replace(pattern2, '').strip()

    return whlname


def casatools_repack(whlname, abi=None, workdir='/tmp'):
    """
    repack a Py37 casatools whl for Py37/38

    Usage:
        casatools_repack(casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl,abi='cp38')
        casatools_repack(casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl,abi='cp37m')
    """

    if abi is None:
        abi = get_abi_tag()
    if abi == 'cp36m':  # do nothing them
        return whlname

    # Step 1:	wheel unpack .whl
    #	https://github.com/pypa/wheel/blob/master/src/wheel/cli/unpack.py

    whl_unpack(whlname, dest=workdir)
    wf = WheelFile(whlname)
    namever = wf.parsed_filename.group('namever')
    dirname = os.path.join(workdir, namever)

    # Step 2:	modify the casacore library file (.so) names

    flist = glob.glob(dirname+'/casatools/__casac__/*-36m-*', recursive=True)

    for filename in flist:
        newfilename = filename.replace('-36m-', '-'+abi.replace('cp', '')+'-')
        print('Rename {} to {}'.format(filename, newfilename))
        shutil.move(filename, newfilename)

    # Step 3: rename the function keyword "async" to "isasync"

    pyfile = dirname+'/casatools/imager.py'
    print('rename the kwarg "async" in {}'.format(pyfile))
    with fileinput.FileInput(pyfile, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(', async=', ', isasync=').replace(
                ': async', ': isasync'), end='')

    # Step 4: modify the .whl tag within .dist-info/WHEEL

    pyfile = dirname+'/'+namever+'.dist-info/WHEEL'
    dict_oldname = wf.parsed_filename.groupdict()
    dict_newname = copy.deepcopy(dict_oldname)

    dict_newname['pyver'] = '{}{}'.format(get_abbr_impl(), get_impl_ver())
    dict_newname['abi'] = abi

    print('change "tag" in {}'.format(pyfile))
    with fileinput.FileInput(pyfile, inplace=True, backup='.bak') as file:
        oldtag = '{pyver}-{abi}-{plat}'.format(**dict_oldname)
        newtag = '{pyver}-{abi}-{plat}'.format(**dict_newname)
        for line in file:
            print(line.replace(oldtag, newtag), end='')

    # Step 5: repack: whl: wheel pack *

    whl_path = whl_pack(dirname, workdir, None)

    return whl_path


def casa6_install(whl_path, select='core', user=True, upgrade=True, nodeps=False):
    """
    install casa6 packages with pip
    """

    package_list = [whl_path]   # used for rxastro/casa6:base
    if select == 'full':        # optional, used for rxastro/casa6:latest
        package_list += ['casatasks', 'casadata', 'casashell', 'casaviewer',
                         'casaplotms', 'casatelemetry']

    cmd = sys.executable
    cmd += ' -m pip install'
    if user == True:
        cmd += ' --user'
    if upgrade == True:
        cmd += ' --upgrade'
    if nodeps == True:
        cmd += ' --no-deps'
    cmd += ' --extra-index-url '+extra_index_url
    cmd += ' '+' '.join(package_list)
    print('exe: {}'.format(cmd))
    rc, output = run_subprocess(cmd)

    return rc, output


def whl_pack(directory, dest_dir, build_number):
    """
    Repack a previously unpacked wheel directory into a new wheel file.

    modified from https://github.com/pypa/wheel/blob/master/src/wheel/cli/pack.py
    with the output whl path returned

    Repack a previously unpacked wheel directory into a new wheel file.
    The .dist-info/WHEEL file must contain one or more tags so that the target
    wheel file name can be determined.
    :param directory: The unpacked wheel directory
    :param dest_dir: Destination directory (defaults to the current directory)
    """

    DIST_INFO_RE = re.compile(
        r"^(?P<namever>(?P<name>.+?)-(?P<ver>\d.*?))\.dist-info$")
    BUILD_NUM_RE = re.compile(br'Build: (\d\w*)$')

    # Find the .dist-info directory
    dist_info_dirs = [fn for fn in os.listdir(directory)
                      if os.path.isdir(os.path.join(directory, fn)) and DIST_INFO_RE.match(fn)]
    if len(dist_info_dirs) > 1:
        raise WheelError(
            'Multiple .dist-info directories found in {}'.format(directory))
    elif not dist_info_dirs:
        raise WheelError(
            'No .dist-info directories found in {}'.format(directory))

    # Determine the target wheel filename
    dist_info_dir = dist_info_dirs[0]
    name_version = DIST_INFO_RE.match(dist_info_dir).group('namever')

    # Read the tags and the existing build number from .dist-info/WHEEL
    existing_build_number = None
    wheel_file_path = os.path.join(directory, dist_info_dir, 'WHEEL')
    with open(wheel_file_path) as f:
        tags = []
        for line in f:
            if line.startswith('Tag: '):
                tags.append(line.split(' ')[1].rstrip())
            elif line.startswith('Build: '):
                existing_build_number = line.split(' ')[1].rstrip()

        if not tags:
            raise WheelError('No tags present in {}/WHEEL; cannot determine target wheel filename'
                             .format(dist_info_dir))

    # Set the wheel file name and add/replace/remove the Build tag in .dist-info/WHEEL
    build_number = build_number if build_number is not None else existing_build_number
    if build_number is not None:
        if build_number:
            name_version += '-' + build_number

        if build_number != existing_build_number:
            replacement = ('Build: %s\r\n' % build_number).encode(
                'ascii') if build_number else b''
            with open(wheel_file_path, 'rb+') as f:
                wheel_file_content = f.read()
                if not BUILD_NUM_RE.subn(replacement, wheel_file_content)[1]:
                    wheel_file_content += replacement

                f.truncate()
                f.write(wheel_file_content)

    # Reassemble the tags for the wheel file
    impls = sorted({tag.split('-')[0] for tag in tags})
    abivers = sorted({tag.split('-')[1] for tag in tags})
    platforms = sorted({tag.split('-')[2] for tag in tags})
    tagline = '-'.join(['.'.join(impls), '.'.join(abivers),
                        '.'.join(platforms)])

    # Repack the wheel
    wheel_path = os.path.join(
        dest_dir, '{}-{}.whl'.format(name_version, tagline))
    with WheelFile(wheel_path, 'w') as wf:
        print("Repacking wheel as {}...".format(wheel_path), end='')
        sys.stdout.flush()
        wf.write_files(directory)

    print('OK')

    return wheel_path


if __name__ == '__main__':

    main()
