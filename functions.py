# Import third-party modules
import maya.cmds as cmds
import pymel.core as pmc
import maya.mel as mel
import tempfile
import os
import main

import subprocess

EXPORT_PATH = ""
CHECK_LIST = {"Saving to Temp File" : 0, "Parent to World" : 1, "Fetch Geometry" : 2, "Delete History" : 3, "Freeze Transforms" : 4,
              "Apply Lambert1" : 5}

def kill_existing_app(windowName):
    """Kill the app if it's running.

    Args:
        windowName (str): Window object name of the app.
    """
    if cmds.window(windowName, exists=True, q=True):
        cmds.deleteUI(windowName)

def show_help():

    help_path = "T:/david.waldhaus/documentation/fixPref/fixPref_documentation.pdf"

    subprocess.Popen(help_path, shell=True)

def build_default_export_path():
    scene_dir = os.path.dirname(pmc.sceneName())
    export_dir = os.path.join(scene_dir, "_export", "mdl")
    export_path = os.path.join(export_dir, pmc.sceneName())
    return export_dir

def is_group(node):
    try:
        children = node.getChildren()
        for child in children:
            if type(child) is not pmc.nodetypes.Transform:
                return False
        return True
    except:
        return False


def get_and_validate_sel():

    sel = pmc.ls(sl=1)
    if not sel:
        pmc.warning("Please select a root group!")
        return
    if len(sel) > 1:
        pmc.warning("Please select only a single root group!")
        return
    else:
        sel = sel[0]
    if not is_group(sel):
        pmc.warning("Please select a root group!")
        return

    return sel, str(sel)


def parent_to_world(obj):
    try:
        pmc.parent(obj, world=True)
        return True
    except:
        return False

def get_geo_from_sel(obj):
    childs = pmc.listRelatives(obj, ad=True)
    transforms = [x for x in childs if x.nodeType() == "transform"]
    meshes = [x.getTransform() for x in childs if x.nodeType() == "mesh"]
    if meshes and transforms:
        return meshes, transforms, True
    else:
        return None, None, False


def save_current_scene():
    original_file = None
    original_file = pmc.saveFile()
    if original_file:
        return original_file, True
    else:
        return None, False

def save_as_temp_file():
    # get temp dir
    try:
        tmp_dir = tempfile.gettempdir()
        scene_name = "NO_WORKFILE.ma"
        tmp_file = os.path.join(tmp_dir, scene_name)
        pmc.renameFile(tmp_file)
        pmc.saveFile()
        return True
    except:
        return False

def delete_history(obj_list):
    try:
        for obj in obj_list:
            pmc.delete(ch=True)
        return True
    except:
        return False


def freeze_transformations(obj_list):
    try:
        for obj in obj_list:
            pmc.makeIdentity(apply=True, t=1, r=1, s=1)
        return True
    except:
        return False

def assign_lambert(obj_list):
    try:
        for obj in obj_list:
            pmc.hyperShade(obj, a="lambert1")
        return True
    except:
        return False


