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


import unittest

import configsuite

from .data import templating


class TestTransformations(unittest.TestCase):
    def test_transformation_valid(self):
        raw_config = templating.build_config_no_definitions()
        config_suite = configsuite.ConfigSuite(raw_config, templating.build_schema())
        self.assertTrue(config_suite.valid)
        self.assertEqual(
            (
                "This is a story about a cow.",
                "It had a blue house.",
                "And the password to enter was 42.",
                "The end.",
            ),
            config_suite.snapshot.templates,
        )

    def test_transformation_invalid_value(self):
        raw_config = templating.build_config_no_definitions()
        raw_config["templates"].append(14)
        config_suite = configsuite.ConfigSuite(raw_config, templating.build_schema())
        self.assertFalse(config_suite.valid)

        self.assertEqual(1, len(config_suite.errors))
        err = config_suite.errors[0]
        self.assertIsInstance(err, configsuite.InvalidTypeError)

    def test_transformation_exception(self):
        raw_config = templating.build_config_no_definitions()
        raw_config["templates"].append("<this_is_no_variable>")
        config_suite = configsuite.ConfigSuite(raw_config, templating.build_schema())
        self.assertFalse(config_suite.valid)
        # TODO: Test errors
