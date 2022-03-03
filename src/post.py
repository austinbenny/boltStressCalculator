import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

try:
    import calculate
except:
    from src import calculate

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

def getBarColors(bolts,s_type):
    """Helper function to get colors for bar chart

    :param bolts: properties of bolts
    :type bolts: pandas df
    """

    lstIR = bolts[f'IR_{s_type}'].to_numpy()
    lstColors = np.zeros(shape = len(lstIR), dtype='<U32')
    for i,IR in enumerate(lstIR):
        if IR < 0.75:
            lstColors[i] = 'green'
        elif (IR > 0.75 and IR < 1):
            lstColors[i] = 'yellow'
        else:
            lstColors[i] = 'red'

    return lstColors


def getColormap(maxIR):

    colors = np.linspace(255,150)/255
    colorMap = np.zeros((len(colors),4))
    colorMap[:,1] = colors
    colorMap[:,3] = len(colors)*[1]

    if maxIR > 0.75:

        colorMapYl = np.zeros((len(colors),4))
        colorMapYl[:,1] = colors
        colorMapYl[:,[0,3]] = np.ones((len(colors),2))
        colorMap = np.vstack((colorMap,colorMapYl))
    
    if maxIR > 1:

        colorMapRd = np.zeros((len(colors),4))
        colorMapRd[:,0] = colors
        colorMapRd[:,3] = len(colors)*[1]
        colorMap = np.vstack((colorMap,colorMapRd))

    return ListedColormap(colorMap)

def createPLOT(bolts,axes,output_path):

    a1,a2,_ = axes
    cg = calculate.findCentroid(bolts)
    fig, ((norm_scatter,shear_scatter),\
          (norm_hist, shear_hist)) = plt.subplots(2,2, figsize=(12,7))
    for s_type,ax,idx in zip(['normal','shear'],[[norm_scatter,norm_hist],[shear_scatter,shear_hist]],[0,1]):
        # make scatter
        # get new colorbar
        newcmp = getColormap(bolts[f'IR_{s_type}'].max())
        scatter_plot = ax[0].scatter(bolts[a1],bolts[a2],\
                    c = bolts[f'IR_{s_type}'],
                    s = (bolts[a1].max()/bolts['d_maj'].max())*75,
                    cmap = newcmp,
                    label='Fastener')
        ax[0].scatter(cg[a1],cg[a2],\
                    marker = 'D',
                    alpha = 0.25,
                    color = 'grey',
                    label = 'CG')
        ax[0].set_title(f'{s_type} stress IR on fasteners', fontweight = 'bold')
        ax[0].set_xlabel(f'${a1}$ [in]')
        if idx == 0:
            ax[0].set_ylabel(f'${a2}$ [in]')
            ax[0].legend(loc = 'best')
        fig.colorbar(scatter_plot, ax = ax[0], label = 'IR')
        ax[0].grid(linestyle='dashed')
        ax[0].set_xlim([1.25*bolts[a1].min(),1.25*bolts[a1].max()])
        # make bar
        ax[1].set_xticks(range(bolts.shape[0]), bolts.index.to_numpy())
        ax[1].bar(x = range(bolts.shape[0]),\
                  height = bolts[f'{s_type} stress'],
                  color = getBarColors(bolts,s_type))
        ax[1].set_title(f'{s_type} stress on fasteners',fontweight = 'bold')
        ax[1].set_ylabel(f'{s_type} stress [psi]')
    plot_path = f'{output_path}/bolts_stress_plot.svg'
    fig.tight_layout()
    fig.savefig(plot_path,bbox_inches='tight')
    
    return plot_path

def getResults(bolts,axes):

    a1,a2,a3 = axes
    results = bolts[[f'I{a1}{a1}',f'I{a2}{a2}',f'I{a1}{a2}',\
                    'normal force','shear force',\
                    'normal stress','shear stress',\
                    'IR_normal','IR_shear']]
    return results

def writeHTML(bolts,axes,output_path,f_name):

    results = getResults(bolts,axes)
    plot_path = createPLOT(bolts,axes,output_path)

    title = f_name
    # bullet points
    maxNormName = bolts['normal stress'].idxmax()
    maxShearName = bolts['shear stress'].idxmax()
    lines = [f"The centroid of the pattern is at: {bolts.attrs['Centroid'][0]}",\
             f"The fastener(s) with the largest normal stress is(are): [{maxNormName}] at [{bolts.loc[maxNormName,'normal stress']:.3G}] psi",
             f"The fastener(s) with the largest shear stress is(are): [{maxShearName}] at [{bolts.loc[maxShearName,'shear stress']:.3G}] psi",
             ]
    f_name = f'{f_name}_structural_parameters.html'
    f_path = os.path.join(output_path,f_name)
    with open(f_path,'w+') as html:
        html.write(htmlhead(title))
        # Information line
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
        html.write('   <hr>\n')
        html.write('  </body>\n')
        html.write('<p>The stress values in negative imply that the fastener is in compression while the positive values imply the fastener is in tension. A green color indicates the IR is below 0.75, yellow indicates the IR is above 0.75 but below 1, and red indicates the IR is above 1. In some of the output (such as the sub plots), the aforementioned colors vary subtly (or along a gradient) depending on the corresponding IR value. For example, for a fastener with an IR of 0.4, the green will be a darker shade.\n')
        html.write('<ul style=“list-style-type:circle>\n')
        for ln in lines:
            html.write(f'<li>{ln}</li>\n')
        html.write('</ul>\n')
        html.write('<p>The plots below are generated from the results.\n')
        html.write(f'<img src="{plot_path}" alt="Stress Plots">\n')
        html.write('</html>\n')
    
    return f_path


def output(bolts,axes,case):

    output_path = case['projectInformation']['output_dir']
    f_name = case['projectInformation']['project_name']
    output_path = os.path.join(output_path,f_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(),output_path)
    else:
        os.mkdir(output_path)
        output_path = os.path.join(os.getcwd(),output_path)

    if case['projectInformation']['output_format'].lower() == 'html':
        f_path = writeHTML(bolts,axes,output_path,f_name)
    elif case['projectInformation']['output_format'].lower() == 'csv':
        f_path = writeCSV(getResults(bolts,axes),output_path,f_name)

    return f_path


if __name__ == "__main__":

    print(getColormap(0.5))


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

