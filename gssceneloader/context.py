import xml.etree.cElementTree as et
import torch
from collections import namedtuple
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

ContextLock = namedtuple('ContextLock', ['seed'], defaults=[False])


class Context():
    seed: int
    generator: torch.Generator
    locked: ContextLock

    def fill(self, element: et.Element, ignore_malformed=False):
        if not self.locked.seed:
            seed_element = element.find('seed')
            if seed_element is not None:
                self.seed = 0
                try:
                    self.seed = int(seed_element.text)
                    self.locked.seed = True
                except ValueError:
                    if not ignore_malformed:
                        raise ValueError(
                            f'Expected int for seed, got {seed_element.text}')

            self.generator = torch.Generator()
            self.generator.manual_seed(self.seed)

    def __init__(self):
        self.locked = ContextLock()

        self.seed = 0

        self.generator = torch.Generator()
        self.generator.manual_seed(self.seed)
