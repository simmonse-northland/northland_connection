import tkinter as tk
from OrderData import OrderData


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        contract_label = tk.Label(self, text="Contract Number:")
        contract_label.pack()
        self.contract_entry = tk.Entry(self)
        self.contract_entry.pack()

        generate_report_button = tk.Button(self, text="Generate Report", command=self.generate_report_on_click)
        generate_report_button.pack()

    def generate_report_on_click(self):
        contract_number = int(self.contract_entry.get())
        data = OrderData.get_trim(contract_number)
        headers = OrderData.get_headers_for_trim_labels(contract_number)
        print(headers)
        if data:
            OrderData.generate_report(headers, data)
            print("Report Generated!")
        else:
            print("Couldn't generate report")

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
