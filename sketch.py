import bpy
from random import *


def setup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.engine = 'CYCLES'

#    bpy.ops.object.light_add(type='SUN', location=(0, 0, 0))
#    bpy.context.object.data.energy = 1000
    bpy.ops.object.camera_add(location=(0, 0, 25), rotation=(0, 0, 0))
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        1, 1, 1, 1)


def draw():
    drawBackground()
    drawSpheres()


def drawBackground():
    mat = newMat("Plane")
    mat.node_tree.nodes["Emission"].inputs[0].default_value = (
        1, 0.570698, 0, 1)
    mat.node_tree.nodes["Emission"].inputs[1].default_value = 1

    bpy.ops.mesh.primitive_plane_add(
        size=30, enter_editmode=False, align='WORLD', location=(0, 0, 0))

    bpy.context.active_object.data.materials.append(mat)


def drawSpheres():
    mat = newMat("Material")
    mat.node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (
        0, 0.0394903, 0.212479, 1)
    mat.node_tree.nodes["Glossy BSDF"].inputs[1].default_value = 0.1

    for x in range(-4, 5):
        for y in range(-4, 5):

            z = randrange(0, 10)
            obj = bpy.ops.mesh.primitive_uv_sphere_add(
                radius=.8, location=(x, y, z))

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
