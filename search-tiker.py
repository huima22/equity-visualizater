
import tkinter as tk
from main import AutocompleteEntry
from main import NO_RESULTS_MESSAGE
import pandas_datareader.data as data
import matplotlib.pyplot as plt
from scraper import getIncomeAnalysis
from scraper import getExpenseAnalysis
from scraper import getLiabilityAnalysis
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


        label = tk.Label(self, text="Search company name ")
        label.pack()

        self.entry = AutocompleteEntry(self)
        self.build(case_sensitive=False, no_results_message=NO_RESULTS_MESSAGE)
        self.entry.pack(after=label)
        self.nr = tk.StringVar()


    def _update(self, *args):
        case_sensitive = False
        if self.cs.get() == "1":
            case_sensitive = False
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


def getGraphIncomeAnalysis():
    company_name = root.children['!autocompleteentry'].selected_value
    company_tiker = code_dic[company_name].lower()
    print(company_tiker)
    df = getIncomeAnalysis(company_tiker)
    if(df is not None):
        df.plot(kind='line', x='asOfDate', y=['NetIncome', 'TotalRevenue', 'GrossProfit', 'EBIT'])
    else:
        tk.messagebox.showinfo(title='Information', message='Service Not Available')

def getGraphExpenseAnalysis():
    company_name = root.children['!autocompleteentry'].selected_value
    company_tiker = code_dic[company_name]
    df = getExpenseAnalysis(company_tiker)
    if (df is not None):
        df.plot.pie(subplots=True, autopct='%.2f', labeldistance=True, legend=False, figsize=(5, 5))
        plt.show()
    else:
        tk.messagebox.showinfo(title='Information', message='Service Not Available')
def getGraphLiabilityAnalysis():
    company_name = root.children['!autocompleteentry'].selected_value
    company_tiker = code_dic[company_name]
    df = getLiabilityAnalysis(company_tiker)
    if (df is not None):
        df.plot(kind='bar', x='Year',
                         y=['LongTermDebt', 'CurrentDebt', 'CurrentDeferredRevenue', 'DeferredIncomeTax',
                            'AccountsPayable'])
        plt.show()
    else:
        tk.messagebox.showinfo(title='Information', message='Service Not Available')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Equity Performance Visualizer")
    root.tk_setPalette("white")

    application = Application(root)
    application.grid(row=1, column=2, columnspan=3)
   # application.pack()

    b1 = tk.Button(root, text='Income Analysis', width=15, height=2, command=getGraphIncomeAnalysis)
    b1.grid(row=1, column =7, sticky = 'n', padx = 3)
    b2 = tk.Button(root, text='Expense Analysis', width=15, height=2, command=getGraphExpenseAnalysis)
    b2.grid(row=1, column= 8,  sticky = 'n', padx = 3)
    b3 = tk.Button(root, text='Liability Analysis', width=15, height=2, command=getGraphLiabilityAnalysis)
    b3.grid(row=1, column= 9,  sticky = 'n', padx = 3)

    root.mainloop()