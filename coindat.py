import json
import urllib.request
import pandas as pd


##Please get your API key from Nomics##

API_KEY_NOMICS = 'YOUR API KEY HERE'


def main():
    pd.options.display.float_format = '{:,.2f}'.format
    print('Gathering Currency Volumes')
    print(convert_volumes())
    print("Top Ten Day Volume List")
    print(get_day_list())
    print("Top Ten Week Volume List")
    print(get_week_volume())


def get_prices():
    url = "https://api.nomics.com/v1/prices?key={}".format(API_KEY_NOMICS)
    parsed_resp_obj = json.loads(urllib.request.urlopen(url).read())
    return parsed_resp_obj


def get_filtered_volumes_overview():
    url = "https://api.nomics.com/v1/dashboard?key={}".format(API_KEY_NOMICS)
    data = urllib.request.urlopen(url).read()
    parsed_data = json.loads(data)
    volumes = []
    for market in parsed_data:
        market_item = {
            'currency': market['currency'],
            'day_volume': market['dayVolume'],
            'week_volume': market['weekVolume'],
            'month_volume': market['monthVolume']
        }
        volumes.append(market_item)
    return volumes


def get_df_volumes():
    df_prices = pd.DataFrame(get_prices())
    df_prices['currency'] = df_prices['currency'].astype(str)

    df_volumes = pd.DataFrame(get_filtered_volumes_overview())
    df_volumes['currency'] = df_volumes['currency'].astype(str)

    df_merged = pd.merge(df_volumes, df_prices, on='currency', how='outer')
    return df_merged


def convert_volumes():
    df_volumes = get_df_volumes()
    df_volumes['month_volume'] = df_volumes['month_volume'].astype(float)
    df_volumes['week_volume'] = df_volumes['week_volume'].astype(float)
    df_volumes['day_volume'] = df_volumes['day_volume'].astype(float)
    df_volumes = df_volumes.sort_values(by='month_volume', ascending=False).head(20)
    return df_volumes


def print_json(your_json):
    print(your_json)
    if isinstance(your_json, bytes):
        parsed = json.loads(your_json)
        print(json.dumps(parsed, indent=4, sort_keys=True))

    elif isinstance(your_json, list):
        print(json.dumps(your_json, indent=4, sort_keys=True))


def get_day_list():
    volumes_list = convert_volumes()
    volumes_list = volumes_list.sort_values(by='day_volume', ascending=False).head(10)
    return volumes_list


def get_week_volume():
    week_volumes = convert_volumes()
    week_volumes = week_volumes.sort_values(by='week_volume', ascending=False).head(10)
    return week_volumes


if __name__ == '__main__':
    main()
