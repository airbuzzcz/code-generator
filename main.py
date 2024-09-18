import csv
import random
from datetime import datetime
from pathlib import Path
import platform
import subprocess
import sys

BASIC_CHARACTER_SETS = {
    "numeric": "1234567890",
    "alpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "custom": ""
}

default_file_name = "codes_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"


def build_character_set(charset, case):
    if case == "lower":
        alpha_set = BASIC_CHARACTER_SETS["alpha"].lower()
    elif case == "mixed":
        alpha_set = BASIC_CHARACTER_SETS["alpha"] + BASIC_CHARACTER_SETS["alpha"].lower()
    else:
        alpha_set = BASIC_CHARACTER_SETS["alpha"]

    if charset == "3":
        used_charset = BASIC_CHARACTER_SETS["numeric"]
    elif charset == "2":
        used_charset = alpha_set
    elif charset == "1":
        used_charset = BASIC_CHARACTER_SETS["numeric"] + alpha_set
    else:
        used_charset = BASIC_CHARACTER_SETS["custom"]

    return used_charset


def generate_codes(codes_count, char_length, charset):
    codes_set = set()
    i = 0

    print()
    while i < codes_count:
        code = "".join(random.choice(charset) for _ in range(char_length))
        if code in codes_set:
            continue
        else:
            codes_set.add(code)
            i += 1

            progress = i / codes_count
            num_chars = int(progress * 50)
            progress_bar = "│" + "█" * num_chars + "─" * (50 - num_chars) + "│"
            print(f"\r{progress_bar} {progress * 100: .1f}%", end='', flush=True)

    print()
    print("\033[32mKódy vygenerovány.\033[0m")

    return codes_set


def make_directory():
    directory = Path("generated_codes")
    directory.mkdir(exist_ok=True)
    return directory


def open_directory(path):
    directory = path.parent

    if platform.system() == "Windows":
        subprocess.run(["explorer", str(directory)])
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(directory)])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", str(directory)])
    else:
        print("Operating system not supported for automatic directory opening.")


def save_codes(codes_set, output_file_name, encoding):
    codes_dir = make_directory()

    full_output_path = codes_dir / output_file_name

    with open(full_output_path, "w", newline="", encoding=encoding) as csvfile:
        cw = csv.writer(csvfile)
        for row in codes_set:
            cw.writerow([row])
    print("\033[32mKódy uloženy do souboru " + output_file_name + ".\033[0m")

    return full_output_path


def get_positive_int():
    while True:
        try:
            value = int(input())
            if value > 0:
                return value
            else:
                print("\033[31mZadej kladné číslo.\033[0m")
        except ValueError:
            print("\033[31mZadej platné číslo.\033[0m")


def get_valid_option(valid_options):
    while True:
        choice = input().lower()
        if choice in valid_options:
            return choice
        print(f"\033[31mVyber jednu z platných možností: {', '.join(valid_options)}\033[0m")


def get_optional_input():
    value = input()
    if value:
        return value
    else:
        print("Vybrána defaultní hodnota.")


def get_required_input():
    while True:
        value = input()
        if value:
            return value
        else:
            print("\033[31mSada nesmí být prázdná.\033[0m")


def interactive_input():
    # Get code count with validation
    print()
    print("\033[1mZadej počet kódů:\033[0m")
    codes_count = get_positive_int()

    # Get code length with validation
    print()
    print("\033[1mPočet znaků:\033[0m")
    char_length = get_positive_int()

    # Get character set choice with validation
    print()
    print("\033[1mVyber sadu znaků:\033[0m")
    print("1. Písmena a čísla (doporučeno)")
    print("2. Písmena")
    print("3. Čísla")
    print("4. Vlastní sada znaků")
    charset_choice = get_valid_option({"1", "2", "3", "4"})

    if charset_choice == "4":
        print()
        print("\033[1mZadej vlastní sadu kódů:\033[0m")
        custom_charset = get_required_input()
        BASIC_CHARACTER_SETS["custom"] = custom_charset

    if charset_choice != "4":
        print()
        print("\033[1mVyber velikost písmen:\033[0m")
        print("1. Velká písmena (doporučeno)")
        print("2. Malá písmena")
        print("3. Oboje")
        case_choice = get_valid_option({"1", "2", "3"})
    else:
        case_choice = "1"

    print()
    print("\033[1mZadej kódování souboru\033[0m")
    print("1. UTF-8 (doporučeno)")
    print("2. ISO-8859-2")
    print("3. Windows-1250")
    encoding_choice = get_valid_option({"1", "2", "3"})

    if encoding_choice == "1":
        encoding = "utf-8"
    elif encoding_choice == "2":
        encoding = "iso-8859-2"
    elif encoding_choice == "3":
        encoding = "windows-1250"
    else:
        encoding = "utf-8"

    print()
    print(f"\033[1mZadej název souboru (defaultní: {default_file_name})\033[0m")
    output_file_name = get_optional_input() or default_file_name

    return codes_count, char_length, charset_choice, case_choice, output_file_name, encoding


def print_app_info():
    print()
    print("\033[1m\033[94m\033[7mAirbuzz Code Generator\033[0m")
    print()
    print("Verze: 1.0.0")
    print("Licence: MIT License")
    print("Copyright (c) 2024 Airbuzz, s.r.o.")
    print("=" * 60)


def main():
    print_app_info()

    codes_count, char_length, charset, case, output_file_name, encoding = interactive_input()

    character_set = build_character_set(charset, case)

    codes = generate_codes(codes_count, char_length, character_set)

    output_path = save_codes(codes, output_file_name, encoding)

    print()
    print("\033[1mOtevřít složku s vygenerovanými kódy?\033[0m")
    print("1. Ano")
    print("2. Ne")
    open_dir_choice = get_valid_option({"1", "2"})

    if open_dir_choice == "1":
        open_directory(output_path)
    else:
        sys.exit()


if __name__ == "__main__":
    main()
