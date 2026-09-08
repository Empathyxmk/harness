#!/usr/bin/env python

import argparse
import urllib
import zipfile
import os
import sys
import requests
import shutil
from requests.exceptions import HTTPError
from filecmp import dircmp

global WP_VERSION_FILE_PATH
global WP_PACKAGE_ARCHIVE_LINK
global IGNORED_WP_DIRS
global WP_FILES
global TEMP_DIR
global verbose

# File that contains the WordPress version number
WP_VERSION_FILE_PATH = "wp-includes/version.php"

# To get a particular version, add its number + .zip, e.g 4.2.1.zip
WP_PACKAGE_ARCHIVE_LINK = "https://wordpress.org/wordpress-"

# To get a plugin add name (words separated by -) + version, e.g.
# photo-gallery.1.4.3.zip
WP_PLUGIN_ARCHIVE_LINK = "https://downloads.wordpress.org/plugin/"

# Url for standard wordpress themes, add theme + version num
# e.g. appointment.2.4.5.zip
WP_THEME_ARCHIVE_LINK = "https://downloads.wordpress.org/theme/"

# Ignore everything below these directories
IGNORED_WP_DIRS = ['wp-content/themes', 'wp-content/uploads']

# Some common files to search for when identifying a WordPress directory
WP_COMMON_FILES = ['wp-login.php', 'wp-blog-header.php',
                   'wp-admin/admin-ajax.php', 'wp-includes/version.php']

# File extensions that may be executed by php processor
PHP_FILE_EXTENSIONS = ('.php', '.phtml', '.php3', '.php4', '.php5', '.phps')

# Directory to hold downloaded files
TEMP_DIR = 'wpa-temp'

# Should info messages be displayed
verbose = False


def msg(msg, error=False):
    """Print a message according to verbosity and error conditions."""
    if error or verbose:
        print(msg)


def open_file(fileName, mode):
    """Open file with mode. Return False on failure."""
    try:
        f = open(fileName, mode)
        return f
    except IOError as e:
        msg("Error opening [%s]: %s" % (fileName, getattr(e, "strerror", str(e))), True)
        return False


def unzip(zippedFile, outPath):
    """Extract all files from a zip archive to a destination directory."""
    newDir = False  # the toplevel directory name in the zipfile
    fh = open_file(zippedFile, 'rb')
    if not fh:
        return False
    with fh:
        try:
            z = zipfile.ZipFile(fh)
            namelist = z.namelist()
            newDir = namelist[0] if namelist else None
            for name in namelist:
                z.extract(name, outPath)
        except RuntimeError as re:
            msg("Error processing zip (RuntimeError): %s" % (re), True)
            return False
        except IOError as ioe:
            msg("Error opening [%s]: %s" % (zippedFile, getattr(ioe, "strerror", str(ioe))), True)
            return False
        except zipfile.BadZipFile:
            msg("Bad zip file: %s" % zippedFile, True)
            return False
    return newDir


def download_file(fileUrl, newFilePath, newFileName):
    """Download a file via HTTP. If verbose is true, show a progress bar"""
    newFile = os.path.join(newFilePath, newFileName)
    if os.path.isfile(newFile):
        msg("ERROR: cannot download %s, file already exists" % newFile, True)
        return False
    try:
        response = requests.get(fileUrl, stream=True)
        response.raise_for_status()
    except HTTPError:
        msg("ERROR: download problem[%s]: %s " % (
                                                getattr(response, "status_code", "?"),
                                                fileUrl), True)
        return False
    else:
        f = open_file(newFile, "wb")
        if not f:
            msg("ERROR: cannot create new file %s" % (newFile), True)
            return False
        with f:
            contentLength = response.headers.get('content-length')
            if (contentLength is None) or (verbose is False):
                f.write(response.content)
            else:
                dl = 0
                contentLength = int(contentLength)
                sys.stdout.write("\r%s [%s]" % (newFileName, ' ' * 50))
                for data in response.iter_content(chunk_size=1024):
                    if data:
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / contentLength)
                        sys.stdout.flush()
                        sys.stdout.write("\r%s [%s%s]" % (
                                                         newFileName,
                                                         '=' * done,
                                                         ' ' * (50-done)))
                print('')  # newline after progress bar
        return True


def search_dir_for_exts(searchDir, exts):
    """Search directory and its sub-directories for files with extensions."""
    foundFiles = set()
    for root, dirs, files in os.walk(searchDir):
        for f in files:
            if f.endswith(exts):
                foundFiles.add(os.path.join(root, f))
    return foundFiles


def is_subdir(child, parent):
    """Return True if child is a sub-directory of parent directory."""
    absPath = os.path.abspath(child)
    absDir = os.path.abspath(parent)
    return absPath.startswith(absDir + os.path.sep)


def ignored_file(f, wpPath):
    """Returns True if a file should be ignored."""
    for excluded in IGNORED_WP_DIRS:
        if os.path.abspath(f).startswith(os.path.abspath(os.path.join(wpPath, excluded))):
            return True
    return False