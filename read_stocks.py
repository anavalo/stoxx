import time
import warnings
import wget
import os
import pandas

from config import stocks

if __name__ == '__main__':
    if not os.path.isdir('historical_prices'):
        os.mkdir('historical_prices')
    for symbol in set(stocks.values()):
        url = 'https://www.naftemporiki.gr/finance/Data/getHistoryData.aspx?symbol=' + symbol + '&type=csv&period=5y'
        try:
            filename = wget.download(url)
            df = pandas.read_csv(filename, sep=';', index_col='Trade Date')\
                .filter(['Trade Date','High','Low','Open','Close','Volume','Prev. Close','Total Turnover','Num. Of Trans.'])
            df.to_csv(filename, sep='\t', index='Trade Date')
            os.rename(filename, os.path.join('historical_prices', symbol+'.tsv'))
        except:
            warnings.warn('No historical data for'+symbol)
            pass
        time.sleep(0.5)

    #dr.DataReader(symbol, 'yahoo', start, end).to_csv(symbol + '.csv')
    #load_yahoo_quote(ticker=symbol, begindate='20190301', enddate='20190329').to_csv(symbol + '.csv')



