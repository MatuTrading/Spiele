#!/usr/bin/env python3
"""ODIN asset builder. Run inside Blender: blender -b --python build_asset.py -- --job file.json --output output.
No remote commands, dynamic script execution, add-ons or paid dependencies.
"""
import argparse
import json
import math
import random
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector

PALETTE = {}
ARMATURE = None
EXPORT_OBJECTS = []


def color(hexrgb):
    h = hexrgb.removeprefix('#')
    if not re.fullmatch('[0-9a-fA-F]{6}', h):
        raise ValueError('Invalid material color')
    def srgb(v):
        v = int(v, 16) / 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    return tuple(srgb(h[i:i+2]) for i in (0, 2, 4)) + (1,)


def material(name, hexrgb, metallic=0, roughness=.65):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color(hexrgb)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = mat.diffuse_color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return mat


def register(obj, mat=None, bone=None):
    if mat:
        obj.data.materials.append(mat)
    if bone:
        if ARMATURE is None:
            raise RuntimeError('Cannot skin before armature exists')
        vg = obj.vertex_groups.new(name=bone)
        vg.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
        mod = obj.modifiers.new('ODIN Armature', 'ARMATURE')
        mod.object = ARMATURE
        obj.parent = ARMATURE
    obj['odin_export'] = True
    EXPORT_OBJECTS.append(obj)
    return obj


def cube(name, loc, scale, mat, bone=None, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        m = o.modifiers.new('Soft edge', 'BEVEL')
        m.width = bevel
        m.segments = 2
        if hasattr(m, 'affect'):
            m.affect = 'EDGES'
        m2 = o.modifiers.new('Normals', 'WEIGHTED_NORMAL')
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.ops.object.modifier_apply(modifier=m2.name)
    return register(o, mat, bone)


def sphere(name, loc, scale, mat, bone=None, segments=16, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for p in o.data.polygons:
        p.use_smooth = True
    return register(o, mat, bone)


def cylinder(name, a, b, radius, mat, bone=None, vertices=10, radius_end=None):
    start, end = Vector(a), Vector(b)
    axis = end - start
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius,
                                    radius2=radius if radius_end is None else radius_end,
                                    depth=axis.length, location=(start+end)/2)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = axis.to_track_quat('Z','Y').to_euler()
    return register(o, mat, bone)


def tube(name, coords, radius, mat, bone=None, smooth=True):
    curve = bpy.data.curves.new(name+'Path', type='CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 12
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new('POLY')
    spline.points.add(len(coords)-1)
    for p, co in zip(spline.points, coords):
        p.co = (*co,1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='MESH')
    obj = bpy.context.object
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    return register(obj, mat, bone)


def make_rig():
    global ARMATURE
    arm = bpy.data.armatures.new('ODIN_Rig')
    rig = bpy.data.objects.new('ODIN_Armature', arm)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    definitions = [
        ('Root', (0,0,.15), (0,0,.98), None),
        ('Hips', (0,0,.98), (0,0,1.15), 'Root'),
        ('Spine', (0,0,1.15), (0,0,1.72), 'Hips'),
        ('Neck', (0,0,1.72), (0,0,1.89), 'Spine'),
        ('Head', (0,0,1.89), (0,0,2.16), 'Neck'),
        ('UpperArm.L',(-.36,0,1.66),(-.76,0,1.48),'Spine'),
        ('Forearm.L',(-.76,0,1.48),(-1.06,-.07,1.31),'UpperArm.L'),
        ('Hand.L',(-1.06,-.07,1.31),(-1.13,-.16,1.25),'Forearm.L'),
        ('UpperArm.R',(.36,0,1.66),(.76,0,1.48),'Spine'),
        ('Forearm.R',(.76,0,1.48),(1.06,-.07,1.31),'UpperArm.R'),
        ('Hand.R',(1.06,-.07,1.31),(1.13,-.16,1.25),'Forearm.R'),
        ('Thigh.L',(-.22,0,1.01),(-.25,-.03,.59),'Hips'),
        ('Shin.L',(-.25,-.03,.59),(-.23,-.02,.20),'Thigh.L'),
        ('Foot.L',(-.23,-.02,.20),(-.23,-.27,.12),'Shin.L'),
        ('Thigh.R',(.22,0,1.01),(.25,-.03,.59),'Hips'),
        ('Shin.R',(.25,-.03,.59),(.23,-.02,.20),'Thigh.R'),
        ('Foot.R',(.23,-.02,.20),(.23,-.27,.12),'Shin.R'),
    ]
    for name, head, tail, parent in definitions:
        b = arm.edit_bones.new(name)
        b.head, b.tail = head,tail
        if parent:
            b.parent = arm.edit_bones[parent]
            b.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')
    rig['odin_export'] = True
    EXPORT_OBJECTS.append(rig)
    ARMATURE = rig
    return rig


def character_mesh(job):
    p = dict(hair='#E8B94E', armor='#344655', leather='#65412C', metal='#B9C7D1', cloth='#29493D')
    p.update(job.get('palette', {}))
    for key, value in p.items():
        if key not in ('hair','armor','leather','metal','cloth'):
            raise ValueError('Unsupported color key')
        color(value)
    m = {key:material(key, val, metallic=.62 if key=='metal' else .05) for key,val in p.items()}
    m.update(skin=material('skin','#E9BB92'), eye=material('eyes','#86ABBA'),
             black=material('pupils','#142530'), trim=material('warm_gold','#D7AB57',.63),
             fur=material('wolf_fur','#AEB4AD'), wood=material('bow_wood','#915734'),
             string=material('bow_string','#DFD2B4'))
    make_rig()
    sphere('ChestArmor',(0,-.005,1.46),(.43,.25,.37),m['armor'],'Spine')
    sphere('Tunic',(0,0,1.16),(.38,.23,.26),m['cloth'],'Hips')
    cylinder('Belt',(-.38,0,1.125),(.38,0,1.125),.075,m['leather'],'Hips')
    cube('BeltBuckle',(0,-.265,1.125),(.16,.06,.13),m['trim'],'Hips',.02)
    sphere('HeadShape',(0,-.045,2.02),(.25,.225,.28),m['skin'],'Head')
    sphere('Nose',(0,-.252,1.991),(.064,.073,.085),m['skin'],'Head')
    for side in (-1,1):
        sphere('Eye'+str(side),(side*.102,-.244,2.085),(.043,.024,.040),m['eye'],'Head')
        sphere('Pupil'+str(side),(side*.102,-.267,2.088),(.018,.012,.020),m['black'],'Head')
        sphere('Brow'+str(side),(side*.103,-.245,2.157),(.093,.026,.024),m['hair'],'Head')
        sphere('Ear'+str(side),(side*.246,-.03,2.015),(.052,.066,.092),m['skin'],'Head')
    sphere('HairCap',(0,.015,2.235),(.27,.23,.16),m['hair'],'Head')
    for i,x in enumerate((-.19,-.10,0,.10,.19)):
        cylinder('HairFringe'+str(i),(x,-.22,2.26),(x,-.25,2.16-abs(x)*.15),.06,m['hair'],'Head',6,radius_end=.012)
    for s in (-1,1):
        cylinder('HairBraid'+str(s),(s*.235,.04,2.24),(s*.27,.04,1.89),.056,m['hair'],'Head',8,radius_end=.03)
        sphere('ShoulderFur'+str(s),(s*.38,.03,1.67),(.25,.30,.135),m['fur'],'Spine')
        cylinder('UpperArm'+str(s),(s*.42,0,1.64),(s*.76,0,1.48),.125,m['cloth'], 'UpperArm.L' if s<0 else 'UpperArm.R')
        cylinder('Bracer'+str(s),(s*.76,0,1.48),(s*1.06,-.07,1.31),.107,m['leather'], 'Forearm.L' if s<0 else 'Forearm.R')
        sphere('Hand'+str(s),(s*1.10,-.12,1.28),(.11,.11,.095),m['skin'],'Hand.L' if s<0 else 'Hand.R')
        cylinder('UpperLeg'+str(s),(s*.22,0,1.01),(s*.25,-.03,.59),.17,m['cloth'], 'Thigh.L' if s<0 else 'Thigh.R')
        cylinder('LowerLeg'+str(s),(s*.25,-.03,.59),(s*.23,-.02,.20),.14,m['leather'], 'Shin.L' if s<0 else 'Shin.R')
        sphere('Boot'+str(s),(s*.23,-.18,.15),(.17,.31,.16),m['leather'],'Foot.L' if s<0 else 'Foot.R')
        sphere('KneeGuard'+str(s),(s*.25,-.17,.59),(.165,.08,.11),m['metal'],'Shin.L' if s<0 else 'Shin.R')
    sphere('Beard',(0,-.20,1.895),(.185,.13,.17),m['hair'],'Head')
    for side in (-1,1):
        sphere('ChestBadge'+str(side),(side*.25,-.235,1.52),(.09,.04,.09),m['trim'],'Spine')
    cube('CloakBack',(0,.25,1.39),(.69,.08,.67),m['cloth'],'Spine',.05)
    # Wooden recurved bow, physically skinned to Hand.L; all components move with that hand.
    arc=[]
    for i in range(21):
        t=-1+2*i/20
        arc.append((-1.24-.23*(1-t*t),-.15,1.25+t*.77))
    tube('RecurveBow',arc,.035,m['wood'],'Hand.L')
    tube('BowString',[arc[0],(-1.24,-.15,1.25),arc[-1]],.008,m['string'],'Hand.L')
    sphere('BowGrip',(-1.47,-.15,1.25),(.085,.08,.12),m['leather'],'Hand.L')
    # Arrow prepared in the drawing hand; exact nock/string deformation remains a future refinement.
    cylinder('NockedArrow',(1.09,-.12,1.29),(1.09,-1.18,1.29),.016,m['wood'],'Hand.R',8)
    cylinder('Arrowhead',(1.09,-1.19,1.29),(1.09,-1.33,1.29),.042,m['metal'],'Hand.R',6,radius_end=0)
    for z in (1.25,1.32):
        cube('ArrowFeather',(1.09,-.23,z),(.09,.20,.018),m['fur'],'Hand.R')
    # Back quiver is attached to torso; decorative arrow shafts are separate geometries.
    cylinder('Quiver',(0,.32,1.55),(.1,.34,1.95),.13,m['leather'],'Spine',10)
    for x in (-.07,0,.07):
        cylinder('QuiverArrow',(x,.37,1.8),(x,.37,2.18),.014,m['wood'],'Spine',6)
        sphere('QuiverFletching',(x,.37,2.18),(.055,.045,.08),m['fur'],'Spine')
    return ARMATURE


def make_clips(arm, names):
    # Blended poses are deliberately modest, reducing limb/weapon intersections in the first pipeline version.
    bone_names = ('Root','Hips','Spine','Neck','Head','UpperArm.L','Forearm.L','Hand.L',
                  'UpperArm.R','Forearm.R','Hand.R','Thigh.L','Shin.L','Foot.L','Thigh.R','Shin.R','Foot.R')
    arm.animation_data_create()
    definitions = {
       'Idle': [(1,0),(12,1),(24,0),(36,-1),(48,0)],
       'Walk': [(1,0),(8,1),(16,0),(24,-1),(32,0)],
       'Run': [(1,0),(6,1),(12,0),(18,-1),(24,0)],
       'Attack': [(1,0),(6,0.35),(13,1),(19,1),(24,-.5),(31,0)],
       'Hit': [(1,0),(5,1),(10,-.5),(18,0)],
       'Death': [(1,0),(10,.35),(23,.8),(39,1)]
    }
    for clip in names:
        if clip not in definitions:
            raise ValueError('Unknown animation clip '+str(clip))
        act = bpy.data.actions.new(clip)
        arm.animation_data.action = act
        for frame, phase in definitions[clip]:
            bpy.context.scene.frame_set(frame)
            for bname in bone_names:
                pb = arm.pose.bones[bname]
                pb.rotation_mode = 'XYZ'
                x=y=z=0.0
                if clip == 'Idle':
                    if bname=='Spine': x=.027*phase
                    if bname=='Head': y=.028*phase
                    if bname=='UpperArm.L': x=.028*phase
                elif clip in ('Walk','Run'):
                    a= (.42 if clip=='Walk' else .65)*phase
                    if bname=='Thigh.L': x=a
                    if bname=='Thigh.R': x=-a
                    if bname=='Shin.L': x=max(0,-a)*.45
                    if bname=='Shin.R': x=max(0,a)*.45
                    if bname=='UpperArm.L': x=-a*.7
                    if bname=='UpperArm.R': x=a*.7
                    if bname=='Spine': z=.045*phase
                    if bname=='Hips': y=.04*phase
                elif clip=='Attack':
                    if bname=='UpperArm.L': x=-1.05*max(0,phase); y=-.10*phase
                    if bname=='Forearm.L': x=-.24*max(0,phase)
                    if bname=='UpperArm.R': x=-.65*max(0,phase); y=.15*phase
                    if bname=='Forearm.R': x=-.80*max(0,phase)
                    if bname=='Spine': z=-.11*phase
                    if bname=='Head': x=-.11*phase
                elif clip=='Hit':
                    if bname=='Spine': x=.30*phase
                    if bname=='Head': x=-.22*phase
                    if bname.startswith('UpperArm'): z=.23*phase
                elif clip=='Death':
                    if bname=='Root': y=-1.37*phase
                    if bname=='Spine': x=.18*phase
                    if bname.startswith('UpperArm'): y=.23*phase
                    if bname.startswith('Thigh'): x=.28*phase
                pb.rotation_euler=(x,y,z)
                pb.keyframe_insert(data_path='rotation_euler', frame=frame, group=bname)
            if clip in ('Walk','Run'):
                pb=arm.pose.bones['Root']
                pb.location=(0,0,(.04 if clip=='Walk' else .08)*abs(phase))
                pb.keyframe_insert(data_path='location',frame=frame,group='Root')
        arm.animation_data.action = None
        track = arm.animation_data.nla_tracks.new()
        track.name=clip
        strip=track.strips.new(clip,1,act)
        strip.action_frame_start=1
        strip.action_frame_end=definitions[clip][-1][0]
        strip.blend_type='REPLACE'
        strip.extrapolation='HOLD_FORWARD'
        print('ODIN_CLIP',clip,'frames',int(strip.action_frame_end),flush=True)
    bpy.context.scene.frame_set(1)


def make_world(job):
    random.seed(int(job.get('seed', 17)))
    grass=material('tundra','#6F8061')
    earth=material('earth','#63554B')
    timber=material('timber','#6F4630')
    roof=material('slate_roof','#384F4C')
    light=material('stone','#99A49D')
    fire=material('ember','#ED852C')
    leaf=material('conifer','#365B48')
    cube('Ground',(0,0,-.19),(18,18,.35),grass,bevel=.08)
    for i in range(2):
        x=(-3.5 if i==0 else 3.6); y=1.25 if i==0 else 2.4
        cube('Longhouse_'+str(i),(x,y,.9),(3.5,2.5,1.8),timber,bevel=.06)
        # Two pitched roof surfaces (steep gables, lowpoly).
        for s in (-1,1):
            o=cube('Roof_'+str(i)+'_'+str(s),(x+s*.66,y,2.04),(2,2.9,.15),roof)
            o.rotation_euler[1]=s*math.radians(29)
        cube('VikingDoor_'+str(i),(x,y-1.29,.66),(.7,.10,1.3),earth)
        for xx in (-1.6,1.6):
            cylinder('Support', (x+xx,y-1.16,0), (x+xx,y-1.16,1.85),.105,light)
    for n in range(9):
        theta=n*2*math.pi/9
        x=6.8*math.cos(theta);y=6.9*math.sin(theta)
        height=random.uniform(2.0,3.7)
        cylinder('PineTrunk',(x,y,0),(x,y,height*.66),.17,timber)
        for k in range(3):
            z=height*(.47+k*.17)
            cylinder('PineBranches',(x,y,z-.60),(x,y,z+.45),.85*(1-k*.22),leaf,vertices=7,radius_end=0)
    for i in range(14):
        x=random.uniform(-7,7);y=random.uniform(-7,7)
        sphere('Boulder',(x,y,.13),(.15+random.random()*.20,.19,.13),light,segments=9,rings=5)
    for i in range(10):
        x=random.uniform(-2,2)
        cylinder('Palisade',(x,-4.3,0),(x,-4.3,1.15),.13,timber,vertices=7,radius_end=.02)
    for i in range(8):
        angle=i*math.pi/4
        x=1.6*math.cos(angle);y=-.7+1.6*math.sin(angle)
        sphere('CampfireStone',(x,y,.14),(.26,.27,.17),light,segments=8,rings=6)
    cylinder('FireCore',(0,-.7,0),(0,-.7,.67),.25,fire,vertices=8,radius_end=0)
    return None


def export_glb(out_file):
    bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode!='OBJECT' else None
    bpy.ops.object.select_all(action='DESELECT')
    for obj in EXPORT_OBJECTS:
        obj.select_set(True)
    if ARMATURE:
        bpy.context.view_layer.objects.active=ARMATURE
        for track in ARMATURE.animation_data.nla_tracks:
            track.mute=False
    available=set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    opts={'filepath':str(out_file),'export_format':'GLB','export_animations':True}
    for k in ('use_selection','export_selected'):
        if k in available: opts[k]=True
    if 'export_animation_mode' in available:
        opts['export_animation_mode']='NLA_TRACKS'
    elif 'export_nla_strips' in available:
        opts['export_nla_strips']=True
    if 'export_force_sampling' in available:opts['export_force_sampling']=True
    bpy.ops.export_scene.gltf(**opts)
    print('ODIN_EXPORTED',str(out_file),out_file.stat().st_size,flush=True)


def studio_camera(position,target,orthoscale):
    cam_data=bpy.data.cameras.new('PreviewCamera')
    cam=bpy.data.objects.new('PreviewCamera',cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location=position
    direction=Vector(target)-cam.location
    cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    cam.data.type='ORTHO'
    cam.data.ortho_scale=orthoscale
    bpy.context.scene.camera=cam
    return cam


def setup_render(job):
    sc=bpy.context.scene
    sc.render.engine='CYCLES'
    sc.cycles.samples=int(job.get('render_samples',12))
    bpy.context.view_layer.cycles.use_denoising=False  # Ubuntu Blender package lacks OpenImageDenoiser
    sc.render.resolution_x=sc.render.resolution_y=int(job.get('render_size',480))
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'
    sc.world.color=(.15,.17,.22)
    sc.render.film_transparent=False
    try:
        sc.view_settings.view_transform='AgX'
    except (ValueError, TypeError):
        sc.view_settings.view_transform='Standard'
    light_data=bpy.data.lights.new('StudioKey','AREA')
    light=bpy.data.objects.new('StudioKey',light_data)
    bpy.context.collection.objects.link(light)
    light.location=(1,-3,5)
    light_data.energy=850
    light_data.shape='DISK';light_data.size=5.0
    light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
    fill_data=bpy.data.lights.new('Fill','AREA')
    fill=bpy.data.objects.new('Fill',fill_data)
    bpy.context.collection.objects.link(fill)
    fill.location=(-4,2,3);fill_data.energy=500;fill_data.size=6
    fill.rotation_euler=(Vector((0,0,1))-fill.location).to_track_quat('-Z','Y').to_euler()
    return sc


def render_previews(output,job):
    sc=setup_render(job)
    if job['kind']=='character':
        # Preview stage is excluded from export by being created after export_glb().
        stone=material('preview_floor','#454F57')
        stage=cube('PreviewStage',(0,0,-.16),(5,5,.26),stone)
        stage['odin_export']=False
        bpy.context.scene.frame_set(1)
        size=4.4; target=(0,0,1.22)
        viewpoints={
           'front':(0,-6,2.25), 'left':(-6,0,2.15),
           'back':(0,6,2.25), 'threequarter':(-4.3,-5,2.8)
        }
    else:
        size=20;target=(0,0,1.1)
        viewpoints={'front':(0,-24,12),'left':(-24,0,11),'back':(0,24,12),
                    'threequarter':(-19,-23,18)}
    cam=studio_camera(viewpoints['front'],target,size)
    for name,pos in viewpoints.items():
        cam.location=pos
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(output / f'preview_{name}.png')
        bpy.ops.render.render(write_still=True)
        print('ODIN_RENDERED',name,flush=True)
    if ARMATURE:
        for clip, frame in [('Walk',9),('Attack',13),('Attack',23),('Death',27)]:
            for track in ARMATURE.animation_data.nla_tracks:
                track.mute=(track.name!=clip)
            sc.frame_set(frame)
            cam.location=(-4.3,-5,2.8)
            cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
            suffix=('release' if clip=='Attack' and frame==23 else 'draw') if clip=='Attack' else str(frame)
            sc.render.filepath=str(output / f'preview_{clip.lower()}_{suffix}.png')
            bpy.ops.render.render(write_still=True)
            print('ODIN_RENDERED',clip,frame,flush=True)


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser()
    ap.add_argument('--job',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args(argv)
    job=json.loads(Path(a.job).read_text(encoding='utf8'))
    if job.get('schema_version')!=1 or job.get('kind') not in ('character','world'):
        raise ValueError('Unsupported job schema')
    if not re.fullmatch('[a-z][a-z0-9-]{2,40}', job.get('job_id','')):
        raise ValueError('Unsafe job_id')
    if not (128 <= int(job.get('render_size',0)) <= 1024):
        raise ValueError('render_size out of range')
    if not (1 <= int(job.get('render_samples',0)) <= 32):
        raise ValueError('render_samples out of range')
    output=Path(a.output).resolve();output.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    if job['kind']=='character':
        char=character_mesh(job)
        make_clips(char,job['animations'])
    else:make_world(job)
    bpy.context.scene.render.fps=24
    out_file=output / (job['job_id']+'.glb')
    export_glb(out_file)
    render_previews(output,job)
    (output/'build_metadata.json').write_text(json.dumps({
      'job':job['job_id'],'kind':job['kind'],'blender':bpy.app.version_string,
      'exported':out_file.name,'clip_names':job.get('animations',[]),
      'render_note':'Preview snapshots; visual review not guaranteed by this workflow'},indent=2))
    print('ODIN_COMPLETE',job['job_id'],flush=True)

if __name__=='__main__':main()
