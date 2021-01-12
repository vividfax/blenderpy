import bpy
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
    bpy.ops.object.camera_add(location=(0, 0, 12), rotation=(0, 0, 0))
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1,1,1, 1)


def draw():
    drawBackground()
    drawSpheres()


def drawBackground():
    mat = newMat("Plane")

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    emission = nodes.new( type = 'ShaderNodeEmission' )
    mat.node_tree.nodes["Emission"].inputs[0].default_value = (0.0231534, 0.031896, 0.0703601, 1)
    mat.node_tree.nodes["Emission"].inputs[1].default_value = 1
    link = links.new( emission.outputs['Emission'], output.inputs['Surface'] )

    bpy.ops.mesh.primitive_plane_add(size=300, enter_editmode=False, align='WORLD', location=(0, 0, 0))

    bpy.context.active_object.data.materials.append(mat)


def drawSpheres():
    for x in range (-4, 5):
        for y in range(-4, 5):

            r = random()
            g = random()
            b = 0.5

            mat = newMat("Sphere" + str(x) + "o" + str(y))

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            output = nodes.new( type = 'ShaderNodeOutputMaterial' )

            mix = nodes.new( type = 'ShaderNodeMixShader' )

            diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
            mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)
            link = links.new( diffuse.outputs[0], mix.inputs[1] )

            velvet = nodes.new( type = 'ShaderNodeBsdfVelvet' )
            mat.node_tree.nodes["Velvet BSDF"].inputs[0].default_value = (r, g, b, 1)
            link = links.new( velvet.outputs[0], mix.inputs[2] )

            link = links.new( mix.outputs[0], output.inputs[0] )

            rad = 1
            obj = bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, location=(x, y, 0))

            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].render_levels = 3

            bpy.context.active_object.data.materials.append(mat)


            obj = bpy.ops.mesh.primitive_uv_sphere_add(radius=rad/2, location=(x-.5, y-.5, 1))

            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].render_levels = 3

            bpy.context.active_object.data.materials.append(mat)


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
