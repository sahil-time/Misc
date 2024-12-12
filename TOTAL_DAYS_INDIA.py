from datetime import datetime
from colorama import Fore, Style, init

# FORMAT - "YYYY-MM-DD" as [ ARRIVAL in US, DEPARTURE from US ] i.e. TOTAL INDIA TRIPS
dates = [
"2024-12-31", "2024-09-21",
"2024-02-18", "2024-02-10", #10
"2024-01-12", "2023-11-07",
"2023-02-11", "2023-01-01",
"2022-09-23", "2022-07-23",
"2022-02-22", "2021-11-18",
"2021-01-24", "2020-09-04", #5
"2020-01-13", "2019-11-29",
"2019-01-31", "2018-12-23",
"2017-01-24", "2016-12-10",
"2016-08-15", "2016-05-10"  #1
]

FIRST_DATETIME = datetime(2015, 8, 6) # 6th Aug 2015 [ Left for USA ]

############## DO NOT CHANGE BELOW ##############

init()
date_format = "%Y-%m-%d" # Define the date format 

# Function to calculate days between two dates
def calculate_days(date1_str, date2_str):
    # Convert string dates to datetime objects
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    # Calculate the difference and return the number of days
    return (date2 - date1).days

print("")
print("-------------- INDIA TRIPS --------------")
print("")
TOTAL_DAYS_INDIA = 0
# Iterate through the date pairs and calculate the days between each pair
for i in range(0, len(dates), 2):  # Step by 2 to get pairs
    date2 = dates[i]
    date1 = dates[i + 1]
    total_days = calculate_days(date1, date2) - 3 # Remove 3 days PER trip coz travel
    TOTAL_DAYS_INDIA += total_days
    tmp1 = datetime.strptime(date1, "%Y-%m-%d").strftime("%d-%b-%Y")
    tmp2 = datetime.strptime(date2, "%Y-%m-%d").strftime("%d-%b-%Y")

    print(f"Total days in INDIA between {Fore.RED}{tmp1}{Fore.RESET} & {Fore.RED}{tmp2}{Fore.RESET}: {Style.BRIGHT}{total_days}{Style.RESET_ALL} days")

print("")
print("-------------- OVERALL STATS --------------")
print("")
TOTAL_DAYS_ELAPSED = datetime.today() - FIRST_DATETIME
TOTAL_DAYS_USA = TOTAL_DAYS_ELAPSED.days - TOTAL_DAYS_INDIA
TOTAL_PCT_INDIA = round(TOTAL_DAYS_INDIA*100/TOTAL_DAYS_ELAPSED.days, 1)
FIRST_DATETIME_STR = FIRST_DATETIME.strftime("%d %B %Y")
print(f"TOTAL DAYS ELAPSED SINCE {Style.BRIGHT}'{FIRST_DATETIME_STR}': {Fore.BLUE}{TOTAL_DAYS_ELAPSED.days} days{Style.RESET_ALL}{Fore.RESET}")
print(f"TOTAL DAYS INDIA: {Fore.CYAN}{Style.BRIGHT}{TOTAL_DAYS_INDIA} days{Style.RESET_ALL}{Fore.RESET}")
print(f"TOTAL DAYS USA: {Fore.MAGENTA}{Style.BRIGHT}{TOTAL_DAYS_USA} days{Style.RESET_ALL}{Fore.RESET}")
print(f"TOTAL % INDIA: {Fore.GREEN}{Style.BRIGHT}{TOTAL_PCT_INDIA} %{Style.RESET_ALL}{Fore.RESET} in INDIA")

print("")
