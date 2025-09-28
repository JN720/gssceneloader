from abc import ABC, abstractmethod
import torch
import re

from ..context import Context


class Vector3(ABC):
    @staticmethod
    def Zero():
        return StaticVector3(0.0, 0.0, 0.0)

    @staticmethod
    def One():
        return StaticVector3(1.0, 1.0, 1.0)

    @staticmethod
    def Parse(value: str):
        try:
            value = re.sub(r'[\(\)\[\]\{\}]', '', value)
            value = value.strip()
            x, y, z = map(float, value.split(','))
            return StaticVector3(x, y, z)
        except:
            raise ValueError(f'Expected valid Vector3 string, got {value}')

    @abstractmethod
    def get_tensor(self, context: Context) -> torch.tensor:
        pass

    def get(self, context: Context) -> (float, float, float):
        tensor = self.get_tensor(context)
        return (tensor[0], tensor[1], tensor[2])

    # def __add__(self, other):
    #     vec1 = self.get_tensor()
    #     vec2 = other.get_tensor() if isinstance(
    #         other, Vector3) else torch.tensor([other, other, other])
    #     return vec1 + vec2

    # def __sub__(self, other):
    #     vec1 = self.get_tensor()
    #     vec2 = other.get_tensor() if isinstance(
    #         other, Vector3) else torch.tensor([other, other, other])
    #     return vec1 - vec2

    # def __mul__(self, other):
    #     vec1 = self.get_tensor()
    #     vec2 = other.get_tensor() if isinstance(
    #         other, Vector3) else torch.tensor([other, other, other])
    #     return vec1 * vec2

    # def __truediv__(self, other):
    #     vec1 = self.get_tensor()
    #     vec2 = other.get_tensor() if isinstance(
    #         other, Vector3) else torch.tensor([other, other, other])
    #     return vec1 / vec2


class StaticVector3(Vector3):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def get_tensor(self, context: Context) -> torch.tensor:
        return torch.tensor([self.x, self.y, self.z])


class RandomVector3(Vector3):
    def __init__(self):
        self.tensor = None

    def get_tensor(self, context: Context) -> torch.tensor:
        if self.tensor is None:
            self.tensor = torch.rand(
                3, dtype=torch.float64, generator=context.generator)
        return self.tensor


class RandomRangeVector3(Vector3):
    def __init__(self, min: Vector3, max: Vector3):
        self.minimum = min
        self.maximum = max
        self.tensor = None

    def get_tensor(self, context: Context) -> torch.tensor:
        if self.tensor is None:
            min_tensor = self.minimum.get_tensor(context)
            max_tensor = self.maximum.get_tensor(context)
            self.tensor = (torch.rand(3, dtype=torch.float64, generator=context.generator) *
                           (max_tensor - min_tensor)) + min_tensor
        return self.tensor
