import tkinter as tk
from OrderData import OrderData


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")

        # Add a label and an entry field for the estimate ID
        estimate_id_label = tk.Label(self, text="Estimate ID:")
        estimate_id_label.pack()
        self.estimate_id_entry = tk.Entry(self)
        self.estimate_id_entry.pack()

        # Add a button to generate the report
        generate_report_button = tk.Button(self, text="Generate Report", command=self.generate_report_on_click)
        generate_report_button.pack()

    def generate_report_on_click(self):
        estimate_id_number = int(self.estimate_id_entry.get())
        data = OrderData.get_trim(estimate_id_number)
        headers = OrderData.get_headers_for_trim_labels(estimate_id_number)
        print(headers)
        if data:
            OrderData.generate_report(headers, data)
            print("Report Generated!")
        else:
            print("Couldn't generate report")

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
