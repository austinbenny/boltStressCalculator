import numpy as np 
import pandas as pd

def tensileArea(d,tpi):
    return (np.pi/4)*(d - 0.9743/tpi)**2

def circArea(d):
    return np.pi*(d**4)/4

def circMomentInertia(d):
    R = d/2
    return np.pi*(R**4)/4

def storeAttrs(results):

    results.attrs['Ixx'] = results.attrs['Iyy'] = results.attrs['Ixy'] = 'in^4'
    results.attrs['tensile area'] = results.attrs['shear area'] = 'in^2'
    results.attrs['normal stress'] = results.attrs['shear stress'] = 'psi'
    results.attrs['IR_normal'] = results.attrs['IR_shear'] = 'none'

    return results


def extract(data):
    """This function extracts all the necessary data used from the inputs.yml file

    :param data: full inputs.yml file
    :type data: dict or pandas df
    :return: df with structural characteristics
    :rtype: pandas df
    """

    bolts = np.array([[bolt['bolt'],bolt['major_diameter'],bolt['minor_diameter'],bolt['tpi'],bolt['Sy']] + bolt['location'] for bolt in data['fasteners']])
    bolts = pd.DataFrame(bolts[:,1:],columns=['d_maj','d_min','tpi','Sy','x','y','z',],index=bolts[:,0]).astype(np.float64)

    # get BC
    forces = np.array([[force['force']] + force['magnitude'] + force['location'] for force in data['forces']])
    forces = pd.DataFrame(forces[:,1:],columns=['fx','fy','fz','x','y','z'],index=forces[:,0]).astype(float)
    moments = np.array([[moment['moment']] + moment['magnitude'] + moment['location'] for moment in data['moments']])
    moments = pd.DataFrame(moments[:,1:],columns=['mx','my','mz','x','y','z'],index=moments[:,0]).astype(float)

    # factor in plane here

    bolts_struc = centroidBC(data,bolts,forces,moments)
    return storeAttrs(bolts_struc)

def centroidBC(data,bolts,forces,moments):
    ''' calculate forces and moments at bolting centroid '''

    # distance from centroid of bolting to force for all force
    centroid = data['frameOfReference']['patternCentroid']['location']
    forces['dx'] = forces['x'] - centroid[0]
    forces['dy'] = forces['y'] - centroid[1]
    forces['dz'] = forces['z'] - centroid[2]
    
    bc = pd.DataFrame(np.zeros(shape=(3,2)),columns=['moments','forces'],index=['mag_x','mag_y','mag_z'])
    bc.loc[:,'moments'] += moments.loc[:,['mx','my','mz']].sum().to_numpy()

    for r,f in zip(forces.loc[:,['dx','dy','dz']].to_numpy(),forces.loc[:,['fx','fy','fz']].to_numpy()):
        bc.loc[:,'moments'] += np.cross(r,f)
        bc.loc[:,'forces'] += f
    
    return fastenerStress(bolts,bc,centroid)

def fastenerStress(bolts,bc,centroid):

    # find tensile and shear area
    bolts['tensile area'] = list(map(tensileArea,bolts.loc[:,'d_maj'],bolts.loc[:,'tpi']))
    bolts['shear area'] = list(map(circArea,bolts.loc[:,'d_min']))

    # find location and moment arms
    bolts['dx'] = bolts.loc[:,'x'] - centroid[0]
    bolts['dy'] = bolts.loc[:,'y'] - centroid[1]
    bolts['dz'] = bolts.loc[:,'z'] - centroid[2]

    # find moment of intertias
    bolts['Ixx'] = np.sum(bolts['tensile area']*bolts['dy'] +  np.array(list(map(circMomentInertia,bolts.loc[:,'d_maj']))))
    bolts['Iyy'] = np.sum(bolts['tensile area']*bolts['dx'] +  np.array(list(map(circMomentInertia,bolts.loc[:,'d_maj']))))
    bolts['Ixy'] = bolts['Ixx'] + bolts['Iyy']

    # find normal force
    mom_term = (bolts.loc[:,['dx','dy']].to_numpy()/bolts.loc[:,['Ixx','Iyy']]) @ bc.loc[['mag_x','mag_y'],'moments'].to_numpy()[:,None]
    f_term = (np.repeat(bc.loc['mag_z','forces'],bolts.shape[0])*(bolts.loc[:,'tensile area'].sum()/bolts.loc[:,'tensile area'].to_numpy()))[:,None]
    bolts['normal force'] = mom_term + f_term
    bolts['normal stress'] = bolts['normal force']/bolts['tensile area']

    # find shear force
    torsion_r = np.sqrt(bolts.loc[:,'dx']**2 + bolts.loc[:,'dy']**2)
    torsion_theta = np.arctan(bolts.loc[:,'dy']/bolts.loc[:,'dx'])
    torsion = (bc.loc['mag_z','moments']*torsion_r*bolts.loc[:,'shear area'])/bolts.loc[:,'Ixy']
    torsion_x = torsion*np.sin(torsion_theta)
    torsion_y = -torsion*np.cos(torsion_theta)
    bolts['shear force'] = np.sqrt((bc.loc['mag_x','forces']*(bolts.loc[:,'shear area']/bolts.loc[:,'shear area'].sum()) + torsion_x).to_numpy()**2 \
        + (bc.loc['mag_y','forces']*(bolts.loc[:,'shear area']/bolts.loc[:,'shear area'].sum()) + torsion_y).to_numpy()**2)
    bolts['shear stress'] = bolts['shear force']/bolts['shear area']

    bolts['IR_normal'] = abs(bolts['normal stress']/bolts['Sy'])
    bolts['IR_shear'] = abs(bolts['shear stress']/bolts['Sy'])

    bolts_struc = bolts.loc[:,['Ixx','Iyy','Ixy','shear area','tensile area','normal stress','shear stress','IR_normal','IR_shear']]

    return bolts_struc