'''
    This is the main module file for this application. Start here.

'''

# import python packages
import os

# import modules
import inputs
import calculate
import post

file_path = 'inputs.yml'

file = os.path.join(os.getcwd(),file_path)
data = inputs.parseYML(file)

# preproces
# clean up, check, and convert data here

# pass data to other module to calculate
results = calculate.extract(data)

# post process
post.output(results)