'''
    This is the main module file for this application. Start here.

'''

# import python packages
import os

# import modules
from src import inputs
from src import calculate
from src import post

def main(file_path):

    file = os.path.join(os.getcwd(),file_path)
    data = inputs.parseYML(file)

    # preproces
    # clean up, check, and convert data here

    # pass data to other module to calculate
    results = calculate.extract(data)

    # post process
    post.output(results,data)