#!/usr/bin/env python3
"""ASCII Netpbm conversion regression tests."""
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ASCIIConversionTests(unittest.TestCase):
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
    def tearDownClass(cls):
        if cls.temp is not None:
            cls.temp.cleanup()

    def tearDownClass(cls):
        cls.temp.cleanup()

    def convert(self, data):
        return subprocess.run([str(self.binary)], input=data,
                              capture_output=True, timeout=2)

    def test_p3_to_p2(self):
        result = self.convert(b"P3\n2 1\n255\n255 0 0  0 255 0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P2\n2 1\n255\n76 149\n")

    def test_p2_to_p1(self):
        result = self.convert(b"P2\n3 1\n255\n0 128 255\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P1\n3 1\n1 1 0\n")

    def test_comments_in_ascii_data(self):
        result = self.convert(b"P2\n2 1\n255\n0 # comment\n255\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P1\n2 1\n1 0\n")

    def test_truncated_p3(self):
        self.assertNotEqual(self.convert(b"P3\n1 1\n255\n10 20\n").returncode, 0)

    def test_truncated_p2(self):
        self.assertNotEqual(self.convert(b"P2\n2 1\n255\n0\n").returncode, 0)

    def test_out_of_range_p3(self):
        self.assertNotEqual(self.convert(b"P3\n1 1\n255\n256 0 0\n").returncode, 0)

    def test_out_of_range_p2(self):
        self.assertNotEqual(self.convert(b"P2\n1 1\n255\n256\n").returncode, 0)

    def test_large_maxval_avoids_overflow(self):
        result = self.convert(b"P3\n1 1\n65535\n65535 65535 65535\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"P2\n1 1\n65535\n65535\n")


if __name__ == "__main__":
    unittest.main()
