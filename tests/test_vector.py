import pytest
import torch

from ..gssceneloader.geometry.state import State
from ..gssceneloader.geometry.vector3 import Vector3, StaticVector3, RandomVector3, RandomRangeVector3
from ..gssceneloader.context import Context


class TestVector:
    @pytest.fixture(scope="session")
    def context(self):
        return Context()

    def test_construct(self):
        vec = StaticVector3(1.1, 2.2, 3.3)
        assert vec.x == 1.1
        assert vec.y == 2.2
        assert vec.z == 3.3

    def test_get_tensor(self, context):
        vec = StaticVector3(1.1, 2.2, 3.3)
        tensor = vec.get_tensor(context)
        assert tensor.shape == (3,)
        assert tensor[0] == 1.1
        assert tensor[1] == 2.2
        assert tensor[2] == 3.3

    def test_get(self, context):
        vec = StaticVector3(1.1, 2.2, 3.3)
        x, y, z = vec.get(context)
        assert x == 1.1
        assert y == 2.2
        assert z == 3.3

    def test_random_vector(self, context):
        vec = RandomVector3()
        tensor = vec.get_tensor(context)
        assert tensor.shape == (3,)
        assert tensor[0] != 0
        assert tensor[1] != 0
        assert tensor[2] != 0

        new_tensor = vec.get_tensor(context)
        assert tensor is new_tensor

    def test_random_range_vector(self, context):
        vec = RandomRangeVector3(StaticVector3(
            1.1, 2.2, 3.3), StaticVector3(4.4, 5.5, 6.6))
        tensor = vec.get_tensor(context)
        assert tensor.shape == (3,)
        assert tensor[0] >= 1.1
        assert tensor[0] <= 4.4
        assert tensor[1] >= 2.2
        assert tensor[1] <= 5.5
        assert tensor[2] >= 3.3
        assert tensor[2] <= 6.6

        new_tensor = vec.get_tensor(context)
        assert tensor is new_tensor
