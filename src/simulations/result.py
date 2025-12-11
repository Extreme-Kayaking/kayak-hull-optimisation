from dataclasses import dataclass
from trimesh import Scene

@dataclass
class Result:
    """
    float righting_moment: angular force exerted to right the hull
    float draugh_proportion: [0,1] proportion of hull underwater when floating
    Trimesh.Scene scene: scene containing the tilted hull & waterline for viewing with scene.show()
    """
    righting_moment: float
    draught_proportion: float
    scene: Scene
