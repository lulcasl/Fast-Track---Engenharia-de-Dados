import json
from urllib.request import urlopen
from datetime import datetime, timedelta

def get_brazilian_holidays(year):
   
    # URL da API
    url = f"https://brasilapi.com.br/api/feriados/v1/{year}"
    
    # Criar requisição com User-Agent (se identifica como navegador)
    from urllib.request import Request
    
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    # HTTP requisition
    with urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # Converter strings de data para objetos datetime
    holidays = []
    for holiday in data:
        date_str = holiday['date']  # Ex: "2025-01-01"
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        holidays.append(date_obj)
    
    return holidays

# Test the function
if __name__ == "__main__":
    print("Testing get_brazilian_holidays...")
    holidays_2025 = get_brazilian_holidays(2025)
    print(f"Total holidays in 2025: {len(holidays_2025)}")
    print("\nFirst 5 holidays:")
    for h in holidays_2025[:5]:
        print(f"  - {h.strftime('%Y-%m-%d')}")