import pandas
import numpy
import yaml
import platform
import sys
from datetime import datetime
import os
import matplotlib


def getVersions():

    pckgs = ["pandas", "numpy", "yaml"]

    str = "<pre>"
    str += f"Pandas Version: {pandas.__version__}\n"
    str += f"Numpy Version: {numpy.__version__}\n"
    str += f"Yaml Version: {yaml.__version__}\n"
    str += f"matplotlib Version: {matplotlib.__version__}\n"
    str += "</pre>"

    return str


def getSysInfo():

    now = datetime.now()
    str = "<pre>"
    str += f"OS: {platform.platform()}\n"
    str += f"Python Version: {sys.version}\n"
    str += f'Ran on: {now.strftime("%d/%m/%Y %H:%M:%S")}\n'
    str += "</pre>"

    return str


def createOutDirs(case):

    output_path = case["projectInformation"]["output_dir"]
    f_name = case["projectInformation"]["project_name"]
    output_path = os.path.join(output_path, f_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(), output_path)
    else:
        os.mkdir(output_path)
        output_path = os.path.join(os.getcwd(), output_path)

    return output_path, f_name


def getInpFile(case, output_path):

    f = output_path + "/inputFile.txt"
    with open(f, "w+") as out:
        out.write(yaml.dump(case))

    f = ""
    for k, v in case.items():
        f += f"{k}</br>"
        f += f"    {v}</br>"

    return f
