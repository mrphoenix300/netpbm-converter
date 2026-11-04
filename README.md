# Netpbm Image Converter (figproc)

A lightweight **C command-line image converter** developed originally for the *Introduction to Programming* university course and subsequently improved with input validation and automated regression tests.

The program reads an image from **standard input** and writes the converted image to **standard output**. The input magic number determines the conversion automatically.

## Supported conversions

| Input | Output | Description |
| --- | --- | --- |
| P3 (ASCII PPM) | P2 (ASCII PGM) | RGB to grayscale |
| P2 (ASCII PGM) | P1 (ASCII PBM) | Grayscale to black and white |
| P6 (binary PPM) | P5 (binary PGM) | RGB to grayscale |
| P5 (binary PGM) | P4 (binary PBM) | Grayscale to packed black and white |

Grayscale is calculated using integer arithmetic:

`gray = (299 * R + 587 * G + 114 * B) / 1000`

Values are rounded down by integer division. Black-and-white conversion uses the threshold `(maxval + 1) / 2`: samples at or below that threshold become black (`1` in PBM), and larger samples become white (`0`).

## Build

Requires a C99-compatible compiler (for example, GCC):

```bash
gcc -std=c99 -Wall -Wextra -Wpedantic -Wconversion figproc.c -o figproc
```

## Usage

Pass the source image via standard input and redirect the output to a file:

```bash
./figproc < input.ppm > output.pgm
./figproc < input.pgm > output.pbm
```

For an ASCII example:

```bash
printf 'P3\n2 1\n255\n255 0 0 0 255 0\n' | ./figproc
```

Expected output:

```text
P2
2 1
255
76 149
```

The converter uses standard input/output, so **binary outputs should be redirected to a file**, rather than displayed in a terminal. Diagnostics are written to standard error. An invalid or truncated input returns a nonzero exit status; because conversion is streamed, output may already have been partially written.

## Input validation and limitations

- Supports positive image dimensions and `maxval` in the range `1..65535` for ASCII P2/P3 input.
- Supports **8-bit binary samples only** (`maxval` in `1..255`) for P5/P6. 16-bit binary samples are rejected.
- Rejects unsupported input magic numbers, malformed or incomplete headers, integer-overflowing header values, truncated image data and sample values exceeding `maxval`.
- Parses decimal samples and `#` comments in ASCII input.
- Performs **single-image, streaming conversion**, reading only the declared number of pixels. Extra trailing data is not interpreted as another image.
- It is not a general-purpose Netpbm library and does not implement every possible variant or extension.

The implementation avoids floating-point arithmetic, `math.h` and file-opening APIs; it uses standard streams (`getchar`, `putchar`, `printf` and `fprintf`).

## Tests

The regression suite uses Python's standard `unittest` module (no third-party Python packages required):

```bash
python3 -m unittest discover -s tests -v
```

The **28 regression tests** cover all four conversions, invalid headers, truncated data and out-of-range samples.

### Run with UndefinedBehaviorSanitizer

Build a UBSan-enabled executable:

```bash
mkdir -p build
gcc -std=c99 -Wall -Wextra -Wpedantic -Wconversion \
    -g -O1 -fno-omit-frame-pointer \
    -fsanitize=undefined -fno-sanitize-recover=all \
    figproc.c -o build/figproc_ubsan
```

Use `FIGPROC_BINARY` to run the tests against that exact executable:

```bash
FIGPROC_BINARY="$PWD/build/figproc_ubsan" \
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
python3 -m unittest discover -s tests -v
```

Passing tests does not guarantee the absence of vulnerabilities; sanitizer results apply to the exercised code paths.

## Project background

Originally a first-semester C programming exercise, this project has been revisited to improve its robustness and testability while preserving its small, stream-based design.

Author: [mrphoenix300](https://github.com/mrphoenix300)
