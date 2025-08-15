from cli.arguments import get_arguments
from core.data_processor import get_json_data
from core.reports import ReportEngine
from tabulate import tabulate


def main():
    args = get_arguments()
    if args.date:
        log_entries = get_json_data(args.file, args.date, as_dataclass=True)
    else:
        log_entries = get_json_data(args.file, as_dataclass=True)
    
    result = ReportEngine.run(args.report, log_entries)

    if isinstance(result, dict) and "table_data" in result:
        headers = ["handler", "total", "avg_response_time"]
        print(tabulate(result["table_data"], headers=headers, tablefmt="grid"))
    else:
        print(result)


if __name__ == "__main__":
    main()
