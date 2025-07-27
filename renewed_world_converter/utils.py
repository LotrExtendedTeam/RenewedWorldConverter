# extended_world_converter/utils.py
import os
import sys
import shutil
import tempfile
from .settings import JAR_NAME, CONVERSIONS_FILE, TEMP_PREFIX

def get_temp_work_dir():
    """
    Create a unique temp working directory.
    """
    return tempfile.mkdtemp(prefix=TEMP_PREFIX)

def get_bundle_dir():
    """
    For PyInstaller: sys._MEIPASS is the extracted temp folder.
    For normal dev: fallback to current dir.
    """
    return getattr(sys, "_MEIPASS", os.path.abspath("."))

def extract_resources(temp_dir):
    """
    Copy the JAR and Conversions.json into the temp working directory.
    Returns absolute paths to the copied JAR and JSON.
    """
    bundle_dir = get_bundle_dir()
    jar_src = os.path.join(bundle_dir, JAR_NAME)
    conv_src = os.path.join(bundle_dir, CONVERSIONS_FILE)

    jar_dst = os.path.join(temp_dir, JAR_NAME)
    conv_dst = os.path.join(temp_dir, CONVERSIONS_FILE)

    shutil.copy(jar_src, jar_dst)
    shutil.copy(conv_src, conv_dst)

    return jar_dst, conv_dst