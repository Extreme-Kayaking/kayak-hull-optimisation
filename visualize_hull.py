#!/usr/bin/env python3
"""
Visualize a hull generated from parameters
"""

from src.hull import Hull, Params

# Create hull parameters
params = Params(
    # Physical properties
    density=900.0,          # kg/m³ (polyethylene)
    hull_thickness=0.005,   # 5mm shell
    
    # Global dimensions
    length=2.6,            # meters
    beam=0.65,             # meters
    depth=0.35,            # meters
    
    # Cross-section shape
    cross_section_exponent=5.0,  # 2.0=round, 10.0=flat/hard chine
    
    # Rocker (longitudinal curve)
    rocker_bow=0.0,       # meters of bow lift
    rocker_stern=0.0,     # meters of stern lift
    rocker_position=0.5,   # 0.5=symmetric, <0.5=more bow rocker
    rocker_exponent=2.0    # 2.0=parabolic curve
)

print("Generating hull mesh...")
hull = Hull(params)

print("\n" + "="*60)
print("HULL INFORMATION")
print("="*60)
print(f"Length:       {params.length:.2f} m")
print(f"Beam:         {params.beam:.2f} m")
print(f"Depth:        {params.depth:.2f} m")
print(f"Mass:         {hull.mass:.2f} kg")
print(f"Volume:       {hull.mesh.volume:.3f} m³")
print(f"Watertight:   {hull.mesh.is_watertight}")
print(f"Vertices:     {len(hull.mesh.vertices)}")
print(f"Faces:        {len(hull.mesh.faces)}")
print(f"\nBounds (X): {hull.mesh.bounds[0][0]:.2f} to {hull.mesh.bounds[1][0]:.2f}")
print(f"Bounds (Y): {hull.mesh.bounds[0][1]:.2f} to {hull.mesh.bounds[1][1]:.2f}")
print(f"Bounds (Z): {hull.mesh.bounds[0][2]:.2f} to {hull.mesh.bounds[1][2]:.2f}")
print("="*60)

print("\nOpening 3D viewer...")
print("(Rotate with mouse, scroll to zoom)")

# Add coordinate axes that extend through the boat
import trimesh
import numpy as np
scene = trimesh.Scene()

# Color the hull - deck vs bottom
mesh_colored = hull.mesh.copy()
colors = np.ones((len(mesh_colored.faces), 4)) * 255  # Start with white

# For each face, check if it's on top or bottom based on vertex z-coordinates
for i, face in enumerate(mesh_colored.faces):
    face_vertices = mesh_colored.vertices[face]
    avg_z = np.mean(face_vertices[:, 2])
    
    if avg_z > 0.0:  # Top/Deck
        colors[i] = [100, 150, 255, 255]  # Light blue
    else:  # Bottom/Hull
        colors[i] = [200, 100, 100, 255]  # Light red

mesh_colored.visual.face_colors = colors
scene.add_geometry(mesh_colored)

# Create longer axes that extend beyond the hull
axis_length = max(params.length, params.beam, params.depth) * 1.2
axes = trimesh.creation.axis(
    origin_size=0.01, 
    axis_radius=0.005, 
    axis_length=axis_length
)
scene.add_geometry(axes)

print("\nColors: Blue = Deck (top), Red = Hull (bottom)")
scene.show()
