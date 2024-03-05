# README

## Overview

This Python script assigns students to slots. The students are read from a CSV file and the slots are saved to an Excel file. The assignment is done randomly, but the randomness is controlled by a seed. The seed can be provided as a command line argument, or it can be generated from an image. If no image is provided, a random image is downloaded from Unsplash.

## Seed in Random Number Generation

A seed is an initial value used in the generation of a sequence of random numbers. When you set a seed, the algorithm will ensure that the same sequence of random numbers is generated, or re-generated when you run it again. This is useful for debugging and testing purposes, where you want repeatable sequences.

### Why Use a Seed?

- **Reproducibility**: It ensures that the sequence of random numbers remains the same across multiple runs. This is important in scenarios where you need to reproduce the results, such as debugging or testing.

- **Fairness**: In the context of this script, using a seed ensures that the assignment of students to slots is done fairly. The seed can be generated from an image, which can be provided or randomly downloaded from Unsplash. This ensures that the assignment process is not biased and can be reproduced if needed.

### How Does a Seed Work?

In this script, the seed is used in the `assign_students_to_slots` function. The `random.seed(seed)` function initializes the random number generator. The `random.shuffle(students)` function then shuffles the students randomly, but in a way that is determined by the seed. This means that if you run the script again with the same seed and the same list of students, the students will be assigned to the same slots.

## Virtual Environment (venv)

A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated Python environments for them. This is one of the most important tools that most Python developers use.

### Why Use venv?

- Different applications can then use different versions of the same module without causing conflicts.
- It's easier to manage Python packages with `venv`.

### How to Use venv?

1. Install the virtual environment via pip:

```bash
pip install virtualenv
```

2. Navigate to your project directory and create a virtual environment:

```bash
cd my_project
virtualenv venv
```

3. Activate the virtual environment:

On Windows, run:

```bash
venv\Scripts\activate
```

On Unix or MacOS, run:

```bash
source venv/bin/activate
```

4. Install the required packages for your project:

```bash
pip install -r requirements.txt
```

## Requirements

The script requires Python 3.10 or later and the Python packages listed in `requirements.txt`. You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

The script is run from the command line with the following arguments:

- `--student-csv-file-name`: Name of the student CSV file (required)
- `--image-path`: Path to the image file (optional)
- `--output-xlsx-file-name`: Name of the output xlsx file (required)
- `--seed`: Seed for random number generator (optional)

Example:

```bash
    main.py [-h] --student-csv-file-name
               STUDENT_CSV_FILE_NAME [--image-path IMAGE_PATH]
               --output-xlsx-file-name OUTPUT_XLSX_FILE_NAME
               [--seed SEED]
```

### Example Usage

This will read students from `students.csv`, generate a seed from a random image from Unsplash, assign students to slots, and save the result to `output.xlsx`.

```bash
python main.py --student-csv-file-name students.csv --output-xlsx-file-name output.xlsx

```

This will read students from `students.csv`, generate a seed from a random image from Unsplash, assign students to slots, and save the result to `output.xlsx`.

## Input

The student CSV file should be formatted with semicolon-separated values and the columns should be named 'imie' and 'nazwisko' for first name and last name respectively.

This list could be obtained from the USOS system after login: [export link](https://usosweb.usos.pw.edu.pl/kontroler.php?_action=common/sqlExport&export=g_6cd51435&format=csv-excel)

## Output

The output is an Excel file with the seed and the slots. Each slot is a column with the title "Session X", where X is the slot number. The seed is also included in the Excel file. If a seed image was used, it is included in the Excel file as well.

## Cleaning Up

The script cleans up after itself by deleting any temporary image files it created in the process.
