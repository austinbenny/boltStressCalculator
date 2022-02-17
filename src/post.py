import os

def writeCSV(data,output_path):
    
    f_name = 'bolts_structural_parameters.csv'
    data.to_csv(os.path.join(output_path,f_name),sep=',',float_format='%.3f',index_label='Bolts')

def output(data):

    output_path = 'build'
    if os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(),output_path)
    else:
        os.mkdir(output_path)
        output_path = os.path.join(os.getcwd(),output_path)

    writeCSV(data,output_path)
