# 🌟 Real Time Synchronisation of Google Sheet and MYSQL 🌟

## 📚 Approach to the Problem: Real-Time Synchronization between Google Sheets and MySQL Database

The **Superjoin Hiring Assignment** project involves developing a solution that synchronizes data between a Google Sheet and a MySQL database in real-time. This two-way synchronization ensures that changes made in either system are reflected in the other seamlessly.

---

## 🔑 Key Components

### 1. GoogleSheetWatcher: The Client for Google Sheets
The `GoogleSheetWatcher` class serves as the interface with the Google Sheets API, performing the following key operations:

- **Authentication**: This class authenticates the application using Google OAuth 2.0, allowing secure access to the specified Google Sheet. The authentication is handled using a token stored in `token.json`, which is refreshed when expired, ensuring the connection remains valid. 🔐

- **Data Fetching**: The `get_sheet_data()` method retrieves data from the Google Sheet based on the specified range (e.g., `Sheet1!A2:E`). 📝

- **Detecting New Rows**: The `detect_new_rows()` method compares the current number of rows with the previously stored row count (`prev_data`). If the row count increases, it identifies and returns the newly added rows. 📈

- **Appending Data**: When new rows are inserted into the MySQL database, the `append_data()` method ensures that the same data is appended to the Google Sheet, keeping it updated in real-time. ⏱️

- **Deleting Rows**: The `delete_row_by_reg_id()` method locates and deletes a row in the Google Sheet based on a specific `regID`, ensuring that records removed from the MySQL database are also deleted from the Google Sheet. ❌

---

### 2. Database: The Consumer for MySQL
The `Database` class interacts with the MySQL database and ensures data synchronization with the Google Sheet. Key functions include:

- **Connecting to the Database**: The `connect()` method establishes a connection with the MySQL database using MySQL's connector module. This ensures that any operations (insert, delete, fetch) are executed within an active connection. 🔗

- **Inserting New Rows**: When new data is detected in the Google Sheet, the `insert_row()` method inserts that data into the MySQL `user_records` table. Each insertion updates the `last_inserted_time` field, ensuring subsequent synchronizations are based on the latest data. ✍️

- **Fetching Data**: The `fetch_rows_after_last_inserted()` method retrieves rows from the MySQL database that were inserted after the last synchronization. These rows are then appended to the Google Sheet for consistency. 🔄

- **Detecting Deleted Rows**: The method compares the data in the MySQL database and the Google Sheet, identifying rows that exist in one system but not the other. If rows are deleted in the Google Sheet, they are also deleted in the MySQL database via the `delete_row_in_mysql()` method. 🗑️

---

### 3. Synchronization Process
The synchronization occurs in real-time through the following steps:

- **Detect New Rows in Google Sheets**: The `watch_to_sheet()` function constantly monitors the Google Sheet. If new rows are detected, they are inserted into the MySQL database via the `insert_row()` method. 🔍

- **Sync Deleted Rows from Google Sheets to MySQL**: If rows are deleted in the Google Sheet, the `watch_to_sheet()` function identifies these rows, and the corresponding entries are deleted from the MySQL database using `delete_row_in_mysql()`. ⚠️

- **Sync New Rows from MySQL to Google Sheets**: If new rows are added to the MySQL database, they are fetched and appended to the Google Sheet using the `append_data()` method in `GoogleSheetWatcher`. ⬆️

- **Sync Deleted Rows from MySQL to Google Sheets**: If rows are deleted from the MySQL database, the `watch_to_sheet()` function ensures that these rows are also deleted from the Google Sheet using the `delete_row_by_reg_id()` method. 🔄

---

### 4. Optimizing the Solution
The real-time synchronization is achieved efficiently by minimizing unnecessary data retrieval and write operations. Key optimizations include:

- **Polling Intervals**: The script uses a `while True` loop with a `time.sleep(3)` delay to check data every 3 seconds. This provides near real-time synchronization while preventing excessive API calls to Google Sheets or database queries. ⏲️

- **Selective Fetching**: Instead of fetching the entire dataset repeatedly, the solution fetches only the newly inserted rows using timestamps (from the `inserted_at` column). This ensures faster processing and minimizes resource consumption. 📊

- **Batch Operations**: The Google Sheets API supports batch updates (e.g., `batchUpdate()` for row deletion), allowing multiple changes to be applied in a single API call, reducing network overhead. 🌐

---

### 5. How the Client and Consumer Work Together
- **Client (Google Sheets)**: The `GoogleSheetWatcher` serves as the client, constantly monitoring changes in Google Sheets and ensuring that new or deleted records are synchronized with the MySQL database. 

- **Consumer (MySQL)**: The `Database` class serves as the consumer, ensuring that the latest data is always available and synchronized with Google Sheets. The consumer maintains data integrity, performing insertions, deletions, and updates in a timely manner. 📅

By working together, these two components ensure that the data remains consistent across both systems. The real-time synchronization guarantees that users can make changes in either the Google Sheet or the MySQL database, with confidence that these changes will be reflected almost immediately in both systems. 

---

## 📌 Summary
This approach to solving the problem of real-time synchronization leverages efficient data polling, selective fetching, and minimal API usage to provide a scalable, optimized solution. 🌍

---
### 📹 Demonstration Video

The working of the project is showcased in the video. Watch the full [demonstration video](https://drive.google.com/file/d/1VNkigoYlyIYzopo5STuFVe8yVjVM0AMK/view?usp=sharing).
---

Thank you! 👩‍💻👨‍💻
