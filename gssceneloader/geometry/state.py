from .vector3 import Vector3
from xml.etree import cElementTree as et


POSITION_ALIASES = ['position', 'pos', 'p', 'location', 'loc', 'l']
ROTATION_ALIASES = ['rotation', 'rot', 'r', 'orientation', 'orient', 'o']
SCALE_ALIASES = ['scale', 's', 'size']
RELATIVE_ALIASES = ['relative', 'rel']

StateValues = tuple[Vector3, Vector3, Vector3, bool]


class State():
    position: Vector3
    rotation: Vector3
    scale: Vector3
    relative: bool

    def __init__(self, position: Vector3 | None, rotation: Vector3 | None, scale: Vector3 | None, relative: bool = True):
        self.position = position or Vector3.Zero
        self.rotation = rotation or Vector3.Zero
        self.scale = scale or Vector3.One
        self.relative = relative

    def try_parse(self, value: str | None, parse: callable, ignore_malformed=False):
        if not value is None:
            try:
                val = parse(value)
                return val
            except Exception as e:
                if not ignore_malformed:
                    raise e
                return None
        return None

    def try_parse_vector(self, value: str | None, ignore_malformed=False) -> Vector3 | None:
        return self.try_parse(value, Vector3.Parse, ignore_malformed)

    def try_parse_bool(self, value: str | None, ignore_malformed=False) -> bool | None:
        def parse_bool(s: str):
            if s.lower() == 'false':
                return False
            elif s.lower() == 'true':
                return True
            else:
                return bool(int(s))

        return self.try_parse(value, parse_bool, ignore_malformed)

    def reconcile(self, element: et.Element, ignore_malformed=False) -> StateValues:
        position = self.position
        rotation = self.rotation
        scale = self.scale
        relative = self.relative

        position_value = any(map(element.get, POSITION_ALIASES))
        rotation_value = any(map(element.get, ROTATION_ALIASES))
        scale_value = any(map(element.get, SCALE_ALIASES))
        relative_value = any(map(element.get, RELATIVE_ALIASES))

        position = self.try_parse_vector(
            position_value, ignore_malformed) or position
        rotation = self.try_parse_vector(
            rotation_value, ignore_malformed) or rotation
        scale = self.try_parse_vector(scale_value, ignore_malformed) or scale
        relative = self.try_parse_bool(relative_value, ignore_malformed)
        if relative is None:
            relative = self.relative

        return (position, rotation, scale, relative)
