import tkinter as tk
from OrderData import OrderData
from GenerateReport import GenerateReport


class CVS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CVS")
        self.contract_numbers = OrderData.get_all_contracts()

        # create the frame for the contracts listbox, with scrollbar
        listbox_frame = tk.Frame(self)
        listbox_frame.pack(side='left', fill='both', expand=False)
        self.contract_listbox = tk.Listbox(listbox_frame, selectmode='single')
        self.contract_listbox.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        self.contract_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contract_listbox.yview)
        contract_label = tk.Label(self, text="Select a Contract Number:")
        contract_label.pack()

        # populate listbox
        for contract_number in self.contract_numbers:
            self.contract_listbox.insert(tk.END, str(contract_number[0]))
        
        self.contract_listbox.bind('<<ListboxSelect>>', self.select_contract)
        self.contract_data_frame = tk.Frame(self)
        self.contract_data_frame.pack(side='left', fill='both', expand=True)
        
        generate_report_button = tk.Button(self, text="Generate Report", command=self.generate_report)
        generate_report_button.pack()

    def generate_report(self):
        # Get the selected contract number and generate the report
        selected_contract = self.contract_listbox.get(tk.ACTIVE)
        contract_number = int(selected_contract)
        print(selected_contract, contract_number)
        data = OrderData.get_trim(contract_number)
        headers = OrderData.get_headers_for_trim_labels(contract_number)
        print(headers)
        if data:
            GenerateReport.generate_report_all_trim(headers, data)
            GenerateReport.generate_report_each_trim(headers, contract_number)
            GenerateReport.generate_report_title(headers)
            GenerateReport.open_foxit(fr'H:\basic_csv_transfer\{contract_number}_trim_prints')
            print("Reports Generated!")
        else:
            print("Couldn't generate report")


    def select_contract(self, event):
        for widget in self.contract_data_frame.winfo_children():
            widget.destroy()
        selected_index = self.contract_listbox.curselection()
        if selected_index:
            # get the value of the selected item
            selected_contract = self.contract_listbox.get(selected_index[0])
            contract_data = OrderData.get_one_contract(selected_contract)
            print(type(contract_data))
            if contract_data:
                # add the contract data to the contract_data_frame
                for i, value in enumerate(contract_data):
                    label_value = tk.Label(self.contract_data_frame, text=value)
                    label_value.grid(row=i, column=0, sticky='w')

                    
if __name__ == '__main__':
    app = CVS()
    app.mainloop()