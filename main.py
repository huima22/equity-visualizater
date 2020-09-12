import tkinter as tk
import tkinter.ttk as ttk
from autocompletebox import AutocompleteEntry
from autocompletebox import NO_RESULTS_MESSAGE
import pandas_datareader.data as data
from scraper import getIncomeAnalysis
from scraper import getExpenseAnalysis
from scraper import getLiabilityAnalysis
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")

all_ticker = data.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)
all_ticker = all_ticker.drop(columns=['Nasdaq Traded', 'Listing Exchange',
                                          'Market Category', 'ETF', 'Round Lot Size', 'Test Issue',
                                          'Financial Status', 'CQS Symbol', 'NASDAQ Symbol', 'NextShares'])
all_ticker = all_ticker.reset_index()
all_ticker = all_ticker.set_index('Security Name')
code_dic = all_ticker.to_dict()
code_dic = code_dic.get('Symbol')
class Application(tk.Frame, object):
    """Main Class of the application
       Methods:
       __init__ -- Set up the UI
       build -- pass company data to autocompletebox UI component
       _update -- on update pass input data to build
       getGraphIncomeAnalysis -- Plot graph for income analysis
       getGraphExpenseAnalysis -- Plot graph for expense analysis
       getGraphLiabilityAnalysis --Plot graph for liability analysis
       """
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.dataPlot = None
        self.lf = None
        self.entry = AutocompleteEntry(self)
        self.build(case_sensitive=False, no_results_message=NO_RESULTS_MESSAGE)
        self.entry.grid(row=2, column=2, rowspan=1, columnspan=2, padx=10, pady=3)
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
            kwargs["no_results_message"],

        )

    def getGraphIncomeAnalysis(self):
        self.clearCanvas()
        company_name = root.children['!autocompleteentry'].selected_value
        company_tiker = code_dic[company_name].lower()
        dataAvailable = True
        try:
            df = getIncomeAnalysis(company_tiker)
        except:
            tk.messagebox.showinfo(title='Information', message='Data partially not available')
            dataAvailable = False

        if(df is not None and dataAvailable):
            self.lf = ttk.Labelframe(root, text='Income Analysis')
            self.lf.grid(row=3, column=3, columnspan=10, sticky='s', padx=3, pady=3)
            f = Figure(figsize=(10, 6), dpi=100)
            ax = f.add_subplot(111)
            df.plot(kind='line', x='Year', y=['NetIncome', 'TotalRevenue', 'GrossProfit', 'EBIT'],ax=ax)
            self.dataPlot = FigureCanvasTkAgg(f, master=self.lf)
            self.dataPlot.get_tk_widget().grid(row=3, column=3, columnspan=10)
            self.dataPlot.draw()

        else:
            tk.messagebox.showinfo(title='Information', message='Service Not Available')

    def getGraphExpenseAnalysis(self):
        self.clearCanvas()
        company_name = root.children['!autocompleteentry'].selected_value
        company_tiker = code_dic[company_name]
        dataAvailable = True
        try:
            df = getExpenseAnalysis(company_tiker)
        except:
            tk.messagebox.showinfo(title='Information', message='Data partially not available')
            dataAvailable = False
        if (df is not None and dataAvailable):
            self.lf = ttk.Labelframe(root, text='Expense Analysis')
            self.lf.grid(row=3, column=3, columnspan=10, sticky='s', padx=3, pady=3)

            fig, axes = plt.subplots(nrows=2, ncols=2)
            for ax, col in zip(axes.flat, df.columns):
                ax.pie(df[col], labels=df.index, autopct='%.2f')
                ax.set(title=col, aspect='equal')
            axes[0, 0].legend(bbox_to_anchor=(0, 0.5))
            self.dataPlot = FigureCanvasTkAgg(fig, master= self.lf)
            self.dataPlot.get_tk_widget().grid(row=3, column=3, columnspan=10)
            self.dataPlot.draw()


        else:
            tk.messagebox.showinfo(title='Information', message='Service Not Available')

    def getGraphLiabilityAnalysis(self):
        self.clearCanvas()
        company_name = root.children['!autocompleteentry'].selected_value
        company_tiker = code_dic[company_name]
        dataAvailable = True
        try:
            df = getLiabilityAnalysis(company_tiker)
        except:
            tk.messagebox.showinfo(title='Information', message='Data partially not available')
            dataAvailable = False
        if (df is not None and dataAvailable):
            self.lf = ttk.Labelframe(root, text='Liability Analysis')
            self.lf.grid(row=3, column=3, columnspan=10,sticky='s', padx=3, pady=3)
            f = Figure(figsize=(10, 6), dpi=100)
            ax = f.add_subplot(111)
            df.plot(kind='bar', x='Year',ax=ax)
            self.dataPlot = FigureCanvasTkAgg(f, master=self.lf)
            self.dataPlot.draw()
            self.dataPlot.get_tk_widget().grid(row=3, column=3, columnspan=10)
            self.dataPlot.get_tk_widget().grid(row=3, column=3, columnspan=10)
        else:
            tk.messagebox.showinfo(title='Information', message='Service Not Available')

    def clearCanvas(self):
        if(self.dataPlot is not None):
            self.dataPlot.get_tk_widget().destroy()
            self.lf.destroy()
            self.dataPlot = None

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    root.title("Company Performance Visualizer")
    root.tk_setPalette("white")

    application = Application(root)
    application.grid(row=1, column=1, columnspan=1)
    b1 = tk.Button(root, text='Income Analysis', width=15, height=2, command=application.getGraphIncomeAnalysis)
    b1.grid(row=1, column =5, rowspan=2, sticky = 'nw', pady=5,padx = 5)
    b2 = tk.Button(root, text='Expense Analysis', width=15, height=2, command=application.getGraphExpenseAnalysis)
    b2.grid(row=1, column= 6, rowspan=2, sticky = 'nw',pady=5, padx = 5)
    b3 = tk.Button(root, text='Liability Analysis', width=15, height=2, command=application.getGraphLiabilityAnalysis)
    b3.grid(row=1, column= 7, rowspan=2, sticky = 'nw',pady=5, padx = 5)

    root.mainloop()