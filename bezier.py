import bpy
from bpy import context, data, ops
from random import *


def setup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 300

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    bpy.context.object.data.energy = 10
    bpy.ops.object.camera_add(location=(0, 0, 25), rotation=(0, 0, 0))
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        1, 1, 1, 1)

    bpy.context.scene.cycles.max_bounces = 0  # blacken shadows. default:12


def draw():
    drawBackground()
    drawCurve()


def drawBackground():
    mat = newGlossy("Plane", random(), random(), random())

    bpy.ops.mesh.primitive_plane_add(
        size=300, align='WORLD', location=(0, 0, 0))

    bpy.context.active_object.data.materials.append(mat)


def drawCurve():
    mat = newDiffuse("Curve", random(), random(), random())

    ops.curve.primitive_bezier_circle_add(
        radius=1.0, location=(0.0, 0.0, 0.0), enter_editmode=True)
    ops.curve.subdivide(number_cuts=16)
    ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.0, seed=0)
    ops.transform.resize(value=(2.0, 2.0, 3.0))
    ops.object.mode_set(mode='OBJECT')

    obj_data = context.active_object.data
    obj_data.fill_mode = 'FULL'
    obj_data.extrude = 0.125
    obj_data.bevel_depth = 0.125
    obj_data.resolution_u = 20
    obj_data.render_resolution_u = 32

    bpy.context.active_object.data.materials.append(mat)


def newEmission(str, r, g, b):
    mat = newMat(str)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    emission = nodes.new(type='ShaderNodeEmission')
    mat.node_tree.nodes["Emission"].inputs[0].default_value = (r, g, b, 1)
    mat.node_tree.nodes["Emission"].inputs[1].default_value = 1
    link = links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def newDiffuse(str, r, g, b):
    mat = newMat(str)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)
    link = links.new(diffuse.outputs[0], output.inputs[0])

    return mat


def newVelvet(str, r, g, b):
    mat = newMat(str)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    mix = nodes.new(type='ShaderNodeMixShader')

    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)
    link = links.new(diffuse.outputs[0], mix.inputs[1])

    velvet = nodes.new(type='ShaderNodeBsdfVelvet')
    mat.node_tree.nodes["Velvet BSDF"].inputs[0].default_value = (r, g, b, 1)
    link = links.new(velvet.outputs[0], mix.inputs[2])

    link = links.new(mix.outputs[0], output.inputs[0])

    return mat


def newGlossy(str, r, g, b):
    mat = newMat(str)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    glossy = nodes.new(type='ShaderNodeBsdfGlossy')
    mat.node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (r, g, b, 1)
    mat.node_tree.nodes["Glossy BSDF"].inputs[1].default_value = 0
    link = links.new(glossy.outputs[0], output.inputs[0])

    return mat


def newMat(str):
    mat = bpy.data.materials.get(str)
    if mat is None:
        mat = bpy.data.materials.new(name=str)

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    mat.use_nodes = True
    return mat


setup()
draw()
