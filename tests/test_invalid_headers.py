#!/usr/bin/env python3
"""Regression tests for malformed Netpbm headers.

These tests intentionally document inputs the parser must reject. They may
fail against the current implementation until header parsing is hardened.
"""
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class InvalidHeaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get("FIGPROC_BINARY")
        if configured:
            cls.temp = None
            cls.binary = pathlib.Path(configured).expanduser().resolve()
            if not cls.binary.is_file():
                raise FileNotFoundError(f"FIGPROC_BINARY not found: {cls.binary}")
        else:
            cls.temp = tempfile.TemporaryDirectory()
            cls.binary = pathlib.Path(cls.temp.name) / "figproc"
            subprocess.run(
                ["cc", "-std=c99", "-Wall", "-Wextra", "-o",
                 str(cls.binary), str(ROOT / "figproc.c")],
                check=True,
            )

    @classmethod
    @classmethod
    def tearDownClass(cls):
        if cls.temp is not None:
            cls.temp.cleanup()

    def tearDownClass(cls):
        cls.temp.cleanup()

    def assert_rejected(self, data):
        try:
            result = subprocess.run(
                [str(self.binary)], input=data, capture_output=True, timeout=2
            )
        except subprocess.TimeoutExpired:
            self.fail("Converter hung on invalid header")
        self.assertNotEqual(result.returncode, 0, "Invalid input was accepted")

    def test_empty_input(self):
        self.assert_rejected(b"")

    def test_invalid_magic_number(self):
        self.assert_rejected(b"P9\n1 1\n255\n\x00")

    def test_zero_width(self):
        self.assert_rejected(b"P5\n0 1\n255\n")

    def test_zero_height(self):
        self.assert_rejected(b"P5\n1 0\n255\n")

    def test_zero_maxval(self):
        self.assert_rejected(b"P5\n1 1\n0\n\x00")

    def test_missing_maxval(self):
        self.assert_rejected(b"P5\n1 1\n")

    def test_integer_overflow(self):
        self.assert_rejected(b"P5\n999999999999999999999999 1\n255\n")


if __name__ == "__main__":
    unittest.main()
