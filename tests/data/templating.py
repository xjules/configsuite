"""Copyright 2019 Equinor ASA and The Netherlands Organisation for
Applied Scientific Research TNO.

Licensed under the MIT license.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the conditions stated in the LICENSE file in the project root for
details.

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
"""


import jinja2

import configsuite
from configsuite import MetaKeys as MK
from configsuite import types


_VARIABLES = {"color": "blue", "secret_number": 42, "animal": "cow"}


@configsuite.transformation_msg("Renders Jinja template")
def _render(elem):
    if not isinstance(elem, str):
        return elem

    jinja_env = jinja2.Environment(block_start_string="<", block_end_string=">")
    return jinja_env.from_string(elem).render(**_VARIABLES)


def build_schema():
    return {
        MK.Type: types.NamedDict,
        MK.Content: {
            "definitions": {
                MK.Type: types.Dict,
                MK.Required: False,
                MK.Content: {
                    MK.Key: {MK.Type: types.String},
                    MK.Value: {MK.Type: types.String},
                },
            },
            "templates": {
                MK.Type: types.List,
                MK.Content: {
                    MK.Item: {MK.Type: types.String, MK.Transformation: _render}
                },
            },
        },
    }


def build_config_no_definitions():
    return {
        "templates": [
            "This is a story about a <animal>.",
            "It had a <color> house.",
            "And the password to enter was <secret_number>.",
            "The end.",
        ]
    }
