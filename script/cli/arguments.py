import argparse
from .parameter_handlers import validate_file_path, validate_date_format


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        type=validate_file_path,
        nargs="+",
        required=True,
        help="Файлы для обработки",
    )

    parser.add_argument(
        "--report", type=str, required=True, choices=["average"], help="Тип отчета"
    )

    parser.add_argument(
        "--date", type=validate_date_format, help="Дата в формате YYYY-DD-MM"
    )
    return parser.parse_args()
