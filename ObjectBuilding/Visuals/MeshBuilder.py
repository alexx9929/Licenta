from PySide6.Qt3DExtras import Qt3DExtras


def create_torus_mesh(radius=5, minor_radius=1, rings=100, slices=20):
    mesh = Qt3DExtras.QTorusMesh()
    mesh.setRadius(radius)
    mesh.setMinorRadius(minor_radius)
    mesh.setRings(rings)
    mesh.setSlices(slices)
    return mesh


def create_plane_mesh(width=1, height=1):
    mesh = Qt3DExtras.QPlaneMesh()
    mesh.setWidth(width)
    mesh.setHeight(height)
    return mesh


def create_cuboid_mesh(width=1, height=1, depth=1):
    mesh = Qt3DExtras.QCuboidMesh()
    mesh.setXExtent(width)
    mesh.setYExtent(height)
    mesh.setZExtent(depth)
    return mesh
