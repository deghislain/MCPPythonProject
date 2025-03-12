from typing import List
from datetime import datetime, timedelta


def get_income_statement_keys() -> List:
    return [
        'fiscalDateEnding',
        'reportedCurrency',
        'grossProfit',
        'totalRevenue',
        'costOfRevenue',
        'costofGoodsAndServicesSold',
        'operatingIncome',
        'sellingGeneralAndAdministrative',
        'researchAndDevelopment',
        'operatingExpenses',
        'investmentIncomeNet',
        'netInterestIncome',
        'interestIncome',
        'interestExpense',
        'nonInterestIncome',
        'otherNonOperatingIncome',
        'depreciation',
        'depreciationAndAmortization',
        'incomeBeforeTax',
        'incomeTaxExpense',
        'interestAndDebtExpense',
        'netIncomeFromContinuingOperations',
        'comprehensiveIncomeNetOfTax',
        'ebit',
        'ebitda',
        'netIncome'
    ]


def get_balance_sheet_keys() -> List:
    return ['fiscalDateEnding',
            'reportedCurrency',
            'totalAssets',
            'totalCurrentAssets',
            'cashAndCashEquivalentsAtCarryingValue',
            'cashAndShortTermInvestments',
            'inventory',
            'currentNetReceivables',
            'totalNonCurrentAssets',
            'propertyPlantEquipment',
            'accumulatedDepreciationAmortizationPPE',
            'intangibleAssets',
            'intangibleAssetsExcludingGoodwill',
            'goodwill',
            'investments',
            'longTermInvestments',
            'shortTermInvestments',
            'otherCurrentAssets',
            'otherNonCurrentAssets',
            'totalLiabilities',
            'totalCurrentLiabilities',
            'currentAccountsPayable',
            'deferredRevenue',
            'currentDebt',
            'shortTermDebt',
            'totalNonCurrentLiabilities',
            'capitalLeaseObligations',
            'longTermDebt',
            'currentLongTermDebt',
            'longTermDebtNoncurrent',
            'shortLongTermDebtTotal',
            'otherCurrentLiabilities',
            'otherNonCurrentLiabilities',
            'totalShareholderEquity',
            'treasuryStock',
            'retainedEarnings',
            'commonStock',
            'commonStockSharesOutstanding'
            ]


def get_cash_flow_keys() -> List:
    return [
        'fiscalDateEnding',
        'reportedCurrency',
        'operatingCashflow',
        'paymentsForOperatingActivities',
        'proceedsFromOperatingActivities',
        'changeInOperatingLiabilities',
        'changeInOperatingAssets',
        'depreciationDepletionAndAmortization',
        'capitalExpenditures',
        'changeInReceivables',
        'changeInInventory',
        'profitLoss',
        'cashflowFromInvestment',
        'cashflowFromFinancing',
        'proceedsFromRepaymentsOfShortTermDebt',
        'paymentsForRepurchaseOfCommonStock',
        'paymentsForRepurchaseOfEquity',
        'paymentsForRepurchaseOfPreferredStock',
        'dividendPayout',
        'dividendPayoutCommonStock',
        'dividendPayoutPreferredStock',
        'proceedsFromIssuanceOfCommonStock',
        'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet',
        'proceedsFromIssuanceOfPreferredStock',
        'proceedsFromRepurchaseOfEquity',
        'proceedsFromSaleOfTreasuryStock',
        'changeInCashAndCashEquivalents',
        'changeInExchangeRate',
        'netIncome'
    ]


def get_earnings_keys() -> List:
    return [
        'fiscalDateEnding',
        'reportedEPS'
    ]


def get_insider_tx_keys() -> List:
    return [
        'transaction_date',
        'ticker',
        'executive',
        'executive_title',
        'security_type',
        'acquisition_or_disposal',
        'shares',
        'share_price'
    ]


def get_weekly_adjusted_keys() -> List:
    return [
        '1. open',
        '2. high',
        '3. low',
        '4. close',
        '5. adjusted close',
        '6. volume',
        '7. dividend amount'
    ]


def get_date_one_week_ago(date_str):
    """
    This function accepts a date string in 'YYYY-MM-DD' format and returns the date one week prior.

    :param date_str: string, date in 'YYYY-MM-DD' format
    :return: string, date one week before the input date in 'YYYY-MM-DD' format
    """
    try:
        # Parse the input date string into a datetime object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        # Subtract one week using timedelta
        one_week_ago = date_obj - timedelta(weeks=1)

        # Format the datetime object back into a string
        one_week_ago_str = one_week_ago.strftime('%Y-%m-%d')

        return one_week_ago_str
    except ValueError as e:
        return f"Error: {str(e)}. Please ensure the date is in 'YYYY-MM-DD' format."
