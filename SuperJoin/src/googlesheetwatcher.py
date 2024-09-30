import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetWatcher:
    def __init__(self, spreadsheet_id, range_name, scopes):
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.scopes = scopes
        self.service = self.authenticate()
        self.prev_data = len(self.get_sheet_data())
        # self.pre_data = self.get_sheet_data()

    def authenticate(self):
        """Authenticate and return the Google Sheets API service."""
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.scopes)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
                credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

        try:
            service = build("sheets", "v4", credentials=credentials)
            return service
        except HttpError as error:
            print(f"An error occurred during authentication: {error}")
            return None

    def get_sheet_data(self):
        """Retrieve data from the Google Sheet."""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
            values = result.get("values", [])
            return values
        except HttpError as error:
            print(f"An error occurred while fetching the data: {error}")
            return []

    def detect_new_rows(self, current_data):
        """Detect newly added rows by comparing with previous data."""
        new_rows = []
        if current_data and len(current_data) > self.prev_data:
            new_rows = current_data[self.prev_data:]
        return new_rows

    def append_data(self, values):
        """Append a new row of data to the Google Sheet."""
        try:
            body = {
                'values': [values]  # Wrap the row in another list
            }
            sheet = self.service.spreadsheets()
            sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            message = "Data appended successfully to the Google Sheet."

            # Calculate the width for the table boundary
            width = len(message) + 2

            # Print the top boundary
            print("+" + "-" * width + "+")

            # Print the message with boundaries
            print(f"| {message} |")

            # Print the bottom boundary
            print("+" + "-" * width + "+")
        except HttpError as error:
            print(f"An error occurred while appending data: {error}")

    def find_row_by_reg_id(self, reg_id):
        """Find the row index of a given regID."""
        data = self.get_sheet_data()
        if not data:
            print("No data found in the sheet.")
            return None

        # Assuming regID is in the first column (index 1)
        for i, row in enumerate(data, start=2):  # start=2 to match the spreadsheet row number
            if len(row) > 0 and row[0] == reg_id:
                return i  # Return the row number

        print(f"regID {reg_id} not found.")
        return None

    def delete_row(self, row_number):
        """Delete the specified row number."""
        try:
            body = {
                "requests": [
                    {
                        "deleteDimension": {
                            "range": {
                                "sheetId": 0,  # Default is first sheet. Change this if working with multiple sheets.
                                "dimension": "ROWS",
                                "startIndex": row_number-1,  # Zero-indexed
                                "endIndex": row_number  # Exclusive end
                            }
                        }
                    }
                ]
            }

            self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
            message = f"Row {row_number} deleted successfully."

            # Calculate the width for the table boundary
            width = len(message) + 2

            # Print the top boundary
            print("+" + "-" * width + "+")

            # Print the message with boundaries
            print(f"| {message} |")

            # Print the bottom boundary
            print("+" + "-" * width + "+")
        except HttpError as error:
            print(f"An error occurred while deleting the row: {error}")

    def delete_row_by_reg_id(self, reg_id):
        """Find and delete a row based on regID."""
        row_number = self.find_row_by_reg_id(reg_id)
        if row_number:
            self.delete_row(row_number)

    # def detect_updated_rows(self):
    #     """Detect rows that have been updated in the Google Sheet."""
    #     current_data = self.get_sheet_data()  # Fetch current data
    #     updated_rows = []
    #
    #     # Compare each row of current_data with prev_data
    #     for i, row in enumerate(current_data):
    #         if i < len(self.pre_data):  # If there's a previous row to compare with
    #             if row != self.pre_data[i]:  # Check if the row has changed
    #                 updated_rows.append(row)
    #
    #     # Update prev_data after comparison
    #     self.pre_data = current_data
    #
    #     return updated_rows

    # def watch(self):
    #     """Start watching the Google Sheet for new rows."""
    #     # if not self.prev_data:
    #     #     print("No initial data found.")
    #     #     return
    #
    #     # print(f"Initial data: {self.prev_data}")
    #     # Polling loop to check for new data every 10 seconds
    #     while True:
    #         current_data = self.get_sheet_data()
    #         if current_data:
    #             new_rows = self.detect_new_rows(current_data)
    #             if new_rows and len(new_rows[0]) == 5:
    #                 # print(f"New rows added: {new_rows}")
    #                 self.prev_data = current_data  # Update previous data
    #                 print(new_rows)
    #             # else:
    #             #     print("No new rows added.")
    #         else:
    #             time.sleep(2)
    #             continue
    #             # print("Error retrieving data.")
    #         time.sleep(2)


# if __name__ == '__main__':
#     SPREADSHEET_ID = "1qWL1lnqYe-KTP9vfdLKbnQkEaWcCi1oo1SGuEs47gbU"
#     RANGE = "Sheet1!A2:E"
#     SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
#
#     watcher = GoogleSheetWatcher(SPREADSHEET_ID, RANGE, SCOPES)
#
#     watcher.delete_row_by_reg_id("21BCE7170")


