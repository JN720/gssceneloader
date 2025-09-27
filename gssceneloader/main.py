import xml.etree.cElementTree as et
import genesis.options.morphs as morphs
from .context import Context
from .geometry.state import State

from .shape import get_morph


def get_morphs(element: et.Element, morphs: list[morphs.Morph], state: State, context: Context, ignore_malformed=False) -> list[morphs.Morph]:
    state = get_morph(element, state, context, morphs)
    for child in element:
        get_morphs(child, morphs, state, context, ignore_malformed)

    return morphs


def load(xml: str | et.ElementTree, context: Context | None = None, state: State | None = None, ignore_malformed=False) -> list[morphs.Morph]:
    tree: et.ElementTree
    if type(xml) is str:
        tree = et.parse(xml)
    elif type(xml) is et.ElementTree:
        tree = xml
    else:
        raise ValueError(f'Expected str or ElementTree, got {type(xml)}')

    if context is None:
        context = Context()

    context_element: et.Element = tree.find('context')
    if not context_element is None:
        context.fill(context_element, ignore_malformed)

    if state is None:
        state = State()

    scene_element = tree.find('scene')
    if scene_element is None:
        raise ValueError('No scene element found')

    return get_morphs(scene_element, [], state, context, ignore_malformed)
