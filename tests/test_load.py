import xml.etree.cElementTree as et
import torch
import os
import genesis as gs
from genesis.options.morphs import Box, Cylinder


from ..gssceneloader import load
from ..gssceneloader.geometry.state import State
from ..gssceneloader.shape import get_morph


class TestLoad:
    def test_load_basic(self):
        morphs = load(os.path.join('data', 'basic.xml'))
        assert len(morphs) == 2
        assert type(morphs[0]) is Box
        assert type(morphs[1]) is Cylinder

        assert (torch.Tensor(morphs[0].pos).cpu() -
                torch.tensor([1.1, 2.2, 3.3]).cpu()).abs().sum() < 1e-5

        assert (torch.Tensor(morphs[0].size).cpu() -
                2).abs().sum() < 1e-5
        # The scale of the parent box is 2, so the x offset of 0.1 should be doubled
        assert (torch.Tensor(morphs[1].pos).cpu() -
                torch.tensor([1.3, 2.2, 3.3]).cpu()).abs().sum() < 1e-5
        # The 2x size in the parent should compound with the 3x size of the child
        assert (torch.Tensor([morphs[1].height, morphs[1].radius]).cpu() -
                6).abs().sum() < 1e-5
