'''
    This is the main module file for this application. Start here.

'''

# import python packages
import subprocess
import os
import platform


# import modules
from src import inputs
from src import calculate
from src import post

def main(file_path):

    file = os.path.join(os.getcwd(),file_path)
    case = inputs.parseYML(file)

    # preproces
    # clean up, check, and convert case here

    # pass case to other module to calculate
    bolts, axes = calculate.extract(case)

    # post process
    filepath = post.output(bolts,axes,case)
    if case['projectInformation']['open_on_completion']:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))