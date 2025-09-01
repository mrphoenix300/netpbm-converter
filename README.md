# figproc – Netpbm Image Converter

This project was developed as part of the **"Introduction to Programming"** course.  
The goal was to implement basic image processing operations in **C**, working directly with the **Netpbm format** (P1–P6).

---

## 📌 Project Description

The program `figproc.c` reads an image from **standard input** and writes the converted image to **standard output**.  
It supports conversions between **color, grayscale, and black & white** images, depending on the input format:

- **P6 → P5** : Color (binary) → Grayscale (binary)  
- **P5 → P4** : Grayscale (binary) → Black & White (binary)  
- **P3 → P2** : Color (ASCII) → Grayscale (ASCII)  
- **P2 → P1** : Grayscale (ASCII) → Black & White (ASCII)  

The conversion is automatically determined by the input file’s **magic number**.

---

## ⚙️ Implementation Details

- **Language**: C (standard ANSI C)
- **I/O**: Uses only `getchar()` and `putchar()` for reading/writing.
- **Restrictions**:  
  - No arrays (including strings)  
  - No floating-point numbers  
  - No `math.h` functions  
  - No file handling functions (`fopen`, `fread`, etc.)  
- **Conversion methods**:
  - **Color → Grayscale**: Luminosity method  
    \[
    gray = \left\lfloor \frac{299R + 587G + 114B}{1000} \right\rfloor
    \]
  - **Grayscale → Black & White**: Threshold method  
    \[
    pixel = (value > \lfloor \tfrac{max+1}{2} \rfloor) ? 0 : 1
    \]

---

## 🚀 Usage

Compile the program:

```bash
gcc figproc.c -o figproc
````

Run it with input/output redirection:

```bash
./figproc < input.ppm > output.pgm
./figproc < input.pgm > output.pbm
```

Examples:

```bash
./figproc < NIbin.ppm > NIbin.pgm
./figproc < NIbin.pgm > NIbin.pbm
```

---

## 🔍 Testing & Tools

To inspect binary-encoded files, you can use the `od` command on Unix-like systems:

```bash
od -tx1c file.ppm
```

---

## 📂 Example Conversions

* `P6 → P5`: color image to grayscale
* `P5 → P4`: grayscale to black & white
* `P3 → P2`: color (ASCII) to grayscale (ASCII)
* `P2 → P1`: grayscale (ASCII) to black & white (ASCII)

---

## ✨ Bonus (optional extension)

As an extension, the program could also support conversions between **binary ↔ ASCII encodings** without changing the image type (e.g., `P6 ↔ P3`, `P5 ↔ P2`, `P4 ↔ P1`).

---

## 📖 Notes

* The program strictly reads/writes image data — no extra output messages except in case of input errors (`Input error!`).
* Developed and tested in a **Linux environment**.

---

## 👨‍💻 Author

This project was originally developed during my **first semester at the university** as 
part of the course *Introduction to Programming*.  
It represents my first experience in C programming applied to a real-world problem: implementing 
image processing directly on the **Netpbm format**.

**MrPhoenix300**
