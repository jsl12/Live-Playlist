from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_tables(url):
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    names = [tag.find_previous('h5').text.split('//')[0].strip() for tag in soup.find_all('table')]
    dfs = [table_to_df(tab) for tab in soup.find_all('table')]
    return pd.concat(dfs)
    # return {name: df for name, df in zip(names, dfs)}

def table_to_df(table_tag):
    cols = [head.text for head in table_tag.find('thead').find_all('th')]
    df = pd.DataFrame(
        [pd.Series([t.text for t in row.find_all('td')], index=cols) for row in table_tag.find('tbody').find_all('tr')]
    )
    df = df.set_index(df.columns[0])
    return df

if __name__ == '__main__':
    url = r'https://www.kexp.org/read/2018/12/17/kexp-staff-volunteers-interns-top-10-albums-2018-part-1/'
    df1 = get_tables(url)

    url = r'https://www.kexp.org/read/2018/12/18/kexp-staff-volunteers-interns-top-10-albums-2018-part-2/'
    df2 = get_tables(url)
    df2.columns = df1.columns

    df = pd.concat([df1, df2])
    dfc = df.groupby('artist').size().sort_values()
    pass