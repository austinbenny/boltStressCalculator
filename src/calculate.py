import numpy as np 
import pandas as pd

coords = ['x','y','z']

def tensileArea(d,tpi):
    return (np.pi/4)*(d - 0.9743/tpi)**2

def storeAttrs(results):

    results.attrs['Ixx'] = results.attrs['Iyy'] = results.attrs['Ixy'] = 'in^4'
    results.attrs['tensile area'] = results.attrs['shear area'] = 'in^2'
    results.attrs['normal stress'] = results.attrs['shear stress'] = 'psi'
    results.attrs['IR_normal'] = results.attrs['IR_shear'] = 'none'
    results.attrs['normal force'] = results.attrs['shear force'] = 'lbf'

    return results

def findCentroid(bolts):
    """This function takes the bolt pattern location data and determined the centroid. It also sets the calculator origin to be at said centroid. 

    :param bolts: bolts and their parameters
    :type bolts: pandas df
    :return: bolts with the dimensions from the pattern centroid
    :rtype: pandas df
    """

    cg = [np.sum(bolts['tensile area']*bolts[c])/np.sum(bolts['tensile area']) for c in coords]
    return pd.DataFrame(np.array(cg)[:,None].T,columns=['x','y','z'])
     
def extract(data):
    """This function extracts all the necessary data used from the inputs.yml file

    :param data: full inputs.yml file
    :type data: dict
    :return: df with structural characteristics
    :rtype: pandas df
    """

    bolts = np.array([[bolt['bolt'],bolt['major_diameter'],bolt['tpi'],bolt['Sy']] + bolt['location'] for bolt in data['fasteners']])
    bolts = pd.DataFrame(bolts[:,1:],columns=['d_maj','tpi','Sy','x','y','z'],index=bolts[:,0]).astype(float)
    bolts['tensile area'] = list(map(tensileArea,bolts['d_maj'],bolts['tpi']))

    # get BC
    forces = np.array([[force['force']] + force['magnitude'] + force['location'] for force in data['forces']])
    forces = pd.DataFrame(forces[:,1:],columns=['fx','fy','fz','x','y','z'],index = forces[:,0]).astype(float)
    moments = np.array([[moment['moment']] + moment['magnitude'] + moment['location'] for moment in data['moments']])
    moments = pd.DataFrame(moments[:,1:],columns=['mx','my','mz','x','y','z'],index = moments[:,0]).astype(float)

    # factor in plane here
    plane = data['frameOfReference']['patternCentroid']['plane']
    a1,a2 = [char for char in plane]
    a3 = [c for c in coords if (c != a1 and c != a2)][0]
    axes = (a1,a2,a3)

    return centroidBC(data,bolts,forces,moments,axes)

def centroidBC(data,bolts,forces,moments,axes):
    ''' calculate forces and moments at bolting centroid '''

    # distance from centroid of bolting to force for all force
    centroid = data['frameOfReference']['patternCentroid']['location']
    cg = findCentroid(bolts)
    
    forces['dx'] = forces['x'] - centroid[0]
    forces['dy'] = forces['y'] - centroid[1]
    forces['dz'] = forces['z'] - centroid[2]
    
    bc = pd.DataFrame(np.zeros(shape=(3,2)),columns=['moments','forces'],index=['mag_x','mag_y','mag_z'])
    bc.loc[:,'moments'] += moments[['mx','my','mz']].sum().to_numpy()

    for r,f in zip(forces[['dx','dy','dz']].to_numpy(),forces[['fx','fy','fz']].to_numpy()):
        bc.loc[:,'moments'] += np.cross(r,f)
        bc.loc[:,'forces'] += f
    
    return fastenerStress(bolts,bc,centroid,axes)

def fastenerStress(bolts,bc,centroid,axes):

    # find tensile and shear area
    totalTensileArea = bolts['tensile area'].sum()

    # find location and moment arms
    bolts['dx'] = bolts['x'] - centroid[0]
    bolts['dy'] = bolts['y'] - centroid[1]
    bolts['dz'] = bolts['z'] - centroid[2]

    # find moment of intertias
    a1,a2,a3 = axes
    bolts[f'I{a1}{a1}'] = np.sum(bolts['tensile area']*bolts[f'd{a2}']**2)
    bolts[f'I{a2}{a2}'] = np.sum(bolts['tensile area']*bolts[f'd{a1}']**2)
    bolts[f'I{a1}{a2}'] = bolts[f'I{a1}{a1}'] + bolts[f'I{a2}{a2}']

    # find normal force
    mom_term = (bolts[[f'd{a1}',f'd{a2}']].to_numpy()/bolts[[f'I{a1}{a1}',f'I{a2}{a2}']]) @ \
                bc.loc[[f'mag_{a1}',f'mag_{a2}'],'moments'].to_numpy()[:,None]
    f_term = (np.repeat(bc.loc[f'mag_{a3}','forces'],bolts.shape[0])*\
             (totalTensileArea/bolts['tensile area'].to_numpy()))[:,None]
    bolts['normal force'] = mom_term + f_term
    bolts['normal stress'] = bolts['normal force']/bolts['tensile area']

    # find shear force
    torsion_r = np.sqrt(bolts[f'd{a1}']**2 + bolts[f'd{a2}']**2)
    torsion_theta = np.arctan(bolts[f'd{a2}']/bolts[f'd{a1}'])
    torsion = (bc.loc[f'mag_{a3}','moments']*torsion_r*bolts['tensile area'])/bolts[f'I{a1}{a2}']
    torsion_x = torsion*np.sin(torsion_theta)
    torsion_y = -torsion*np.cos(torsion_theta)
    bolts['shear force'] = np.sqrt(\
                            (bc.loc[f'mag_{a1}','forces']*(bolts['tensile area']/totalTensileArea)\
                           + torsion_x).to_numpy()**2 \
                           + (bc.loc[f'mag_{a2}','forces']*(bolts['tensile area']/totalTensileArea)\
                           + torsion_y).to_numpy()**2)
    bolts['shear stress'] = bolts['shear force']/bolts['tensile area']

    bolts['IR_normal'] = abs(bolts['normal stress']/bolts['Sy'])
    bolts['IR_shear'] = abs(bolts['shear stress']/bolts['Sy'])

    bolts = storeAttrs(bolts)
    bolts = bolts.fillna(0)

    return bolts, axes