import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def upload_csv_to_gsheet():
    # Read CSV
    df = pd.read_csv('data/fm_data_23_68_filtered.csv')
    
    # Set up credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    
    # Authorize
    client = gspread.authorize(credentials)
    
    # Create new spreadsheet
    spreadsheet = client.create('FM_Radio_Stations')
    
    # Get the first sheet
    worksheet = spreadsheet.get_worksheet(0)
    
    # Update the sheet with DataFrame
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    
    # Share the spreadsheet (optional)
    spreadsheet.share('deardevx@gmail.com', perm_type='user', role='writer')
    
    print(f"Spreadsheet ID: {spreadsheet.id}")

if __name__ == '__main__':
    upload_csv_to_gsheet()