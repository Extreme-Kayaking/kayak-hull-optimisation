from dataclasses import dataclass

@dataclass
class Params:
    """
    Parameters defining a hull.
    Used to create a Hull object.

    density - kg/m^3 (float)

    length - m (float): overall hull length
    beam - m (float): max width of hull
    depth - m (float): max depth of hull below waterline at midship
    
    chine_hardness - float: controls sharpness of hull cross-section (0.0=round, 1.0=sharp)
    
    rocker_bow - m (float): keel curvature at bow
    rocker_stern - m (float): keel curvature at stern
    rocker_position - float: position of minimum rocker along hull length (0.0=bow, 1.0=stern)
    """

    # Physical properties
    density: float
    person_mass: float
    hull_thickness: float

    # global dimensions
    length: float
    beam: float
    depth: float

    # cross-section shape
    chine_hardness: float

    # longitudinal profile
    rocker_bow: float
    rocker_stern: float
    rocker_position: float