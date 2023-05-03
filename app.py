import tkinter as tk
from OrderData import OrderData


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")

        # Get a list of available contract numbers
        self.contract_numbers = OrderData.get_contract_numbers()

        # Create a label and drop-down list for selecting the contract number
        contract_label = tk.Label(self, text="Select a Contract Number:")
        contract_label.pack()
        self.contract_var = tk.StringVar(self)
        self.contract_var.set(self.contract_numbers[0])
        self.contract_dropdown = tk.OptionMenu(self, self.contract_var, *self.contract_numbers)
        self.contract_dropdown.pack()

        # Create a button for generating the report
        generate_report_button = tk.Button(self, text="Generate Report", command=self.generate_report_on_click)
        generate_report_button.pack()

    def generate_report_on_click(self):
        # Get the selected contract number and generate the report
        contract_number = int(self.contract_var.get())
        data = OrderData.get_trim(contract_number)
        headers = OrderData.get_headers_for_trim_labels(contract_number)
        print(headers)
        if data:
            OrderData.generate_report_all_trim(headers, data)
            OrderData.generate_report_each_trim(headers, contract_number)
            print("Reports Generated!")
        else:
            print("Couldn't generate report")
