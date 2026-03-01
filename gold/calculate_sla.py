import json
from urllib.request import urlopen, Request
from datetime import datetime, timedelta

def get_brazilian_holidays(year):
   
    # URL da API
    url = f"https://brasilapi.com.br/api/feriados/v1/{year}"
    
    # Criar requisição com User-Agent (se identifica como navegador)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    # HTTP requisition
    with urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # Convert date strings to datetime objects on new empty list
    holidays = []
    for holiday in data:
        date_str = holiday['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        holidays.append(date_obj)
    
    return holidays

# Get all Brazilian holidays for the years covered by the date range
# This checks holidays from all years, depending on the issue start/end year
def get_holidays_for_date_range(start_date, end_date):
    start_year = start_date.year
    end_year = end_date.year
    
    # Empty list to store all holidays across the years
    all_holidays = []
    
    # Fetch holidays for each year in the range
    for year in range(start_year, end_year + 1):
        try:
            year_holidays = get_brazilian_holidays(year)
            all_holidays.extend(year_holidays)
        except Exception as e:
            # If API fails, continue without holidays for that year
            print(f"Warning: Could not fetch holidays for {year}: {e}")
    
    return all_holidays

# Calculate businesses hours between datetimes
# Excluding weekend and holidays as defined in the project documentation

def calculate_business_hours(start_date, end_date, holidays=None):
    
    # If both dates are the same, return 0 hours
    if start_date >= end_date:
        return 0
    
    # Fetch holidays if not provided
    if holidays is None:
        holidays = get_holidays_for_date_range(start_date, end_date)
    
    # If both dates are the same, return 0 hours
    if start_date >= end_date:
        return 0
    
    # Set working interval
    start_work_hour = 9 
    end_work_hour = 17
    total_work_hours = end_work_hour - start_work_hour

    # Convert holidays to date only format
    holiday_dates = [h.date() for h in holidays]
    
    business_hours = 0
    current_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date_only = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Process each day
    while current_date <= end_date_only:
        is_weekend = current_date.weekday() >= 5
        is_holiday = current_date.date() in holiday_dates
        
        # Check if it's a working day
        if not is_weekend and not is_holiday:
            # Define work hours for this day
            day_work_start = current_date.replace(hour=start_work_hour, minute=0, second=0) 
            day_work_end = current_date.replace(hour=end_work_hour, minute=0, second=0)
            
            # Adjust for start date
            if current_date.date() == start_date.date():
                # First day: use actual start time if after 9 AM
                # Ex: ticket was opened at 11 AM, so we start counting from 11 AM, not 9 AM
                actual_start = max(start_date, day_work_start)
            else:
                actual_start = day_work_start
            
            # Adjust for end date
            if current_date.date() == end_date.date():
                # Last day: use actual end time if before 5 PM
                actual_end = min(end_date, day_work_end)
            else:
                actual_end = day_work_end
            
            # Calculate hours for this day (only within working hours)
            if actual_start < actual_end:
                # Ensure we're within work hours
                if actual_start < day_work_start:
                    actual_start = day_work_start
                if actual_end > day_work_end:
                    actual_end = day_work_end
                
                if actual_start < actual_end:
                    hours_in_day = (actual_end - actual_start).total_seconds() / 3600
                    business_hours += hours_in_day
        
        # Move to next day
        current_date += timedelta(days=1)
    
    return business_hours
  
# Test the function. The __name__ == "__main__" is a common Python idiom that allows
# to run some code only when the script is executed directly, and not when it's imported 
# as a module in another script.
if __name__ == "__main__":
    print("=== TEST get_brazilian_holidays ===")
    # The year was set just for testing purposes.
    holidays = get_brazilian_holidays(2025)
    print(f"Total holidays in 2025: {len(holidays)}")
    print("\nAll holidays:")
    for h in holidays[:]:
        print(f"  - {h.strftime('%Y-%m-%d')}")
        
if __name__ == "__main__":        
    # Test calculate_business_hours
    print("\n=== TEST calculate_business_hours ===")
        
    # Test 1: Simple weekday calculation (no weekends, no holidays)
    start = datetime(2025, 1, 6, 9, 0)   # Monday 9 AM
    end = datetime(2025, 1, 8, 17, 0)     # Wednesday 5 PM
    hours = calculate_business_hours(start, end)
    print(f"\nTest 1: Mon 9AM to Wed 5PM")
    print(f"Business hours: {hours:.2f}h")
        
    # Test 2: Including weekend
    start = datetime(2025, 1, 10, 9, 0)   # Friday 9 AM
    end = datetime(2025, 1, 13, 17, 0)    # Monday 5 PM (trough weekend)
    hours = calculate_business_hours(start, end)
    print(f"\nTest 2: Fri 9AM to Mon 5PM (crosses weekend)")
    print(f"Business hours: {hours:.2f}h (should exclude Sat-Sun)")
        
    # Test 3: Including holiday
    start = datetime(2025, 1, 1, 9, 0)    # New Year (holiday)
    end = datetime(2025, 1, 3, 17, 0)     # Friday 5 PM
    hours = calculate_business_hours(start, end)
    print(f"\nTest 3: Jan 1 (holiday) to Jan 3")
    print(f"Business hours: {hours:.2f}h (should exclude Jan 1)")