# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import bpy
import pathlib
from bpy.types import Context, Event, Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

bl_info = {
    "name" : "MayaConfig",
    "author" : "euph",
    "description" : "Maya快捷键",
    "blender" : (3, 51, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "3D View"
}

MayaConfig=True
AddOnEnable=True

class MayaBlender_OT_Config(bpy.types.Operator):
    bl_idname = "wm.mayaconfig"
    bl_label = "Minimal Operator"

    def execute(self, context):

        if AddOnEnable:
           # 打开常用插件 新功能 bpy.ops.preferences.addon_enable/addon_disable
           bpy.ops.preferences.addon_enable(module="node_arrange")
           bpy.ops.preferences.addon_enable(module="node_presets")
           bpy.ops.preferences.addon_enable(module="node_wrangler")
           bpy.ops.preferences.addon_enable(module="mesh_looptools")
           bpy.ops.preferences.addon_enable(module="io_import_images_as_planes")
           bpy.ops.preferences.addon_enable(module="magic_uv")
           bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
           bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
           bpy.ops.preferences.addon_enable(module="add_mesh_geodesic_domes")
        #bpy.ops.wm.keyconfig_preset_add(name="mayaConfig");
        #切换为Blender
        
        if MayaConfig:
        #改造blender快捷键

           path= bpy.app.binary_path
           version=bpy.app.version
           verStr=str(version[0])+"."+str(version[1])
           print(path)
           pathObj= pathlib.Path(path).parent.joinpath(verStr,"scripts","presets","keyconfig","Blender.py")
           Originconfig=str(pathObj)
           bpy.ops.preferences.keyconfig_activate(filepath=Originconfig)

           bpy.ops.wm.keyconfig_preset_add(name="MayaConfig")
          
           wm = bpy.context.window_manager
           kc = wm.keyconfigs.user
           #启用设置
           context.preferences.view.language='zh_CN'
           context.preferences.view.use_translate_interface=True
           context.preferences.view.show_tooltips_python=True
           context.preferences.view.show_tooltips=True
           context.preferences.inputs.use_auto_perspective=False

           #改键位
           #移除帧数中的帧偏移 screen.frame_offset 与ALt+滚轮缩放冲突
           frameKm = kc.keymaps['Frames']
           for item in frameKm.keymap_items:
            if item.idname=="screen.frame_offset" and item.alt==True:
               frameKm.keymap_items.remove(item)

           km = kc.keymaps['3D View']

           kmi = km.keymap_items.new(
            idname="view3d.rotate",
            type="LEFTMOUSE",
            value="PRESS",
            shift=False,
            ctrl=False,
            alt = True,
            oskey=False
            )
           
           kmi = km.keymap_items.new(
            idname="view3d.move",
            type="MIDDLEMOUSE",
            value="PRESS",
            shift=False,
            ctrl=False,
            alt = True,
            oskey=False
            )
           
           
           kmi = km.keymap_items.new(
            idname="view3d.zoom",
            type="WHEELUPMOUSE",
            value="PRESS",
            shift=False,
            ctrl=False,
            alt = True,
            oskey=False
            )
           kmi.properties.__setitem__("delta", 1)

           kmi = km.keymap_items.new(
            idname="view3d.zoom",
            type="WHEELDOWNMOUSE",
            value="PRESS",
            shift=False,
            ctrl=False,
            alt = True,
            oskey=False,
            )
           
           kmi.properties.__setitem__("delta", -1)

           #ALt+侧键切换透视
           kmi = km.keymap_items.new(
           idname="view3d.view_persportho",
           type="BUTTON4MOUSE",
           value="PRESS",
           shift=False,
           ctrl=False,
           alt = True,
           oskey=False,
           )


           # 翻译切换快捷键 
           kmi = km.keymap_items.new(
           idname="wm.context_toggle",
           type="T",
           value="PRESS",
           shift=True,
           ctrl=True,
           alt = True,
           oskey=False,
            )

           kmi.properties.__setitem__("data_path", "preferences.view.use_translate_interface")
          

        else:
           path= bpy.app.binary_path
           version=bpy.app.version
           verStr=str(version[0])+"."+str(version[1])
           print(path)
           pathObj= pathlib.Path(path).parent.joinpath(verStr,"scripts","presets","keyconfig","Blender.py")
           Originconfig=str(pathObj)
           bpy.ops.preferences.keyconfig_activate(filepath=Originconfig)


        #保存
        bpy.ops.wm.save_userpref()
        #N面板
        return {'FINISHED'}

class Maya_PT_proc(AddonPreferences):
    bl_idname = __name__
    boolean: BoolProperty(
        name="MayaKeyMap",
        default=False,
    )

    addonEnable: BoolProperty(
        name="常用插件启动",# 下拉列表
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "boolean")
        layout.prop(self, "addonEnable")
        global MayaConfig
        MayaConfig=self.boolean
        global AddOnEnable
        AddOnEnable=self.addonEnable
        row= layout.row()
        row.operator(MayaBlender_OT_Config.bl_idname,text="Save",icon="CUBE")



classes=[
    MayaBlender_OT_Config,
    Maya_PT_proc,
]

def register():
    print("Hello Blender")
    for item in classes:
        bpy.utils.register_class(item)
     
    ...

def unregister():
    print("Exit Blender")
    for item in classes:
        bpy.utils.unregister_class(item)
    
    ...
