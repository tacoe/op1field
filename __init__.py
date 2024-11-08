from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import (
    CONTROLLER_ID_KEY,
    PORTS_KEY,
    NOTES_CC,
    REMOTE,
    SCRIPT,
    controller_id,
    inport,
    outport,
)
from .OP1Field import OP1Field

def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(
            vendor_id=0x2367,        # Replace with your device's vendor ID
            product_ids=[0x0102],    # Replace with your device's product ID
            model_name='OP-1'  # Ensure this matches your device's name
        ),
        PORTS_KEY: [
            inport(props=[NOTES_CC, SCRIPT, REMOTE]),
            outport(props=[NOTES_CC, SCRIPT, REMOTE]),
        ]
    }

def create_instance(c_instance):
    return OP1Field(c_instance)
