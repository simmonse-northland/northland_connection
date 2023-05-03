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
            self.contract_listbox.insert(tk.END, contract_number)
        self.contract_listbox.bind('<<ListboxSelect>>', self.select_contract)


        self.contract_data_frame = tk.Frame(self)
        self.contract_data_frame.pack(side='left', fill='both', expand=True)
        
        generate_report_button = tk.Button(self, text="Generate Report", command=self.generate_report)
        generate_report_button.pack()

        # view_contract_button = tk.Button(self, text="View Contract", command=self.view_contract)


    def generate_report(self):
        # Get the selected contract number and generate the report
        contract_number = int(self.contract_var.get())
        data = OrderData.get_trim(contract_number)
        headers = OrderData.get_headers_for_trim_labels(contract_number)
        print(headers)
        if data:
            GenerateReport.generate_report_all_trim(headers, data)
            GenerateReport.generate_report_each_trim(headers, contract_number)
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
            contract_data = OrderData.get_contract_data(selected_contract)
            if contract_data:
                # add the contract data to the contract_data_frame
                for i, (key, value) in enumerate(contract_data.items()):
                    label_key = tk.Label(self.contract_data_frame, text=key)
                    label_key.grid(row=i, column=0, sticky='w')
                    label_value = tk.Label(self.contract_data_frame, text=value)
                    label_value.grid(row=i, column=1, sticky='w')

                    
if __name__ == '__main__':
    app = CVS()
    app.mainloop()