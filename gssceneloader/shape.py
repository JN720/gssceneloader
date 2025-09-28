import xml.etree.cElementTree as et
import torch
import genesis.options.morphs as morphs
from genesis.utils.geom import xyz_to_quat, quat_to_xyz, transform_by_quat, inv_quat, transform_quat_by_quat
from typing import Callable
from .context import Context
from .geometry import State, StaticVector3


def get_scene(position: torch.Tensor, quat: torch.Tensor, scale: torch.Tensor) -> morphs.Morph | None:
    pass


def get_box(position: torch.Tensor, quat: torch.Tensor, scale: torch.Tensor) -> morphs.Morph | None:
    return morphs.Box(pos=position, quat=quat, size=scale)


def get_cylinder(position: torch.Tensor, quat: torch.Tensor, scale: torch.Tensor) -> morphs.Morph | None:
    return morphs.Cylinder(pos=position, quat=quat, radius=scale[0], height=scale[2])


def get_sphere(position: torch.Tensor, quat: torch.Tensor, scale: torch.Tensor) -> morphs.Morph | None:
    return morphs.Sphere(pos=position, quat=quat, radius=scale[0])


def get_plane(position: torch.Tensor, quat: torch.Tensor, scale: torch.Tensor) -> morphs.Morph | None:
    return morphs.Plane(pos=position, quat=quat, plane_size=(scale[0], scale[1]))


TAGS: dict[str, Callable[[torch.Tensor, torch.Tensor, torch.Tensor], morphs.Morph | None]] = {
    'scene': get_scene,
    'box': get_box,
    'cylinder': get_cylinder,
    'sphere': get_sphere,
    'plane': get_plane
}


def transform(position, rotation, scale, relative, parent_state: State, context: Context) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, bool]:
    if not relative:
        return position, rotation, scale

    rot_tensor = rotation.get_tensor(context)
    quat = xyz_to_quat(rot_tensor)
    # Rotate the scaled offset to get the position
    pos = parent_state.position.get_tensor(context) + transform_by_quat(position.get_tensor(
        context) * parent_state.scale.get_tensor(context), quat)
    # COmpose the rotations to get the rotation of the object
    rot = transform_quat_by_quat(
        quat, xyz_to_quat(parent_state.rotation.get_tensor(context)))

    scl = parent_state.scale.get_tensor(context) * scale.get_tensor(context)
    return pos, rot, scl


def get_morph(element: et.Element, state: State, context: Context, morphs: list[morphs.Morph], ignore_malformed=False) -> State:
    state_info = state.reconcile(element, ignore_malformed)
    pos, quat, scale = transform(*state_info, state, context)
    rotation = quat_to_xyz(quat)
    morph = TAGS[element.tag.lower()](
        (*pos.cpu(),), (*quat.cpu(),), (*scale.cpu(),))
    if morph is not None:
        morphs.append(morph)

    new_state = State(StaticVector3(*pos), StaticVector3(*
                      rotation), StaticVector3(*scale), state_info[3])
    return new_state
