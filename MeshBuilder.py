from PySide6.Qt3DExtras import Qt3DExtras


def CreateTorusMesh(radius=5, minorRadius=1, rings=100, slices=20):
    mesh = Qt3DExtras.QTorusMesh()
    mesh.setRadius(radius)
    mesh.setMinorRadius(minorRadius)
    mesh.setRings(rings)
    mesh.setSlices(slices)
    return mesh
