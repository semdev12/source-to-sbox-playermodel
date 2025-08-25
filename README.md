# Source/Gmod To S&Box Playermodel Utilities (BETA)
Utilities to transition a Source/Gmod playermodel into S&amp;box

This repo allows you to turn a playermodel from Gmod or any Source Engine game into a playermodel compatible with the Player Controller and the default citizen/citizen_human models from S&box through bone merging.
The .blend file comes with:
- A fixed version of the S&box armature with properly rotated Bone rolls (without this, all bones in the playermodel would be rotated weirdly when bonemerged)
- An already posed Source armature compatible with the default A-pose of S&box that allows you to transition your mesh without having to set it up manually

# ⚠️ WARNING ⚠️
This works with male armatures so far. Female armatures don't pose properly yet.

## Prerequisites
- Install Blender (duh)
- Install [SourceIO](https://github.com/REDxEYE/SourceIO) for importing .mdl files
- Install the python script included in the repo

## Quick Guide (using the provided .blend file)
- import .mdl with SourceIO
    - <img height="350" alt="image" src="https://github.com/user-attachments/assets/9509753f-8e7a-478e-a15d-3c82a08fbe64" />
    - if the model has multiple meshes, it's probably best to join them together (Ctrl+J)
- scale the armature to match the S&box armature (I noticed scaling by 50 always works well)
- Apply Scale (Ctrl+A -> Scale)
- Switch the target of the Source mesh's Armature modifier to "*SourceToSbox_AdaptationArmature*"
  - (This should instantly snap the mesh to match the s&box A-pose)
  - <img width="653" height="260" alt="image" src="https://github.com/user-attachments/assets/bf2fdba1-52a1-4d17-aaa9-61802acbf24e" />

- Apply the armature modifier
- Rename every vertex group in the Source mesh to match the S&box bones naming convention
  - My python script comes with a "Rename Vertex Groups" button which automates this for you:
  - Click the Source Mesh
  - Press N and click on "Valve Tools"
  - Press "Rename Vertex Groups"
  - All the Source vertex groups ("ValveBiped.Bip01_*") will be converted for s&box
- Use Weight Mix modifier to fix spine issues
  - Because the S&box's rig uses 3 spine bones and Source playermodels use 4, you're gonna have to merge the weights of 2 vertex groups and delete one of them
  - For example ValveBiped.Bip01_Spine2 with ValveBiped.Bip01_Spine4 and then delete Spine4
- Add vertex groups for "leg_lower_L_twist1" and "leg_lower_R_twist1"
- Use Weight Mix Modifier to add weights of "ankles_L/R" to "leg_lower_L/R_twist1"
  - My python script comes with the "Fix Foot Vertex Groups" which automates these 2 steps
- Add an Armature modifier to the Source mesh, this time targeted to "*Sbox_HumanArmature_FixedRolls*"
- Everything should be ready. Ctrl-click your mesh and the sbox armature and export as FBX using these settings:
- <img height="500" alt="image" src="https://github.com/user-attachments/assets/faee66f0-86a9-4328-9360-fc8937b4e7d1" />

## Use in S&box
- Import the .fbx in your project and create the .vmdl
- Drop a Player Controller on your scene that uses the citizen_human.vmdl
- Drag and drop your playermodel .vmdl in your scene
- On the SkinnedModelRenderer, change the "Bone Merge Target" to the Player Controller's "Body" gameobject
- Disable rendering of the default Player Controller's playermodel by changing its Tint to a color with alpha at 0
- <img width="427" height="254" alt="image" src="https://github.com/user-attachments/assets/1ab0ef12-8c86-4405-a10b-ad2bf169d0ff" />



