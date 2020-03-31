import requests
from bs4 import BeautifulSoup


def get_tables():

    url = 'https://www.bloomberg.com/markets/rates-bonds/government-bonds/us'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-languages': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br'
    }

    html = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')
    return html.find_all('div', {'class': 'table-container'})

def parse_asset(name_header):
    text = [x.text for x in name_header]
    text = text[0].split()
    symbol = text[0]
    if symbol[:2]=='GB': # TREASURY BILLS
        maturity = int(text[1])
        asset = 'bill'

        return symbol, asset, maturity

    elif symbol[:2]=='GT':
        maturity = 12 * int(text[1])
        if symbol[:2]=='GTI':
            asset = 'tips'
        else:
            asset = 'bond'

        return symbol, asset, maturity

    elif symbol[0]=='B': # MUNI BONDS
        maturity = int(text[3]) * 12
        asset = 'muni'

        return symbol, asset, maturity

    return None

def get():
    data = []

    for table in get_tables():
        title = table.find('h2', {'class': 'table-container_title'})
        sub_table = table.find('table', {'class': 'data-table'})
        for row in sub_table.find_all('tr'):
            if row['class']==['data-table-headers']:
                # COLUMN HEADERS
                temp = [x.text for x in row.find_all('th')]
                if 'Yield' in temp: # Ignore treasure targets
                    col_heads = temp
            else:
                asset = parse_asset(row.find_all('th'))
                if asset:
                    x = {'symbol': asset[0],
                         'type': asset[1],
                         'maturity': asset[2],}
                    x.update(
                        {k.lower(): v for k, v in
                         zip(col_heads[1:], [x.text for x in row.find_all('td')])}
                    )
                    x['yield'] = float(x['yield'].replace('%',''))

                    if 'price' in x.keys():
                        x['coupon'] = float(x['coupon'])
                        x['price'] = float(x['price'])

                    data.append(x)

    return data
