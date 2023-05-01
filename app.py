import tkinter as tk
from queries import get_trim_by_estimate_id, get_headers_by_estimate_id
from generate_report import generate_report

def generate_report_on_click():
    estimate_id_number = int(estimate_id_entry.get())
    data = get_trim_by_estimate_id(estimate_id_number)
    headers = get_headers_by_estimate_id(estimate_id_number)
    if data:
        generate_report(data, headers)
        print("Report Generated!")
    else:
        print("Couldn't generate report")

# Create the tkinter app
root = tk.Tk()

# Add a label and an entry field for the estimate ID
estimate_id_label = tk.Label(root, text="Estimate ID:")
estimate_id_label.pack()
estimate_id_entry = tk.Entry(root)
estimate_id_entry.pack()

# Add a button to generate the report
generate_report_button = tk.Button(root, text="Generate Report", command=generate_report_on_click)
generate_report_button.pack()

# Run the tkinter main loop
root.mainloop()