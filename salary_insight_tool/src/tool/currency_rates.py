def get_curr_rate(base, start_date, end_date):
    import requests
    from src.tool.constants import API_KEY

    url = ('https://api.exchangeratesapi.io/v1/timeseries?access_key={API_KEY}&base={base}&symbols=USD&start_date={start_date}&end_date={end_date}'
            .format(start_date = start_date, 
                    end_date = end_date,
                    API_KEY = API_KEY, 
                    base = base))
    
    output = requests.get(url, timeout = 120)
    return output

def get_latest_currency_rates():
    
    import pandas as pd
    from datetime import datetime, timedelta
    from time import sleep
    
    curr_list = pd.read_csv("data/reference/currency_list.csv")
    currency_ref_df = pd.read_csv("data/reference/currency_ref_df.csv")
    
    todays_date = datetime.today().date()
    currency_ref_df['date'] = pd.to_datetime(currency_ref_df['date'])
    
    c = curr_list['currency'][0]
    
    
    for base in list(curr_list['currency']):
        
        if base != 'USD':
            
            data = currency_ref_df[currency_ref_df['currency'] == base]
            
            if len(data) > 0:
            
                latest_curr_date = ((data.sort_values('date', ascending = False)
                                       .reset_index(drop=True)['date'][0]
                                       .date()))
                
                if (todays_date - latest_curr_date).days > 0:
                    output = get_curr_rate(base, start_date = str(latest_curr_date), end_date = str(todays_date) ).json()
                            
                    cur_df = pd.DataFrame({'currency': base, 'date': list(output['rates'].keys())})
                    cur_df['rate'] = [output['rates'][d]['USD'] for d in cur_df['date']]
                    cur_df['date'] = pd.to_datetime(cur_df['date'])
        
                    currency_ref_df = pd.concat([currency_ref_df, cur_df], axis = 0)
                                
                    sleep(10)
                    
            else:
                output = get_curr_rate(base, start_date = str(todays_date - timedelta(days = 180)), end_date = str(todays_date) ).json()
                        
                cur_df = pd.DataFrame({'currency': base, 'date': list(output['rates'].keys())})
                cur_df['rate'] = [output['rates'][d]['USD'] for d in cur_df['date']]
                cur_df['date'] = pd.to_datetime(cur_df['date'])
                
                currency_ref_df = pd.concat([currency_ref_df, cur_df], axis = 0)
                            
                sleep(10)

    currency_ref_df = currency_ref_df.drop_duplicates()
    currency_ref_df.to_csv("data/reference/currency_ref_df.csv", index = False)

    print('---Currency Data Updated---')

# get_latest_currency_rates()
