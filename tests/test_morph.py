import xml.etree.cElementTree as et
import pytest
import os
import genesis as gs


from ..gssceneloader.context import Context
from ..gssceneloader.geometry.state import State
from ..gssceneloader.shape import get_morph

gs.init(backend=gs.gpu)


class TestMorph:
    @pytest.fixture(scope="session")
    def context(self):
        return Context()

    @pytest.fixture(scope="session")
    def state(self):
        return State()

    def test_box(self, state, context):
        tree = et.parse(os.path.join('data', 'box.xml'))
        element = tree.getroot()  # .find('Box')
        morphs = []
        assert element is not None
        new_state = get_morph(element, state, context, morphs)

        assert len(morphs) == 1
        assert new_state.position.x == 1.1
        assert new_state.position.y == 2.2
        assert new_state.position.z == 3.3

        assert new_state.rotation.x == 0.0
        assert new_state.rotation.y == 0.0
        assert new_state.rotation.z == 0.0

        assert new_state.scale.x == 1.0
        assert new_state.scale.y == 1.0
        assert new_state.scale.z == 1.0

        assert new_state.relative == True
