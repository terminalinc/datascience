from src.tool.currency_rates import * 

def run_tool():
    
    # Run function to get latest currency rates since last time tool was run
    get_latest_currency_rates()
    
if __name__ == '__main__':
    run_tool()