import csv
import random
import sys
import xlsxwriter
import argparse
import aiohttp
import asyncio
import time
import os
from typing import TypeVar

# base directory for input files
INPUT_FILE_PATH_BASE_DIR = "./../input/"
# base directory for output files
OUTPUT_FILE_PATH_BASE_DIR = "./../output/"
# random image source
RANDOM_IMAGE_SOURCE = "https://source.unsplash.com/random"
# students per session
STUDENTS_PER_SESSION = 3


async def get_random_image_from_unsplash() -> str:
    """Get random image from Unsplash

    Returns:
        str: path to the temporary image file
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(RANDOM_IMAGE_SOURCE) as response:
            obtained_image = await response.read()

            temporary_image_path = (
                f"{INPUT_FILE_PATH_BASE_DIR}temporary_seed_image_{int(time.time())}.jpg"
            )

            with open(temporary_image_path, "wb") as f:
                f.write(obtained_image)
            return temporary_image_path


GenericAsyncFunctionReturnType = TypeVar("GenericAsyncFunctionReturnType")


def async_to_sync(
    awaitable: asyncio.Future[GenericAsyncFunctionReturnType],
) -> GenericAsyncFunctionReturnType:
    """Convert async function to sync

    Args:
        awaitable (asyncio.Future[GenericAsyncFunctionReturnType]): Awaitable function

    Returns:
        GenericAsyncFunctionReturnType: Result of the awaitable function
    """

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)


def generate_seed_from_image(image_path: str) -> int:
    """Generate seed from image

    Args:
        image_path (str): Path to the image file

    Returns:
        int: Seed for random number generator
    """

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

            # TODO: Create hashing function for image data
            return 0

    except Exception as e:
        print(f"Error reading image for seed generation: {e}")
        sys.exit(1)


def read_students_from_csv(csv_file_path: str) -> list[str]:
    """Read students from CSV file

    Args:
        csv_file_path (str): Path to the CSV file

    Returns:
        list[str]: List of students in format "Name Surname"
    """

    students = []
    try:
        with open(csv_file_path, newline="", encoding="utf-8-sig", mode="r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')

            for row in reader:
                student_name = f"{row['imie']} {row['nazwisko']}"
                students.append(student_name)
    except Exception as e:
        print(f"Error reading student CSV file: {e}")
        sys.exit(1)
    return students


def assign_students_to_sessions(students: list[str], seed: int) -> list[list[str]]:
    """Assign students to slots

    Args:
        students (list[str]): List of students
        seed (int): Seed for random number generator

    Returns:
        list[list[str]]: List of slots with students assigned
    """

    random.seed(seed)
    random.shuffle(students)

    slots = [[] for _ in range(7)]
    for i, student in enumerate(students):
        slots[i % 7].append(student)

    return slots[::-1]


def clean() -> None:
    """Clean temporary files"""

    for file in os.listdir(INPUT_FILE_PATH_BASE_DIR):
        if file.startswith("temporary_seed_image_"):
            os.remove(f"{INPUT_FILE_PATH_BASE_DIR}{file}")


def save_to_xlsx(
    slots: list[list[str]], seed: int, output_file_path: str, seed_image_path: str
) -> None:
    """Save slots to xlsx file along with the seed and seed image (format: .xlsx)

    Args:
        slots (list[list[str]]): Slots with students assigned
        seed (int): Seed for random number generator
        output_file_path (str): File path for the output xlsx file
        seed_image_path (str): Path to the seed image
    """

    workbook = xlsxwriter.Workbook(f"{OUTPUT_FILE_PATH_BASE_DIR}{output_file_path}")
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "Session", bold)
    worksheet.write("A2", seed)
    for i in range(7):
        worksheet.write(0, i + 1, f"Session {i+1}", bold)
        for j, student in enumerate(slots[i]):
            worksheet.write(j + 1, i + 1, student)

    if seed_image_path:
        worksheet.write("K1", "Seed Image", bold)
        worksheet.insert_image("K3", seed_image_path, {"x_scale": 0.1, "y_scale": 0.1})

    for i in range(7):
        worksheet.set_column(i, i, len(max(slots[i], key=len)) + 5)

    workbook.close()


def main() -> None:
    """Main function for the script that assigns students to slots"""

    command_line_parser = argparse.ArgumentParser(
        description="Assign students to slots"
    )
    command_line_parser.add_argument(
        "--student-csv-file-name",
        type=str,
        help="Name of the student CSV file",
        required=True,
    )
    command_line_parser.add_argument(
        "--image-path", type=str, help="Path to the image file", required=False
    )
    command_line_parser.add_argument(
        "--output-xlsx-file-name",
        type=str,
        help="Name of the output xlsx file",
        required=True,
        # validate if ends with .xlsx
    )
    command_line_parser.add_argument(
        "--seed", type=int, help="Seed for random number generator", required=False
    )
    args = command_line_parser.parse_args()

    if (
        len(sys.argv) == 1
        or sys.argv[1] == "-h"
        or sys.argv[1] == "--help"
        or (
            args.image_path is None
            and not args.student_csv_file_name
            and not args.output_xlsx_file_name
        )
    ):
        command_line_parser.print_help()
        sys.exit(1)

    if not args.output_xlsx_file_name.endswith(".xlsx"):
        print("Output file should end with .xlsx")
        sys.exit(1)

    seed_image_path = None

    if args.image_path:
        seed_image_path = args.image_path
    else:
        seed_image_path = async_to_sync(get_random_image_from_unsplash())

    if args.seed:
        seed = args.seed
    else:
        seed = generate_seed_from_image(seed_image_path)

    try:
        student_csv_file_path, output_xlsx_file_name = (
            f"{INPUT_FILE_PATH_BASE_DIR}{args.student_csv_file_name}",
            f"{OUTPUT_FILE_PATH_BASE_DIR}{args.output_xlsx_file_name}",
        )

        students = read_students_from_csv(student_csv_file_path)

        sessions = assign_students_to_sessions(students, seed)

        save_to_xlsx(sessions, seed, output_xlsx_file_name, seed_image_path)

        print(
            f"Students have been successfully assigned to slots. Output saved to {output_xlsx_file_name}. Seed: {seed}"
        )

    except Exception as e:
        print(f"Error generating seed and assigning students to slots: {e}")
        sys.exit(1)
    finally:
        clean()


if __name__ == "__main__":
    main()
