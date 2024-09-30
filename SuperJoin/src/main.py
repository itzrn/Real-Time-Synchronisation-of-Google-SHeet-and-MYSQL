import time
from database import Database
from googlesheetwatcher import GoogleSheetWatcher


def watch_to_sheet():
    """Start watching the Google Sheet for new rows."""
    db = Database(host="localhost", user="root", password="10702", database="superjoin")
    db.connect()
    db.prev_num = db.count_rows()
    SPREADSHEET_ID = "1qWL1lnqYe-KTP9vfdLKbnQkEaWcCi1oo1SGuEs47gbU"
    RANGE = "Sheet1!A2:E"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    watcher = GoogleSheetWatcher(SPREADSHEET_ID, RANGE, SCOPES)

    # new_row_data = ["21BCE1234", "John Doe", "john.doe@example.com", 22, "1234567890"]
    # watcher.append_data(new_row_data)
    while True:
        cur_data = watcher.get_sheet_data()
        # print(cur_data)
        # print(len(cur_data))
        if cur_data:
            new_rows = watcher.detect_new_rows(current_data=cur_data)
            if new_rows and len(new_rows[len(new_rows) - 1]) == 5:
                print(new_rows)
                watcher.prev_data = len(cur_data)
                for r in new_rows:
                    db.insert_row(r[0], r[1], r[2], r[3], r[4])
                # watcher.pre_data = cur_data

        if watcher.prev_data > len(cur_data):
            watcher.prev_data = len(cur_data)
            # mysql_reg_ids = db.fetch_all_data()
            mysql_reg_ids = [item[0] for item in db.fetch_all_data()]
            # sheet_reg_ids = watcher.get_sheet_data()
            sheet_reg_ids = [item[0] for item in watcher.get_sheet_data()]
            reg_ids_to_delete = set(mysql_reg_ids) - set(sheet_reg_ids)
            # print(reg_ids_to_delete)
            for id_ in reg_ids_to_delete:
                db.delete_row_in_mysql(id_)
            # watcher.pre_data = cur_data

        # updated_rows = watcher.detect_updated_rows()
        # for r in updated_rows:
        #     print(r)

        if (db.curr_inserted_time is not None and db.last_inserted_time is not None and db.curr_inserted_time >
                db.last_inserted_time) or db.curr_inserted_time is not None and db.last_inserted_time is None:
            data_from_sql = db.fetch_rows_after_last_inserted()
            db.last_inserted_time = db.curr_inserted_time
            for data in data_from_sql:
                watcher.append_data(data)
                watcher.prev_data += 1
            db.prev_num = db.count_rows()

        if db.prev_num > db.count_rows():
            db.prev_num = db.count_rows()
            mysql_reg_ids = [item[0] for item in db.fetch_all_data()]
            sheet_reg_ids = [item[0] for item in watcher.get_sheet_data()]
            reg_ids_to_delete = set(sheet_reg_ids) - set(mysql_reg_ids)

            for id_ in reg_ids_to_delete:
                # print(id_)
                watcher.delete_row_by_reg_id(id_)

        time.sleep(3)
        db.connect()


if __name__ == '__main__':
    watch_to_sheet()

# https://developers.google.com/sheets/api/quickstart/python
