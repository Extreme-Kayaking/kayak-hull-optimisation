"""
Hull object, generated from hull parameters.
Including mesh and all info required for simulation
"""

from trimesh import Trimesh
import trimesh
from params import Params
from typing import Tuple, Any
import numpy as np

def vec3d_to_tuple(vec: np.ndarray[Any, np.dtype[np.float64]]) -> Tuple[float, float, float]:
  return (vec[0], vec[1], vec[2])

class Hull:
  def __init__(self, params: Params) -> None:
    """
    params: dict: "density" ...
    """
    # Set unmodified params
    self.density: float = params.density
    
    # Generate Mesh
    self.mesh: Trimesh = Hull.generate_mesh(params)
    if self.mesh.is_watertight:
      raise RuntimeError("Generated Hull contains Holes")

    # Calculate mesh properties
    self.width: float = self.mesh.bounds[0]
    self.length: float = self.mesh.bounds[1]
    self.height: float = self.mesh.bounds[2]

    self.mass: float = self.mesh.mass

    self.centre_of_mass: Tuple[float, float, float] = vec3d_to_tuple(self.mesh.center_mass)
    moments_of_inertia = self.mesh.mass_properties.inertia
    self.i_xx = vec3d_to_tuple(moments_of_inertia[0])
    self.i_yy = vec3d_to_tuple(moments_of_inertia[1])
    self.i_zz = vec3d_to_tuple(moments_of_inertia[2])

    # Draught and buoyancy
    self.draught = Hull.iterate_draught(self.mesh)
    self.centre_of_buoyancy = Hull.calculate_centre_of_buoyancy(self.mesh, self.draught)

  @staticmethod
  def generate_mesh(params: Params) -> Trimesh:
    return Trimesh() # TODO

  @staticmethod
  def iterate_draught(mesh: Trimesh) -> float:
    """
    Iterate various water levels (draught) and calculate displacement.
    Returns the draught iterating until displacement = weight
    """
    return 0 # TODO

  @staticmethod
  def calculate_centre_of_buoyancy(mesh: Trimesh, draught: float) -> Tuple[float, float, float]:
    """
    Calculate the centre of buoyancy for a given draught level.
    i.e. The centre of mass of the submerged portion.
    """
    return (0, 0, 0) # TODO

  def save_to_stl(self, filepath: str) -> None:
    if self.mesh is None:
      raise ValueError("Mesh not generated.")
    self.mesh.export(filepath)
    
    
  def load_from_stl(self, filepath: str) -> None:
    loaded = trimesh.load(filepath)
    if not isinstance(loaded, trimesh.Trimesh):
      raise ValueError("Loaded STL did not contain a valid mesh.")
    self.mesh = loaded
    # TODO recalculate_properties
