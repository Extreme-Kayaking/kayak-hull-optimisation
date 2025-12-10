from dataclasses import dataclass

@dataclass
class Params:
    """
    Parameters defining a hull.
    Used to create a Hull object.
    """
    density: float
    heel: float  # Heel angle
    # Note: heel could be moved into mutating an existing hull and recalculating draught (more efficient)
