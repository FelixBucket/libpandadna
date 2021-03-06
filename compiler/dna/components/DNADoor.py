import DNAGroup
from dna.base.DNAPacker import *


class DNADoor(DNAGroup.DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)

        self.code = ''
        self.color = (1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def traverse(self, recursive=True, verbose=False):
        packer = DNAGroup.DNAGroup.traverse(self, recursive=False, verbose=verbose)
        packer.name = 'DNADoor'  # Override the name for debugging.

        packer.pack('code', self.code, SHORT_STRING)
        packer.packColor('color', *self.color)

        return packer
