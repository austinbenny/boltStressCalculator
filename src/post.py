import os
from jinja2 import Template
import matplotlib.pyplot as plt


def htmlhead(title):

    htmlheader = f'''
<!DOCTYPE html>
<html>
  <head>
    <title>{title} Results</title>
    <style>
    table,
    h1,
    th,
    td {{
        padding: 10px;
        border: 1px solid black;
        border-collapse: collapse;
        text-align: left;
    }}
    h1 {{
        border: 3px double #1c87c9;
        background-color: #d9d9d9;
    }}
    </style>
  </head>
  <body>
    <h1>{title} Results</h2>\n'''

    return htmlheader

def writeCSV(results,output_path,f_name):
    
    f_name = f'{f_name}_structural_parameters.csv'
    f_path = os.path.join(output_path,f_name)
    results.to_csv(f_path,sep=',',float_format='%.3f',index_label='Bolts')

    return f_path

def createPLOT():

    pass

def writeHTML(results,output_path,f_name):

    title = f_name
    # write paragraph here

    f_name = f'{f_name}_structural_parameters.html'
    f_path = os.path.join(output_path,f_name)
    with open(f_path,'w+') as html:
        html.write(htmlhead(title))
        html.write('    <table>\n')
        html.write('      <tr>\n')
        html.write(f'        <th>Fasteners</th>\n')
        for key, _ in results.items():
            html.write(f'        <th>{key} [{results.attrs[key]}]</th>\n')
        html.write('      </tr>\n')
        for idx,bolt in enumerate(results.index):
            html.write('      <tr>\n')
            html.write(f'        <td>{str(bolt)}</td>\n')
            for key,val in results.items():
                if (key == 'IR_shear' or key == 'IR_normal'):
                    if (val[idx]  > 0.750 and val[idx] < 1):
                        html.write(f'        <td bgcolor="yellow">{val[idx]:.3f}</td>\n')
                    if val[idx] > 1:
                        html.write(f'        <td bgcolor="red">{val[idx]:.3f}</td>\n')
                    else:
                        html.write(f'        <td bgcolor="lightgreen">{val[idx]:.3f}</td>\n')
                else:
                    html.write(f'        <td>{val[idx]:.3G}</td>\n')
        html.write('      </tr>\n')
        html.write('    </table>\n')
        html.write('   <hr>')
        html.write('  </body>\n')
        html.write('</html>\n')
    
    return f_path


def output(results,data):


    output_path = data['projectInformation']['output_dir']
    f_name = data['projectInformation']['project_name']
    if os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(),output_path)
    else:
        os.mkdir(output_path)
        output_path = os.path.join(os.getcwd(),output_path)

    if data['projectInformation']['output_format'].lower() == 'html':
        f_path = writeHTML(results,output_path,f_name)
    elif data['projectInformation']['output_format'].lower() == 'csv':
        f_path = writeCSV(results,output_path,f_name)

    return f_path


html_template = '''
<!DOCTYPE html>
<html>
  <head>
    <title>{{ title }} Results</title>
    <style>
    table,
    h1,
    th,
    td {
        padding: 10px;
        border: 1px solid black;
        border-collapse: collapse;
        text-align: left;
    }
    h1 {
        border: 3px double #1c87c9;
        background-color: #d9d9d9;
    }
    </style>
  </head>
  <body>
    <h1>{{ title }} Results</h2>
    <table>
      <tr>
        <th>Fasteners</th>
        <th>Ixx [in^4]</th>
        <th>Iyy [in^4]</th>
        <th>Ixy [in^4]</th>
        <th>shear area [in^2]</th>
        <th>tensile area [in^2]</th>
        <th>normal stress [psi]</th>
        <th>shear stress [psi]</th>
        <th>IR_normal [none]</th>
        <th>IR_shear [none]</th>
      </tr>
      <tr>
        <td>bolt1</td>
        <td>0.196</td>
      </tr>
    </table>
  </body>
</html>

'''

