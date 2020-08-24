
import tkinter as tk
from tkinter import ttk
from main import AutocompleteEntry
from main import NO_RESULTS_MESSAGE
import pandas_datareader.data as data

all_ticker = data.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)
all_ticker = all_ticker.drop(columns=['Nasdaq Traded', 'Listing Exchange',
                                          'Market Category', 'ETF', 'Round Lot Size', 'Test Issue',
                                          'Financial Status', 'CQS Symbol', 'NASDAQ Symbol', 'NextShares'])
all_ticker = all_ticker.reset_index()
all_ticker = all_ticker.set_index('Security Name')
code_dic = all_ticker.to_dict()
code_dic = code_dic.get('Symbol')
print(code_dic.keys())

class Application(tk.Frame, object):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)


        label = tk.Label(self, text="Enter the company name to search for ")
        label.pack()

        self.entry = AutocompleteEntry(self)
        self.build(case_sensitive=False, no_results_message=NO_RESULTS_MESSAGE)
        self.entry.pack(after=label)

        self.nr = tk.StringVar()


    def _update(self, *args):
        case_sensitive = False
        if self.cs.get() == "1":
            case_sensitive = True
        no_results_message = self.nr.get()
        self.build(
            case_sensitive=case_sensitive,
            no_results_message=no_results_message
        )

    def build(self, *args, **kwargs):
        self.entry.build(
            code_dic.keys(),
            kwargs["case_sensitive"],
            kwargs["no_results_message"]
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Equity Performance Visualizer")
    root.tk_setPalette("white")

    application = Application(root)
    application.pack()

    root.mainloop()