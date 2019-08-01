import pandas
import os
import re


pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 10000)

#stocklist = ['της Ελλάδος']

if __name__ == '__main__':
    mylist = []
    for chunk in pandas.read_csv(os.path.join('data', 'news2.csv'), sep='\t', chunksize=10000):
        chunk['date'] = pandas.to_datetime(chunk['date'], format="%d/%m/%Y")
        chunk.drop(columns='Unnamed: 0', inplace=True)
        chunk.dropna(how='any', axis=0, inplace=True)  # αφαιρώ τα nan γιατί κράσαρε
        chunk.drop_duplicates(subset='news', inplace=True)  # remove rows with duplicate news
        cols = ['news','tags']
        chunk[cols] = chunk[cols].astype(str)
        mask = chunk['news'].str.contains('[τΤ]ρ[αά]π[εέ]ζ(α|ης|ας|ες)')
        df1 = chunk[mask]
        mylist.append(df1)

    selection = pandas.concat(mylist, axis=0)
    del mylist

    selection2 = selection.sort_values('date').groupby('date').agg(lambda x: ', '.join(map(str, x)))
    # # remove duplicates tags
    for i, row in selection2.iterrows():
        tags = [tag.replace(' ','') for tag in row['tags'].split(',')]
        row['tags'] = ' '.join(set(tags))

    selection2.reset_index(inplace=True)
    df2 = pandas.read_csv(
        os.path.join(
            os.path.join('data', 'historical_prices'),
            'ETE.ATH.tsv'),
        sep='\t')
    df2.rename(columns={'Trade Date': 'date'}, inplace=True)
    cols = ['Open', 'Close', 'High', 'Low', 'Prev. Close']
    df2[cols] = df2[cols].replace({',': '.'}, regex=True)
    df2[cols] = df2[cols].astype(float)
    df2 = df2[(df2 != 0).all(1)]  # select all rows that not zero
    df2['date'] = pandas.to_datetime(df2['date'], format="%d/%m/%Y")

    final = pandas.merge(df2, selection2, on='date')
    final.sort_values(by=['date'], inplace=True)
    cols = ['news', 'tags']
    final[cols] = final[cols].astype(str)
    final.to_csv(os.path.join('data','dataset1.tsv'), sep='\t')

    df2 = pandas.read_csv(
        os.path.join(
            os.path.join('data', 'historical_prices'),
            'ALPHA.ATH.tsv'),
        sep='\t')
    df2.rename(columns={'Trade Date': 'date'}, inplace=True)
    cols = ['Open', 'Close', 'High', 'Low', 'Prev. Close']
    df2[cols] = df2[cols].replace({',': '.'}, regex=True)
    df2[cols] = df2[cols].astype(float)
    df2 = df2[(df2 != 0).all(1)]  # select all rows that not zero
    df2['date'] = pandas.to_datetime(df2['date'], format="%d/%m/%Y")

    final = pandas.merge(df2, selection2, on='date')
    final.sort_values(by=['date'], inplace=True)
    cols = ['news', 'tags']
    final[cols] = final[cols].astype(str)
    final.to_csv(os.path.join('data', 'dataset2.tsv'), sep='\t')

    df2 = pandas.read_csv(
        os.path.join(
            os.path.join('data', 'historical_prices'),
            'EUROBE.ATH.tsv'),
        sep='\t')
    df2.rename(columns={'Trade Date': 'date'}, inplace=True)
    cols = ['Open', 'Close', 'High', 'Low', 'Prev. Close']
    df2[cols] = df2[cols].replace({',': '.'}, regex=True)
    df2[cols] = df2[cols].astype(float)
    df2 = df2[(df2 != 0).all(1)]  # select all rows that not zero
    df2['date'] = pandas.to_datetime(df2['date'], format="%d/%m/%Y")

    final = pandas.merge(df2, selection2, on='date')
    final.sort_values(by=['date'], inplace=True)
    cols = ['news', 'tags']
    final[cols] = final[cols].astype(str)
    final.to_csv(os.path.join('data', 'dataset3.tsv'), sep='\t')


