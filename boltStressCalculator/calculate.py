import numpy as np
import pandas as pd

coords = ["x", "y", "z"]


def tensileArea(d, tpi):
    return (np.pi / 4) * (d - 0.9743 / tpi) ** 2


def storeAttrs(bolts, axes):
    """Function stores the attributes in the pandas df

    :param bolts: bolts dataframe
    :type bolts: pandas df
    :return: df with stored attributes
    :rtype: pandas df
    """

    a1, a2, a3 = axes
    bolts.attrs[f"I{a1}{a1}"] = bolts.attrs[f"I{a2}{a2}"] = bolts.attrs[
        f"I{a1}{a2}"
    ] = "in^4"
    bolts.attrs["tensile area"] = bolts.attrs["shear area"] = "in^2"
    bolts.attrs["normal stress"] = bolts.attrs["shear stress"] = "psi"
    bolts.attrs["IR_normal"] = bolts.attrs["IR_shear"] = "Dimensionless"
    bolts.attrs["normal force"] = bolts.attrs["shear force"] = "lbf"
    bolts.attrs["Centroid"] = findCentroid(bolts).to_numpy()

    return bolts


def findCentroid(bolts):
    """This function takes the bolt pattern location data and determined the
    centroid. It also sets the calculator origin to be at said centroid.

    :param bolts: bolts and their parameters
    :type bolts: pandas df
    :return: bolts with the dimensions from the pattern centroid
    :rtype: pandas df
    """

    cg = [
        np.sum(bolts["tensile area"] * bolts[c]) / np.sum(bolts["tensile area"])
        for c in coords
    ]
    return pd.DataFrame(np.array(cg)[:, None].T, columns=coords)


def planeCheck(bolts, plane):
    """Function checks if 2D plane value in inputs.yml makes sense.

    :param bolts: bolts data
    :type bolts: pandas df
    :param plane: plane
    :type plane: string
    :return: True if error check passes
    :rtype: Boolean
    """
    # make sure it is a 2D bolting pattern
    count = 0
    for a in coords:
        if len(set(bolts[a])) < 2:
            count += 1

    if count < 2:
        for a in coords:
            if len(set(bolts[a])) == 1:
                noPlane = a

    if noPlane in plane:
        return False

    return True


def extract(data):
    """This function extracts all the necessary data
    used from the inputs.yml file

    :param data: full inputs.yml file
    :type data: dict
    :return: df with structural characteristics
    :rtype: pandas df
    """

    bolts = np.array(
        [
            [bolt["bolt"], bolt["major_diameter"], bolt["tpi"], bolt["Sy"]]
            + bolt["location"]
            for bolt in data["fasteners"]
        ]
    )
    bolts = pd.DataFrame(
        bolts[:, 1:], columns=["d_maj", "tpi", "Sy", "x", "y", "z"], index=bolts[:, 0]
    ).astype(float)
    bolts["tensile area"] = list(map(tensileArea, bolts["d_maj"], bolts["tpi"]))

    # get BC
    forces = np.array(
        [
            [force["force"]] + force["magnitude"] + force["location"]
            for force in data["forces"]
        ]
    )
    forces = pd.DataFrame(
        forces[:, 1:], columns=["fx", "fy", "fz", "x", "y", " z"], index=forces[:, 0]
    ).astype(float)

    # factor in plane here
    plane = data["frameOfReference"]["plane"]
    a1, a2 = [char for char in plane]
    a3 = [c for c in coords if (c != a1 and c != a2)][0]
    axes = (a1, a2, a3)

    # error check the plane
    if not planeCheck(bolts, plane):
        err_str = (
            "Check plane input in inputs.yml. You have specified "
            f"plane {plane} but the bolt coordinates do not suggest "
            "specified plane."
        )
        raise Exception(err_str)

    return centroidBC(bolts, forces, axes)


def centroidBC(bolts, forces, axes):
    """calculate forces and moments at bolting centroid"""

    # distance from centroid of bolting to force for all force
    centroid = findCentroid(bolts)
    for c in coords:
        forces[f"d{c}"] = forces[c] - centroid[c].to_numpy()

    bc = pd.DataFrame(
        np.zeros(shape=(3, 2)),
        columns=["moments", "forces"],
        index=["mag_x", "mag_y", "mag_z"],
    )

    for r, f in zip(
        forces[["dx", "dy", "dz"]].to_numpy(), forces[["fx", "fy", "fz"]].to_numpy()
    ):
        bc.loc[:, "moments"] += np.cross(r, f)
        bc.loc[:, "forces"] += f

    return fastenerStress(bolts, bc, centroid, axes)


def fastenerStress(bolts, bc, centroid, axes):

    # find tensile and shear area
    totalTensileArea = bolts["tensile area"].sum()

    # find location and moment arms
    for c in coords:
        bolts[f"d{c}"] = bolts[c] - centroid[c].to_numpy()

    # find moment of intertias
    a1, a2, a3 = axes
    bolts[f"I{a1}{a1}"] = np.sum(bolts["tensile area"] * bolts[f"d{a2}"] ** 2)
    bolts[f"I{a2}{a2}"] = np.sum(bolts["tensile area"] * bolts[f"d{a1}"] ** 2)
    bolts[f"I{a1}{a2}"] = bolts[f"I{a1}{a1}"] + bolts[f"I{a2}{a2}"]

    # find normal force
    bolts["normal force"] = (
        (bc.loc[f"mag_{a1}", "moments"] * bolts[f"d{a2}"] * bolts["tensile area"])
        / bolts[f"I{a1}{a1}"]
        + (bc.loc[f"mag_{a2}", "moments"] * bolts[f"d{a1}"] * bolts["tensile area"])
        / bolts[f"I{a2}{a2}"]
        + (bc.loc[f"mag_{a3}", "forces"] * bolts["tensile area"]) / totalTensileArea
    )
    bolts["normal stress"] = bolts["normal force"] / bolts["tensile area"]

    # find shear force
    torsion_r = np.sqrt(bolts[f"d{a1}"] ** 2 + bolts[f"d{a2}"] ** 2)
    torsion_theta = np.arctan(bolts[f"d{a2}"] / bolts[f"d{a1}"])
    torsion = (
        bc.loc[f"mag_{a3}", "moments"] * torsion_r * bolts["tensile area"]
    ) / bolts[f"I{a1}{a2}"]
    torsion_x = torsion * np.sin(torsion_theta)
    torsion_y = -torsion * np.cos(torsion_theta)
    bolts["shear force"] = np.sqrt(
        (
            bc.loc[f"mag_{a1}", "forces"] * (bolts["tensile area"] / totalTensileArea)
            + torsion_x
        ).to_numpy()
        ** 2
        + (
            bc.loc[f"mag_{a2}", "forces"] * (bolts["tensile area"] / totalTensileArea)
            + torsion_y
        ).to_numpy()
        ** 2
    )
    bolts["shear stress"] = bolts["shear force"] / bolts["tensile area"]

    bolts["IR_normal"] = abs(bolts["normal stress"] / bolts["Sy"])
    bolts["IR_shear"] = abs(bolts["shear stress"] / bolts["Sy"])

    bolts = storeAttrs(bolts, axes)
    bolts = bolts.fillna(0)

    return bolts, axes
