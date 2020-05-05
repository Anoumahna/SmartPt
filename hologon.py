import bpy
import numpy
from mathutils import *

radius = 150
n_samples = 30

bpy.ops.import_scene.obj(filepath="./woman.obj") # the 4 different meshes that make up woman.obj will be selected but not active
bpy.context.scene.objects.active = bpy.data.objects[0] # join requires there to be a selected object, not just active
bpy.ops.object.join()
bpy.data.objects[0].name = 'woman' #17,938 vertices
 
bpy.ops.object.modifier_add(type="DECIMATE")
bpy.data.objects['woman'].modifiers['Decimate'].ratio = 0.1 #2,264 vertices

bpy.ops.import_scene.obj(filepath="./man.obj") # now the meshes that make the man are selected, but not active
bpy.context.scene.objects.active = bpy.data.objects[0] # bpy.data.objects is sorted alphabetically all the time! So after renaming previous import to 'woman', objects[0] is part of the new import
bpy.ops.object.join()
bpy.data.objects[0].name = 'man'

bpy.ops.object.modifier_add(type="DECIMATE")
bpy.data.objects['man'].modifiers['Decimate'].ratio = 0.1

# 'man' is both selected and active, we can duplicate as much as we want
for man in range(n_samples // 2): # integer division //, range doesn't take floats
    bpy.ops.object.duplicate_move()
    bpy.context.active_object.select = False # deselect the object that was just created so we don't duplicate everything each time
    bpy.context.scene.objects.active = bpy.data.objects['man'] # join requires there to be a selected object, not just active
    bpy.data.objects['man'].select = True

# select the woman and duplicate
bpy.data.objects['man'].select = False
bpy.context.scene.objects.active = bpy.data.objects['woman']
bpy.data.objects['woman'].select = True

for woman in range(n_samples // 2): # integer division //, range doesn't take floats
    bpy.ops.object.duplicate_move()
    bpy.context.active_object.select = False # deselect the object that was just created so we don't duplicate everything each time
    bpy.context.scene.objects.active = bpy.data.objects['woman'] # join requires there to be a selected object, not just active
    bpy.data.objects['woman'].select = True

samples = numpy.random.multivariate_normal([-0.5, -0.5], [[radius, 0],[0, radius]], n_samples)

for xy in range(len(samples)):
    xyz = tuple(samples[xy]) + (0,) # convert array to tuple, append tuple for z coordinate 0, result is 3-tuple 
    bpy.data.objects[xy].location = xyz
        
allObjects = list(bpy.data.objects) # turn the bpy collection into a list so we can shuffle it
numpy.random.shuffle(allObjects) #shuffle the items in place

for blues in range(5):
    thisFigurine = allObjects[blues]
    thisFigurine.keyframe_insert('location',frame=0)        
    thisFigurine.location = Vector(((-blues * 6) - 10,0,35))
    thisFigurine.keyframe_insert('location',frame=125)   

for reds in range(5,10):
    thisFigurine = allObjects[reds]
    thisFigurine.keyframe_insert('location',frame=125)      
    thisFigurine.location = Vector((((reds - 4) * 6) + 10,0,35))
    thisFigurine.keyframe_insert('location',frame=250)


bpy.ops.wm.save_as_mainfile(filepath="./30menandwomen.blend")
bpy.ops.export_scene.fbx(filepath="./30menandwomen.fbx",
                         object_types={'MESH'},
                         bake_anim_use_nla_strips=False, 
                         bake_anim_use_all_actions=False)