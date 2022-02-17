import os

def writeCSV(results,output_path,f_name):
    
    f_name = f'{f_name}_structural_parameters.csv'
    results.to_csv(os.path.join(output_path,f_name),sep=',',float_format='%.3f',index_label='Bolts')

def output(results,data):


    output_path = data['projectInformation']['output_dir']
    f_name = data['projectInformation']['project_name']
    if os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(),output_path)
    else:
        os.mkdir(output_path)
        output_path = os.path.join(os.getcwd(),output_path)

    writeCSV(results,output_path,f_name)
