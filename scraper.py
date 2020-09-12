from yahooquery import Ticker
import matplotlib.pyplot as plt
import pandas as pd

def getFinancialData(ticker,types):
	"""
	Method to read yahoo finance data from API
	"""
	try:
		data = Ticker(ticker).get_financial_data(types, trailing=False)
		if data is not None:
			return data
		else:
			return None
	except:
		return None

def getIncomeAnalysis(ticker):
	"""
	Method to construct data for income analysis
	"""
	dfGrossProfitEbit = getFinancialData(ticker, ['GrossProfit', 'EBIT'])
	dfNetIncomeRevenue = getFinancialData(ticker, ['TotalRevenue', 'NetIncome'])
	if dfGrossProfitEbit is not None and dfNetIncomeRevenue is not None:
		df = pd.merge(dfGrossProfitEbit, dfNetIncomeRevenue, 'inner', on='asOfDate')
		df['Year'] = pd.DatetimeIndex(df['asOfDate']).year
		df = df.drop(['asOfDate'], axis=1)
		return df
	else:
		return None


def getExpenseAnalysis(ticker):
	"""
	Method to construct data for expense analysis
	"""
	dfSGA = getFinancialData(ticker,['SellingGeneralAndAdministration']).drop(['periodType'],axis=1).rename(columns={'SellingGeneralAndAdministration' : 'SG&A'})
	dfRandD = getFinancialData(ticker,['ResearchAndDevelopment']).drop(['periodType'],axis=1).rename(columns={'ResearchAndDevelopment' : 'R&D'})
	dfCOGS = getFinancialData(ticker,['CostOfRevenue','InterestExpense']).drop(['periodType'],axis=1).rename(columns={'CostOfRevenue' : 'COGS', 'InterestExpense':'Interest'})
	dfOtherOperating = getFinancialData(ticker,['OperatingExpense']).drop(['periodType'],axis=1).rename(columns={'OperatingExpense' : 'Operation'})
	df1 = pd.merge(dfSGA, dfRandD, on=['asOfDate'])
	df2 = pd.merge(dfCOGS, dfOtherOperating, on='asOfDate')
	expenseData = pd.merge(df1, df2, on=['asOfDate'])
	expenseData['Year'] = pd.DatetimeIndex(expenseData['asOfDate']).year
	expenseData = expenseData.drop(['asOfDate'],axis=1)
	expenseData.set_index('Year', inplace=True)
	dfTranspose = expenseData.transpose()
	return dfTranspose


def getLiabilityAnalysis(ticker):
	"""
	Method to construct data for liability analysis
	"""
	dfLiability = getFinancialData(ticker, ['LongTermDebt','CurrentDebt','CurrentDeferredRevenue','DeferredIncomeTax','AccountsPayable']).drop(['periodType'], axis=1)
	dfLiability['Year'] = pd.DatetimeIndex(dfLiability['asOfDate']).year
	dfLiability = dfLiability.drop(['asOfDate'], axis=1)
	return dfLiability



