import bpy
from random import *
import mathutils
import math


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


def draw():
    drawBackground()
    drawShape(0, 0)
#    drawGrid()
#    drawCirclePack()


def drawBackground():
    mat = newGlossy("Plane", 1, 1, 1)

    bpy.ops.mesh.primitive_plane_add(
        size=300, align='WORLD', location=(0, 0, 0))

    bpy.context.active_object.data.materials.append(mat)


def drawShape(x, y):

    x *= 2
    y *= 2

    size = 1

    for i in range(0, 10):

        vector = mathutils.Vector((x, y, i))
        size = mathutils.noise.cell(vector) + 1.5

        mat = newDiffuse("Shape" + str(x) + "o" + str(y) +
                         "o" + str(i), random(), random(), random())

        bpy.ops.mesh.primitive_plane_add(
            size=size, enter_editmode=False, align='WORLD', location=(x, y, i/10))

        if i % 2 == 0:
            bpy.context.active_object.rotation_euler[2] = math.radians(45)

        vertices = bpy.context.active_object.data.vertices

        for v in vertices:
            new = v.co
            new[0] = new[0] + random()
            new[1] = new[1] + random()
            new[2] = new[2] + random()
            v.co = new

        bpy.context.active_object.data.materials.append(mat)

#    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, 0))

#    bpy.ops.object.modifier_add(type='SMOOTH')

#    bpy.ops.object.modifier_add(type='SUBSURF')
#    bpy.context.object.modifiers["Subdivision"].render_levels = 5

#    bpy.context.active_object.data.materials.append(mat)


def drawGrid():
    for x in range(-4, 5):
        for y in range(-4, 5):
            drawShape(x, y)


class Circle:

    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_
        self.r = 10

    def draw(self):
        mat = newDiffuse(str(self.x) + "o" + str(self.y), 1/self.r/2, .5, .5)

        obj = bpy.ops.mesh.primitive_uv_sphere_add(
            radius=self.r, location=(self.x, self.y, 0))
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3

        bpy.context.active_object.data.materials.append(mat)

    def shrink(self):
        self.r = self.r - .1


def drawCirclePack():

    circles = list()
    for i in range(0, 100):
        x = randrange(-40, 40)
        y = randrange(-40, 40)
        circle = Circle(x, y)
        for c in circles:
            d1 = (x, y)
            d2 = (c.x, c.y)
            distance = math.sqrt(((d1[0]-d2[0])**2)+((d1[1]-d2[1])**2))
            while distance < c.r + circle.r:
                circle.shrink()
        if circle.r > 0:
            circle.draw()
        circles.append(circle)


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
