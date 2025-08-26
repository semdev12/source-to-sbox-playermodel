# Source/Gmod To S&Box Playermodel Utilities (BETA)
Utilities to transition a Source/Gmod playermodel into S&amp;box

This repo allows you to turn a playermodel from Gmod or any Source Engine game into a playermodel compatible with the Player Controller and the default citizen/citizen_human models from S&box through bone merging.
The .blend file comes with:
- A fixed version of the S&box armature with properly rotated Bone rolls (without this, all bones in the playermodel would be rotated weirdly when bonemerged)
- An already posed Source armature compatible with the default A-pose of S&box that allows you to transition your mesh without having to set it up manually
- An "Adaptation Armature" which allows to deploy the playermodel in s&box without touching the mesh's vertex groups or weight painting

# ⚠️ WARNING ⚠️
This works with male armatures so far. Female armatures don't pose properly yet.

## Prerequisites
- Install Blender (duh)
- Install [SourceIO](https://github.com/REDxEYE/SourceIO) for importing .mdl files

## Quick Guide (using the provided .blend file)
- import .mdl with SourceIO
    - <img height="350" alt="image" src="https://github.com/user-attachments/assets/9509753f-8e7a-478e-a15d-3c82a08fbe64" />
    - if the model has multiple meshes, it's probably best to join them together (Ctrl+J)
- scale the armature to match the S&box armature (I noticed scaling by 50 always works well)
- Apply Scale (Ctrl+A -> Scale)
- Switch the target of the Source mesh's Armature modifier to "*SourceArmature_Rotated*"
  - (This should instantly snap the mesh to match the s&box A-pose)
- Apply the armature modifier
- Add another Armature modifier, this time targeted to "*AdaptationArmature*"
- Everything should be ready. Ctrl-click your mesh and the adaptation armature and export as FBX using these settings:
- <img height="500" alt="image" src="https://github.com/user-attachments/assets/faee66f0-86a9-4328-9360-fc8937b4e7d1" />

## Use in S&box
- Import the fbx of the playermodel in your project and create the .vmdl
- Import the "SourceSbox_AdaptationArmature.fbx"
- Open the playermodel in the editor and in the outliner add a node "Import Skeleton..."
    - <img width="899" height="529" alt="image" src="https://github.com/user-attachments/assets/5887280b-cfb8-4109-8a52-0088503076a2" />
- When prompted, choose the "SourceSbox_AdaptationArmature.fbx"
- Drop a Player Controller on your scene that uses the citizen_human.vmdl
- Drag and drop the playermodel .vmdl in your scene
- On the SkinnedModelRenderer of the playermodel, change the "Bone Merge Target" to the Player Controller's "Body" gameobject
- Disable rendering of the default Player Controller's playermodel by changing its Tint alpha to 0 or by disabling "Game" on the "Advanced Rendering" section
- <img width="325" alt="image" src="https://github.com/user-attachments/assets/c4fa117f-1eeb-4b75-90d4-1952bdcd2303" />




