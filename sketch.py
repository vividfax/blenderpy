import bpy
from random import *


def setup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    bpy.context.object.data.energy = 10
    bpy.ops.object.camera_add(location=(0, 0, 5), rotation=(0, 0, 0))
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1,1,1, 1)


def draw():
    drawBackground()
    drawSpheres()


def drawBackground():
    mat = newMat("Plane")
    mat.node_tree.nodes["Emission"].inputs[0].default_value = (0.0231534, 0.031896, 0.0703601, 1)
    mat.node_tree.nodes["Emission"].inputs[1].default_value = 1

    bpy.ops.mesh.primitive_plane_add(size=300, enter_editmode=False, align='WORLD', location=(0, 0, 0))

    bpy.context.active_object.data.materials.append(mat)


def drawSpheres():
    mat = newMat("Material")
    bpy.data.materials["Material"].node_tree.nodes["Velvet BSDF"].inputs[0].default_value = (1, 0.185308, 0.233881, 1)
    bpy.data.materials["Material"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (1, 0.185308, 0.233881, 1)

    for x in range (-4, 5):
        for y in range(-4, 5):

            rad = randrange(-1, 5)
            obj = bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, location=(x, y, 0))

            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].render_levels = 3

            bpy.context.active_object.data.materials.append(mat)


def newMat(str):
    mat = bpy.data.materials.get(str)
    if mat is None:
        mat = bpy.data.materials.new(name=str)
    return mat


setup()
draw()
