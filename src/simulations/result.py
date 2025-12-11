from dataclasses import dataclass
from trimesh import Scene

@dataclass
class Result:
    """
    float righting_moment: angular force exerted to right the hull
    float draugh_proportion: [0,1] proportion of hull above the waterline when floating
    Trimesh.Scene scene: scene containing the tilted hull & waterline for viewing with scene.show()
    float cost: Simulation cost (accounting for # of iterations, and discretisation). Note: does not account for (hardware-dependent) time taken to complete
    """
    righting_moment: float
    draught_proportion: float
    scene: Scene
    cost: float
