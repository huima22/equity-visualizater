from yahooquery import Ticker
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as data
def getFinancialData(ticker,types):
	data = Ticker(ticker).get_financial_data(types, trailing=False)
	if data is not None:
		return data
	else:
		return None

def getIncomeAnalysis(ticker):
	dfGrossProfitEbit = getFinancialData(ticker, ['GrossProfit', 'EBIT'])
	dfNetIncomeRevenue = getFinancialData(ticker, ['TotalRevenue', 'NetIncome'])
	if dfGrossProfitEbit is not None and dfNetIncomeRevenue is not None:
		df = pd.merge(dfGrossProfitEbit, dfNetIncomeRevenue, 'inner', on='asOfDate')
		df['Year'] = pd.DatetimeIndex(df['asOfDate']).year
		df = df.drop(['asOfDate'], axis=1)
		return df
	else:
		return None
	#df.plot(kind='line', x='asOfDate', y=['NetIncome', 'TotalRevenue', 'GrossProfit', 'EBIT'])


def getExpenseAnalysis(ticker):
	dfSGA = getFinancialData(ticker,['SellingGeneralAndAdministration']).drop(['periodType'],axis=1).rename(columns={'SellingGeneralAndAdministration' : 'SG&A'})
	dfRandD = getFinancialData(ticker,['ResearchAndDevelopment']).drop(['periodType'],axis=1).rename(columns={'ResearchAndDevelopment' : 'R&D'})
	dfCOGS = getFinancialData(ticker,['CostOfRevenue','InterestExpense']).drop(['periodType'],axis=1).rename(columns={'CostOfRevenue' : 'COGS', 'InterestExpense':'Interest'})
	dfOtherOperating = getFinancialData(ticker,['OperatingExpense']).drop(['periodType'],axis=1).rename(columns={'OperatingExpense' : 'Operation'})
	df1 = pd.merge(dfSGA, dfRandD, on=['asOfDate'])
	df2 = pd.merge(dfCOGS, dfOtherOperating, on='asOfDate')
	expenseData = pd.merge(df1, df2, on=['asOfDate'])
	#start_date, end_date = '2016-01-01', '2016-12-31'
	expenseData['Year'] = pd.DatetimeIndex(expenseData['asOfDate']).year
	expenseData = expenseData.drop(['asOfDate'],axis=1)
	expenseData.set_index('Year', inplace=True)
	dfTranspose = expenseData.transpose()
	#print(dfTranspose)
	return dfTranspose
	#df2015.plot.pie(y=['SellingGeneralAndAdministration','ResearchAndDevelopment','CostOfRevenue','InterestExpense','OperatingExpense'])
	#dfTranspose.plot.pie(subplots=True,autopct='%.2f',labeldistance=True, legend=False,figsize=(5, 5))


def getLiabilityAnalysis(ticker):
	dfLiability = getFinancialData(ticker, ['LongTermDebt','CurrentDebt','CurrentDeferredRevenue','DeferredIncomeTax','AccountsPayable']).drop(['periodType'], axis=1)
	dfLiability['Year'] = pd.DatetimeIndex(dfLiability['asOfDate']).year
	dfLiability = dfLiability.drop(['asOfDate'], axis=1)
	#dfLiability.plot(kind='bar', x='Year', y=['LongTermDebt', 'CurrentDebt', 'CurrentDeferredRevenue', 'DeferredIncomeTax','AccountsPayable'])
	return dfLiability
#def getAssetAnalysis(ticker):
#def getRatioAnalysis(ticker):

def main():
	getIncomeAnalysis('aapl')
	getExpenseAnalysis('aapl')
	getLiabilityAnalysis('aapl')

	plt.show()

if __name__== "__main__":
  main()

