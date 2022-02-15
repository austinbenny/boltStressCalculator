import numpy as np 
import pandas as pd

def circArea(d_maj):
    return np.pi*(d_maj**4)/4

def circMomentInertia(d_maj):
    R = d_maj/2
    return np.pi*(R**4)/4

def writeCSV(data):

    pass
``
def extract(data):
    ''' Extract most information from .yml file '''

    bolts = np.array([[bolt['bolt'],bolt['major_diameter'],bolt['minor_diameter'],bolt['tpi']] + bolt['location'] for bolt in data['fasteners']])
    bolts = pd.DataFrame(bolts[:,1:],columns=['d_maj','d_min','tpi','x','y','z',],index=bolts[:,0]).astype(np.float64)

    # get BC
    forces = np.array([[force['force']] + force['magnitude'] + force['location'] for force in data['forces']])
    forces = pd.DataFrame(forces[:,1:],columns=['fx','fy','fz','x','y','z'],index=forces[:,0]).astype(float)
    moments = np.array([[moment['moment']] + moment['magnitude'] + moment['location'] for moment in data['moments']])
    moments = pd.DataFrame(moments[:,1:],columns=['mx','my','mz','x','y','z'],index=moments[:,0]).astype(float)

    centroidBC(data,bolts,forces,moments)

def centroidBC(data,bolts,forces,moments):
    ''' calculate forces and moments at bolting centroid '''

    bc = pd.DataFrame({'moment':[moments.loc[:,col].sum() for col in ['mx','my','mz']],\
    'force':[forces.loc[:,col].sum() for col in ['fx','fy','fz']]},index=['x','y','z']).astype(np.float64)
    
    fastenerStress(data,bolts,bc)

def fastenerStress(data,bolts,bc):

    # find tensile and shear area

    # find location and moment arms
    origin = data['patternCentroid']['location']
    bolts['dx'] = bolts.loc[:,'x'] - origin[0]
    bolts['dy'] = bolts.loc[:,'y'] - origin[1]
    bolts['dz'] = bolts.loc[:,'z'] - origin[2]

    # get diameters & areas
    bolts['area'] = list(map(circArea,bolts.loc[:,'d_maj']))

    # find moment of intertias
    bolts['Ixx'] = np.sum(bolts['area']*bolts['dy'] +  np.array(list(map(circMomentInertia,bolts.loc[:,'d_maj']))))
    bolts['Iyy'] = np.sum(bolts['area']*bolts['dx'] +  np.array(list(map(circMomentInertia,bolts.loc[:,'d_maj']))))
    bolts['Ixy'] = bolts['Ixx'] + bolts['Iyy']

    # find normal force
    # factor in directions
    mom_term = ((bolts.loc[:,['dx','dy']].to_numpy()/bolts.loc[:,['Ixx','Iyy']]).dot(bc.loc[['x','y'],'moment'].to_numpy()[:,None])).to_numpy()
    f_term = (np.repeat(bc.loc['z','force'],bolts.shape[0])*(bolts.loc[:,'area'].sum()/bolts.loc[:,'area'].to_numpy()))[:,None]
    bolts['normal force'] = mom_term + f_term
    bolts['normal stress'] = bolts['normal force']/bolts['area']

    # find shear force

    

