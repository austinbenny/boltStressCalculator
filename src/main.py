'''
    This is the main module file for this application. Start here.

'''

# import python packages
import subprocess
import os
import platform


# import modules
from src import input
from src import calculate
from src import post

def main(file_path):

    file = os.path.join(os.getcwd(),file_path)
    jobs = input.parseYML(file) # list of dicts

    # preproces
    # clean up, check, and convert case here

    for case in jobs:
        # pass case to other module to calculate
        bolts, axes = calculate.extract(case)
        # post process
        filepath = post.run(bolts,axes,case)
        try:
            if case['projectInformation']['open_on_completion']:
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', filepath))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(filepath)
                else:                                   # linux variants
                    subprocess.call(('xdg-open', filepath))
        except:
            pass