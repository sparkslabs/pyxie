from pyxie.model.pynodes.values import ProfilePyNode

import pyxie.model.functions

def initialise_external_function_definitions():
    # Inside <Servo.h>
    function_calls = {
                "Servo": {
                            "iterator": False,
                            "return_ctype": "Servo", # C type of the returned value
                        }
        }

    types = {
                "Servo": {
                    }
        }

    # Update the actual profile functions/types

    for function in function_calls:
        pyxie.model.functions.profile_funcs[function] = function_calls[function]

    for t in types:
        pyxie.model.functions.profile_types[t] = types[t]


def populate_profile_context(context):
    for i in range(8):
        a_pin_name = "A" + str(i)
        a_pin = ProfilePyNode(a_pin_name, "integer")
        context.store(a_pin_name, a_pin)

    a_pin = ProfilePyNode("HIGH", "integer")
    context.store("HIGH", a_pin)

    a_pin = ProfilePyNode("LOW", "integer")
    context.store("LOW", a_pin)

    a_pin = ProfilePyNode("INPUT", "integer")
    context.store("INPUT", a_pin)
    a_pin = ProfilePyNode("OUTPUT", "integer")
    context.store("OUTPUT", a_pin)


def initialise_profile(context):
    context.tag = "PROFILE:arduino"
    populate_profile_context(context)
    initialise_external_function_definitions()

