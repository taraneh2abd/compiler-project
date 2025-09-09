from compiler.utils.output_generator import Mode
from typing import List, Optional
from enum import Enum, auto

from compiler.utils.object import Object, Class, UseCase, Actor, Block, Package , Theme
from compiler.utils.exceptions import ObjectNotDeclaredException


class DiagType(Enum):
    CLASS = auto()
    USE_CASE = auto()
    SEQUENCE = auto()


OBJECTS_IN_DIAGRAMS = {DiagType.CLASS: [Class, Package],
                       DiagType.USE_CASE: [UseCase, Actor, Package],
                       DiagType.SEQUENCE: [Block, Package]}


class DiagGenerator:
    def __init__(self, diag_type: DiagType):
        self.type = diag_type
        self.available_object_types = OBJECTS_IN_DIAGRAMS[diag_type]
        self.objects = []
        self.sequences = []

    def generate(self, mode: Mode, object_list_names: Optional[List[str]] = None) -> str:
        if object_list_names is None:
            return self._generate_all()
        else:
            generated_objects = "".join(obj.generate() for obj in self.objects if obj.name in object_list_names)
            if self.type == DiagType.SEQUENCE:
                return generated_objects + self._generate_sequences(object_list_names)
            return generated_objects \
                + "".join(obj.generate_connections(object_list_names) for obj in self.objects if obj.name in object_list_names)

    def _generate_all(self) -> str:
        res = ""

        for obj in self.objects:
            if type(obj).__name__ == "Theme":
                res += obj._generate()

        for obj in self.objects:
            if type(obj).__name__ != "Theme":
                res += obj.generate()

        if self.type == DiagType.SEQUENCE:
            res += self._generate_sequences()
        else:
            res += "".join(obj.generate_connections() for obj in self.objects if type(obj).__name__ != "Theme")

        return res


    def _generate_sequences(self, object_list_names: List[str] | None = None):
        if object_list_names is None:
            return "".join(sequence.generate() for sequence in self.sequences)
        return "".join(sequence.generate() for sequence in self.sequences
                       if sequence.source_object_name in object_list_names
                       and sequence.destination_object_name in object_list_names)

    def add_object(self, object_to_add: Object):
        for existing_object in self.objects:
            if existing_object.name == object_to_add.name:
                self.objects.remove(existing_object)
                break
        self.objects.append(object_to_add)

    def get_object(self, name: str) -> Object:
        for obj in self.objects:
            if obj.name == name:
                return obj
        raise ObjectNotDeclaredException(name)
