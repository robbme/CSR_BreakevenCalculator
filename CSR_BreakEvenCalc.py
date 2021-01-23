import mintapi
import pandas as pd
import numpy as np
import gspread
from datetime import datetime, date, timedelta
import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from mintconfig import username, password

mint = mintapi.Mint(
    username,  # Email used to log in to Mint
    password,  # Your password used to log in to mint
 
    # Optional parameters
    mfa_method='sms',  # Can be 'sms' (default), 'email', or 'soft-token'.
                       # if mintapi detects an MFA request, it will trigger the requested method
                       # and prompt on the command line.
    headless=False,  # Whether the chromedriver should work without opening a
                     # visible window (useful for server-side deployments)
    mfa_input_callback=None,  # A callback accepting a single argument (the prompt)
                              # which returns the user-inputted 2FA code. By default
                              # the default Python `input` function is used.
    session_path=None, # Directory that the Chrome persistent session will be written/read from.
                       # To avoid the 2FA code being asked for multiple times, you can either set
                       # this parameter or log in by hand in Chrome under the same user this runs
                       # as.
    imap_account=None, # account name used to log in to your IMAP server
    imap_password=None, # account password used to log in to your IMAP server
    imap_server=None,  # IMAP server host name
    imap_folder='INBOX',  # IMAP folder that receives MFA email
    wait_for_sync=False,  # do not wait for accounts to sync
    wait_for_sync_timeout=300,  # number of seconds to wait for sync
)

accountName = 'CREDIT CARD'


monthlyPoints = 0.0
d_tPoints = 0.0
regPoints = 0.0


transactions = mint.get_transactions()
transactions = transactions[transactions.account_name == accountName]

transactions = transactions.drop(["description", "original_description","labels","notes"], axis=1)
transactions = transactions[(transactions.category != 'credit card payment') & (transactions.category != 'service fee')]
transactions = transactions[transactions.transaction_type != 'credit']



#find how to get current date(api with chase somehow?) or just current month?
s_date = datetime.date(datetime.now()) - timedelta(365)
#today
e_date = datetime.date(datetime.now())

start_date = s_date.strftime("%m/%d/%Y")
end_date = e_date.strftime("%m/%d/%Y")

after_start_date = transactions["date"] >= start_date
before_end_date = transactions["date"] <= end_date
between_dates = after_start_date & before_end_date
filtered_dates = transactions.loc[between_dates]

t_dtransactions = filtered_dates[transactions["category"].isin(["restaurants","hotel","air travel"])]
other_transactions = filtered_dates[~transactions["category"].isin(["restaurants","hotel","air travel"])]

yearBreakevenPoints = 10000

t_dPoints = t_dtransactions['amount'].sum() * 3
regPoints = other_transactions['amount'].sum()

totalPoints = t_dPoints + regPoints
#multiply points to get point totals
#find out where I should be  in the points
#print that result out

print(totalPoints)