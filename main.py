from queries import get_trim_by_estimate_id, get_headers_by_estimate_id
from generate_report import generate_report


if __name__ == "__main__":
    estimate_id_number = 150985
    data = get_trim_by_estimate_id(estimate_id_number)
    headers = get_headers_by_estimate_id(estimate_id_number)
    if data:
        generate_report(data, headers)
        print("Report Generated!")
    else:
        print("Couldn't generate report")
