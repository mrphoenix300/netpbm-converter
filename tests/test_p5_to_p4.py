#!/usr/bin/env python3
"""Regression tests for P5 (8-bit PGM) to P4 (packed PBM) conversion."""
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class P5ToP4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.binary = pathlib.Path(cls.temp.name) / "figproc"
        subprocess.run(
            ["cc", "-std=c99", "-Wall", "-Wextra", "-o", str(cls.binary), str(ROOT / "figproc.c")],
            check=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def convert(self, width, height, pixels, maxval=255):
        source = f"P5\n{width} {height}\n{maxval}\n".encode() + bytes(pixels)
        return subprocess.run([str(self.binary)], input=source, capture_output=True)

    def test_single_pixel_per_row(self):
        result = self.convert(1, 2, [0, 255])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P4\n1 2\n\x80\x00")

    def test_eight_pixels_exact_byte(self):
        result = self.convert(8, 1, [0, 255] * 4)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P4\n8 1\n\xaa")

    def test_nine_pixels_two_rows(self):
        result = self.convert(9, 2, [0] * 9 + [255] * 9)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P4\n9 2\n\xff\x80\x00\x00")

    def test_truncated_input_fails(self):
        result = self.convert(2, 1, [0])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"Truncated P5 pixel data", result.stderr)


if __name__ == "__main__":
    unittest.main()
