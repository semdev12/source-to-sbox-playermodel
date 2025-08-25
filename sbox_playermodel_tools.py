bl_info = {
    "name": "Source to S&box Playermodel Utilities",
    "author": "Your Name",
    "version": (2, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Valve Tools",
    "description": "Tools for Source to S&box armature adaptation with pose transfer and vertex group management",
    "category": "Rigging",
}

import bpy
from bpy.types import Panel, Operator

# ============================================
# MODIFY THIS DICTIONARY FOR VERTEX GROUP RENAMING
# ============================================
# Format: "old_name": "new_name"
# Add or modify entries as needed
VERTEX_GROUP_RENAME_MAP = {
    # Valve/Source engine bone names to S&box-friendly names
    "ValveBiped.Bip01_Pelvis": "pelvis",
    "ValveBiped.Bip01_Spine": "spine_0",
    "ValveBiped.Bip01_Spine1": "spine_1",
    "ValveBiped.Bip01_Spine2": "spine_2",
    "ValveBiped.Bip01_Spine4": "chest",
    "ValveBiped.Bip01_Neck1": "neck_0",
    "ValveBiped.Bip01_Head1": "head",
    
    # Left arm
    "ValveBiped.Bip01_L_Clavicle": "clavicle_L",
    "ValveBiped.Bip01_L_UpperArm": "arm_upper_L",
    "ValveBiped.Bip01_L_Forearm": "arm_lower_L",
    "ValveBiped.Bip01_L_Hand": "hand_L",
    
    # Right arm
    "ValveBiped.Bip01_R_Clavicle": "clavicle_R",
    "ValveBiped.Bip01_R_UpperArm": "arm_upper_R",
    "ValveBiped.Bip01_R_Forearm": "arm_lower_R",
    "ValveBiped.Bip01_R_Hand": "hand_R",
    
    # Left leg
    "ValveBiped.Bip01_L_Thigh": "leg_upper_L",
    "ValveBiped.Bip01_L_Calf": "leg_lower_L",
    "ValveBiped.Bip01_L_Foot": "ankles_L",
    "ValveBiped.Bip01_L_Toe0": "ball_L",
    
    # Right leg
    "ValveBiped.Bip01_R_Thigh": "leg_upper_R",
    "ValveBiped.Bip01_R_Calf": "leg_lower_R",
    "ValveBiped.Bip01_R_Foot": "ankles_R",
    "ValveBiped.Bip01_R_Toe0": "ball_R",
    
    # Left hand fingers - Thumb
    "ValveBiped.Bip01_L_Finger0": "finger_thumb_0_L",
    "ValveBiped.Bip01_L_Finger01": "finger_thumb_1_L",
    "ValveBiped.Bip01_L_Finger02": "finger_thumb_2_L",
    
    # Left hand fingers - Index
    "ValveBiped.Bip01_L_Finger1": "finger_index_0_L",
    "ValveBiped.Bip01_L_Finger11": "finger_index_1_L",
    "ValveBiped.Bip01_L_Finger12": "finger_index_2_L",
    
    # Left hand fingers - Middle
    "ValveBiped.Bip01_L_Finger2": "finger_middle_0_L",
    "ValveBiped.Bip01_L_Finger21": "finger_middle_1_L",
    "ValveBiped.Bip01_L_Finger22": "finger_middle_2_L",
    
    # Left hand fingers - Ring
    "ValveBiped.Bip01_L_Finger3": "finger_ring_0_L",
    "ValveBiped.Bip01_L_Finger31": "finger_ring_1_L",
    "ValveBiped.Bip01_L_Finger32": "finger_ring_2_L",
    
    # Left hand fingers - Pinky
    "ValveBiped.Bip01_L_Finger4": "finger_pinky_0_L",
    "ValveBiped.Bip01_L_Finger41": "finger_pinky_1_L",
    "ValveBiped.Bip01_L_Finger42": "finger_pinky_2_L",
    
    # Right hand fingers - Thumb
    "ValveBiped.Bip01_R_Finger0": "finger_thumb_0_R",
    "ValveBiped.Bip01_R_Finger01": "finger_thumb_1_R",
    "ValveBiped.Bip01_R_Finger02": "finger_thumb_2_R",
    
    # Right hand fingers - Index
    "ValveBiped.Bip01_R_Finger1": "finger_index_0_R",
    "ValveBiped.Bip01_R_Finger11": "finger_index_1_R",
    "ValveBiped.Bip01_R_Finger12": "finger_index_2_R",
    
    # Right hand fingers - Middle
    "ValveBiped.Bip01_R_Finger2": "finger_middle_0_R",
    "ValveBiped.Bip01_R_Finger21": "finger_middle_1_R",
    "ValveBiped.Bip01_R_Finger22": "finger_middle_2_R",
    
    # Right hand fingers - Ring
    "ValveBiped.Bip01_R_Finger3": "finger_ring_0_R",
    "ValveBiped.Bip01_R_Finger31": "finger_ring_1_R",
    "ValveBiped.Bip01_R_Finger32": "finger_ring_2_R",
    
    # Right hand fingers - Pinky
    "ValveBiped.Bip01_R_Finger4": "finger_pinky_0_R",
    "ValveBiped.Bip01_R_Finger41": "finger_pinky_1_R",
    "ValveBiped.Bip01_R_Finger42": "finger_pinky_2_R",
    
    # Additional common Source bones
    "ValveBiped.forward": "root_motion",
    "ValveBiped.Bip01_L_Elbow": "arm_lower_L_twist1",
    "ValveBiped.Bip01_R_Elbow": "arm_lower_R_twist1",
    "ValveBiped.Bip01_L_Ulna": "arm_lower_L_twist2",
    "ValveBiped.Bip01_R_Ulna": "arm_lower_R_twist2",
    
    # Add more mappings as needed...
}

# ============================================
# OPERATORS
# ============================================

class VALVE_OT_adapt_source_armature(Operator):
    """Copy pose from adaptation armature to current, then change modifier target and apply"""
    bl_idname = "valve.adapt_source_armature"
    bl_label = "Adapt Source Armature"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH')
    
    def execute(self, context):
        obj = context.active_object
        
        # Find the armature modifier
        armature_modifier = None
        for modifier in obj.modifiers:
            if modifier.type == 'ARMATURE':
                armature_modifier = modifier
                break
        
        if not armature_modifier:
            self.report({'ERROR'}, "No Armature modifier found on selected mesh")
            return {'CANCELLED'}
        
        # Get the current armature from the modifier
        current_armature = armature_modifier.object
        if not current_armature:
            self.report({'ERROR'}, "No armature assigned to the Armature modifier")
            return {'CANCELLED'}
        
        # Find the adaptation armature
        target_armature_name = "SourceToSbox_AdaptationArmature"
        adaptation_armature = bpy.data.objects.get(target_armature_name)
        
        if not adaptation_armature:
            self.report({'ERROR'}, f"Armature '{target_armature_name}' not found in scene")
            return {'CANCELLED'}
        
        # Store original selection and mode
        original_active = context.view_layer.objects.active
        original_mode = context.mode
        
        try:
            # STEP 1: Copy pose from adaptation armature to current armature
            print(f"Copying pose from '{target_armature_name}' to '{current_armature.name}'")
            
            # Select and activate the adaptation armature
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            adaptation_armature.select_set(True)
            context.view_layer.objects.active = adaptation_armature
            
            # Enter pose mode and select all bones
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='SELECT')
            
            # Copy the pose
            bpy.ops.pose.copy()
            print(f"Copied pose from '{target_armature_name}'")
            
            # Switch to the current armature
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            current_armature.select_set(True)
            context.view_layer.objects.active = current_armature
            
            # Enter pose mode and select all bones
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='SELECT')
            
            # Paste the pose
            bpy.ops.pose.paste(flipped=False)
            print(f"Pasted pose to '{current_armature.name}'")
            
            # Return to object mode and reselect the mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # STEP 2: Change the armature modifier target
            old_armature_name = current_armature.name
            armature_modifier.object = adaptation_armature
            print(f"Changed armature target from '{old_armature_name}' to '{target_armature_name}'")
            
            # STEP 3: Apply the modifier
            bpy.ops.object.modifier_apply(modifier=armature_modifier.name)
            self.report({'INFO'}, f"Successfully copied pose, adapted armature and applied modifier")
            print(f"Applied armature modifier '{armature_modifier.name}'")
            
        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {str(e)}")
            # Try to restore original state
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                original_active.select_set(True)
                context.view_layer.objects.active = original_active
            except:
                pass
            return {'CANCELLED'}
        
        return {'FINISHED'}


class VALVE_OT_rename_vertex_groups(Operator):
    """Mass rename vertex groups based on the defined mapping"""
    bl_idname = "valve.rename_vertex_groups"
    bl_label = "Rename Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH')
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj.vertex_groups:
            self.report({'WARNING'}, "No vertex groups found on selected object")
            return {'CANCELLED'}
        
        renamed_count = 0
        skipped_count = 0
        
        # Create a list of vertex groups to rename (to avoid modifying while iterating)
        groups_to_rename = []
        for vg in obj.vertex_groups:
            if vg.name in VERTEX_GROUP_RENAME_MAP:
                new_name = VERTEX_GROUP_RENAME_MAP[vg.name]
                groups_to_rename.append((vg, new_name))
        
        # Perform the renaming
        for vg, new_name in groups_to_rename:
            old_name = vg.name
            try:
                # Check if target name already exists
                if new_name not in obj.vertex_groups:
                    vg.name = new_name
                    renamed_count += 1
                    print(f"Renamed: {old_name} -> {new_name}")
                else:
                    skipped_count += 1
                    print(f"Skipped: {old_name} (target name {new_name} already exists)")
            except Exception as e:
                self.report({'ERROR'}, f"Error renaming {old_name}: {str(e)}")
        
        self.report({'INFO'}, f"Renamed {renamed_count} vertex groups, skipped {skipped_count}")
        return {'FINISHED'}


class VALVE_OT_fix_foot_vertex_groups(Operator):
    """Create twist vertex groups and add weight mix modifiers for foot deformation"""
    bl_idname = "valve.fix_foot_vertex_groups"
    bl_label = "Fix Foot Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH')
    
    def execute(self, context):
        obj = context.active_object
        
        # Define the vertex groups to create and their source groups
        twist_groups = {
            "leg_lower_L_twist1": "ankles_L",
            "leg_lower_R_twist1": "ankles_R"
        }
        
        created_groups = []
        
        # Create new vertex groups
        for new_group_name, source_group_name in twist_groups.items():
            # Check if the group already exists
            if new_group_name not in obj.vertex_groups:
                new_vg = obj.vertex_groups.new(name=new_group_name)
                created_groups.append(new_group_name)
                print(f"Created vertex group: {new_group_name}")
            else:
                print(f"Vertex group '{new_group_name}' already exists")
        
        # Add weight mix modifiers
        modifiers_added = []
        
        for target_group, source_group in twist_groups.items():
            # Check if source vertex group exists
            if source_group not in obj.vertex_groups:
                self.report({'WARNING'}, f"Source vertex group '{source_group}' not found")
                continue
            
            # Create a unique modifier name
            modifier_name = f"WeightMix_{source_group}_to_{target_group}"
            
            # Check if modifier already exists
            if modifier_name in obj.modifiers:
                print(f"Modifier '{modifier_name}' already exists")
                continue
            
            # Add the weight mix modifier
            weight_mix = obj.modifiers.new(name=modifier_name, type='VERTEX_WEIGHT_MIX')
            
            # Configure the modifier
            weight_mix.vertex_group_a = target_group  # Target group (where weights will be added)
            weight_mix.vertex_group_b = source_group  # Source group (weights to add)
            weight_mix.mix_mode = 'ADD'  # Add mode
            weight_mix.mix_set = 'ALL'  # Apply to all vertices
            weight_mix.default_weight_a = 0.0  # Default weight for group A
            weight_mix.default_weight_b = 0.0  # Default weight for group B
            
            modifiers_added.append(modifier_name)
            print(f"Added weight mix modifier: {modifier_name}")
        
        # Report results
        if created_groups or modifiers_added:
            self.report({'INFO'}, 
                       f"Created {len(created_groups)} vertex groups, "
                       f"added {len(modifiers_added)} modifiers")
        else:
            self.report({'WARNING'}, "No changes made - groups and modifiers may already exist")
        
        return {'FINISHED'}


class VALVE_OT_fix_bone_roll(Operator):
    """Subtract 90 degrees from all bone rolls in the selected armature"""
    bl_idname = "valve.fix_bone_roll"
    bl_label = "Fix Bone Rolls (-90°)"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'ARMATURE')
    
    def execute(self, context):
        armature = context.active_object
        
        # Store current mode
        original_mode = context.mode
        
        # Switch to Edit Mode to modify bone rolls
        bpy.ops.object.mode_set(mode='EDIT')
        
        import math
        
        # Get all edit bones
        edit_bones = armature.data.edit_bones
        
        # Subtract 90 degrees (in radians) from each bone's roll
        bones_modified = 0
        for bone in edit_bones:
            old_roll = bone.roll
            bone.roll = bone.roll - math.radians(90)
            bones_modified += 1
            print(f"Bone '{bone.name}': Roll changed from {math.degrees(old_roll):.2f}° to {math.degrees(bone.roll):.2f}°")
        
        # Return to original mode
        bpy.ops.object.mode_set(mode=original_mode.replace('_EDIT', '').replace('_POSE', '').replace('_PAINT', ''))
        
        self.report({'INFO'}, f"Modified roll for {bones_modified} bones")
        return {'FINISHED'}


# ============================================
# UI PANEL
# ============================================

class VALVE_PT_tools_panel(Panel):
    """Creates a Panel in the 3D viewport sidebar"""
    bl_label = "Valve Bones Tools"
    bl_idname = "VALVE_PT_tools_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Valve Tools"
    
    def draw(self, context):
        layout = self.layout
        
        # Source to S&box Adaptation Section
        box = layout.box()
        box.label(text="Source to S&box Adaptation", icon='MOD_ARMATURE')
        
        col = box.column()
        
        # Show info about selected object
        if context.active_object:
            if context.active_object.type == 'MESH':
                obj = context.active_object
                col.label(text=f"Selected: {obj.name}", icon='OBJECT_DATA')
                
                # Check for armature modifier
                has_armature = any(mod.type == 'ARMATURE' for mod in obj.modifiers)
                if has_armature:
                    col.label(text="Has Armature modifier", icon='CHECKMARK')
                else:
                    col.label(text="No Armature modifier", icon='X')
                    
                # Check if adaptation armature exists
                if "SourceToSbox_AdaptationArmature" in bpy.data.objects:
                    col.label(text="Adaptation armature found", icon='CHECKMARK')
                else:
                    col.label(text="Adaptation armature missing!", icon='ERROR')
            else:
                col.label(text="Select a mesh object", icon='INFO')
        else:
            col.label(text="No object selected", icon='INFO')
        
        col.separator()
        col.operator("valve.adapt_source_armature", icon='MOD_ARMATURE')
        
        # Vertex Group Operations Section
        box = layout.box()
        box.label(text="Vertex Group Operations", icon='GROUP_VERTEX')
        
        col = box.column()
        
        if context.active_object and context.active_object.type == 'MESH':
            obj = context.active_object
            if obj.vertex_groups:
                col.label(text=f"Vertex Groups: {len(obj.vertex_groups)}")
            else:
                col.label(text="No vertex groups", icon='ERROR')
        
        col.separator()
        row = col.row(align=True)
        row.operator("valve.rename_vertex_groups", icon='FILE_REFRESH')
        
        col.separator()
        row = col.row(align=True)
        row.operator("valve.fix_foot_vertex_groups", icon='MOD_VERTEX_WEIGHT')
        
        # Bone Roll Fixing Section
        box = layout.box()
        box.label(text="Bone Roll Fixing", icon='BONE_DATA')
        
        col = box.column()
        
        # Show info about selected armature
        if context.active_object:
            if context.active_object.type == 'ARMATURE':
                arm = context.active_object
                col.label(text=f"Selected: {arm.name}", icon='ARMATURE_DATA')
                col.label(text=f"Bones: {len(arm.data.bones)}")
            else:
                col.label(text="Select an armature", icon='INFO')
        else:
            col.label(text="No object selected", icon='INFO')
        
        col.separator()
        col.operator("valve.fix_bone_roll", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        
        # Instructions
        layout.separator()
        box = layout.box()
        box.label(text="Workflow:", icon='QUESTION')
        box.scale_y = 0.9
        col = box.column(align=True)
        col.label(text="1. Select mesh with Source armature")
        col.label(text="2. Click 'Adapt Source Armature'")
        col.label(text="3. Click 'Rename Vertex Groups'")
        col.label(text="4. Click 'Fix Foot Vertex Groups'")
        col.label(text="5. Select armature, fix bone rolls if needed")


# ============================================
# REGISTRATION
# ============================================

classes = [
    VALVE_OT_adapt_source_armature,
    VALVE_OT_rename_vertex_groups,
    VALVE_OT_fix_foot_vertex_groups,
    VALVE_OT_fix_bone_roll,
    VALVE_PT_tools_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()