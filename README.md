# Source/Gmod To S&Box Playermodel Utilities
![readme_new](https://github.com/user-attachments/assets/421a01c1-b6c8-4fe4-bd01-6f3e60f7fc31)



This repo allows you to turn a playermodel from Gmod or any Source Engine game into a playermodel compatible with the Player Controller and the default citizen/citizen_human models from S&box through bone merging.
The .blend file comes with:
- A fixed version of the S&box armature with properly rotated Bone rolls (without this, all bones in the playermodel would be rotated weirdly when bonemerged)
- An already posed Source armature compatible with the default A-pose of S&box that allows you to transition your mesh without having to set it up manually
- An "Adaptation Armature" which allows to deploy the playermodel in s&box without touching the mesh's vertex groups or weight painting

## Prerequisites
- Install Blender (duh)
- Install [SourceIO](https://github.com/REDxEYE/SourceIO) for importing .mdl files

## Quick Guide (using the provided .blend file)
### Importing
- import .mdl with SourceIO
    - <img height="350" alt="image" src="https://github.com/user-attachments/assets/9509753f-8e7a-478e-a15d-3c82a08fbe64" />
- delete everything but the mesh
- scale the mesh to match the S&box armature (If the model is male, scale it by 50. If it's female, scale it by 52)
- Apply Scale (Ctrl+A -> Scale)
### Posing the Armature
First off, pose the armature to match the same pose as the s&box citizen. The project comes with an already posed source armature so you don't have to do this manually.
- Switch the target of the Source mesh's Armature modifier to "*SourceArmature_[Male/Female]_Rotated*"
  - (This should instantly snap the mesh to match the s&box A-pose)
- Apply the armature modifier
- Add another Armature modifier, this time targeted to "*SourceToSbox_[Male/Female]AdapterRig*"
- Everything should be ready. Ctrl-click your mesh and the adapter rig and export as FBX using these settings:
- <img height="500" alt="image" src="https://github.com/user-attachments/assets/faee66f0-86a9-4328-9360-fc8937b4e7d1" />

### Import your playermodel in S&box
- Import the fbx of the playermodel in your project and create the .vmdl
- Import the male/female adapter rig as well (but do not make a vmdl)
- Open the playermodel in the editor and in the outliner add a node "Import Skeleton..."
    - <img width="899" height="529" alt="image" src="https://github.com/user-attachments/assets/5887280b-cfb8-4109-8a52-0088503076a2" />
- When prompted, choose the adapter rig
- Now the vmdl should properly bone merge
### Using your playermodel
Playermodels in s&box can be considered as big pieces of clothing, and as such they can be integrated with the in-game clothing system.
- Drop a Player Controller on your scene (or anything that uses a citizen_human SkinnedModelRenderer)
- Add a Dresser component to the player and link it to the SkinnedModelRenderer
- Create a Clothing Definition in your project
- In the "General/Clothing Setup", assign the .vmdls and set the "Hide Body" to include all options 




