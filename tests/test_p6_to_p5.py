#!/usr/bin/env python3
"""Regression tests for binary P6 (RGB) to P5 (grayscale) conversion."""
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class P6ToP5Tests(unittest.TestCase):
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

    def convert(self, width, height, pixels, maxval=255):
        header = f"P6\n{width} {height}\n{maxval}\n".encode("ascii")
        return subprocess.run(
            [str(self.binary)], input=header + bytes(pixels),
            capture_output=True, timeout=2,
        )

    def test_primary_colors(self):
        result = self.convert(3, 1, [255, 0, 0, 0, 255, 0, 0, 0, 255])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P5\n3 1\n255\n" + bytes([76, 149, 29]))

    def test_binary_control_bytes_are_pixels(self):
        result = self.convert(1, 1, [0, 10, 255])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P5\n1 1\n255\n" + bytes([34]))

    def test_multiple_rows(self):
        result = self.convert(1, 2, [0, 0, 0, 255, 255, 255])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P5\n1 2\n255\n" + bytes([0, 255]))

    def test_extra_bytes_are_not_pixels(self):
        result = self.convert(1, 1, [255, 255, 255, 0, 0, 0])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P5\n1 1\n255\n" + bytes([255]))

    def test_truncated_pixel(self):
        result = self.convert(1, 1, [255, 0])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"Truncated P6 pixel data", result.stderr)

    def test_truncated_second_row(self):
        result = self.convert(1, 2, [0, 0, 0])
        self.assertNotEqual(result.returncode, 0)

    def test_unsupported_16_bit_samples(self):
        result = self.convert(1, 1, [0, 0, 0], maxval=256)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
