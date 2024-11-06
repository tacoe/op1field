import Live # type: ignore
from .OP1Field import OP1Field

def create_instance(c_instance):
    return OP1Field(c_instance)
