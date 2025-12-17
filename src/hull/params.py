from dataclasses import dataclass

@dataclass
class Params:
    """
    Parameters defining a hull.
    Used to create a Hull object.

    density - kg/m^3 (float)

    length - m (float): overall hull length
    beam - m (float): max width of hull
    draft - m (float): max depth of hull below waterline at midship
    rocker_bow - m (float): keel curvature at bow
    rocker_stern - m (float): keel curvature at stern
    section_shape_exponent - float: exponent controlling hull cross-section shape (sharpness)
    """
    density: float

    # Hull geometry parameters
    length: float
    beam: float
    draft: float
    rocker_bow: float
    rocker_stern: float
    section_shape_exponent: float