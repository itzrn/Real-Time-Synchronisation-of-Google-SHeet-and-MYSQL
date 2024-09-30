from datetime import datetime
from mysql.connector import connect, Error


class Database:
    def __init__(self, host, user, password, database):
        self.last_inserted_time = None
        self.curr_inserted_time = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.check = True
        self.prev_num = -1

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database  # Added database connection
            )
            self.cursor = self.connection.cursor()
            # print("Database connection established.")

            # Now that connection is established, fetch the last inserted time
            self.curr_inserted_time = self.get_last_inserted_time()
            if self.check:
                self.check = False
                self.last_inserted_time = self.curr_inserted_time

            print(f"current -> {self.curr_inserted_time}")
            print(f"last -> {self.last_inserted_time}")
            # self.prev_num = self.count_rows()
            # if self.check < 2:
            #     self.last_inserted_time = self.get_last_inserted_time()+timedelta(milliseconds=1)
            #     self.check += 1
            # # else:
            # #     self.last_inserted_time = self.get_last_inserted_time()
        except Error as e:
            print(f"Error connecting to the database: {e}")

    def get_last_inserted_time(self):
        """Fetch the most recent 'inserted_at' timestamp, or return the current time if no records are found."""
        try:
            query = "SELECT inserted_at FROM user_records ORDER BY inserted_at DESC LIMIT 1;"
            self.cursor.execute(query)
            result = self.cursor.fetchone()  # Fetch the first (and only) row
            if result:
                return result[0]
            else:
                # If no records are found, return the current time
                # current_time = datetime.now()
                return None
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_rows_after_last_inserted(self):
        """Fetch all rows inserted after the last inserted timestamp."""
        try:
            if self.last_inserted_time is None:
                query = "SELECT regID, name, email, age, phone_number FROM user_records;"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                # print("No last inserted time found.")
                return rows

            query = "SELECT regID, name, email, age, phone_number FROM user_records WHERE inserted_at > %s;"
            self.cursor.execute(query, (self.last_inserted_time,))
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def execute_query(self, query):
        """Execute a given SQL query."""
        try:
            if self.cursor is None:
                raise Exception("Cursor is not initialized. Please connect first.")
            self.cursor.execute(query)
            return self.cursor.fetchall()  # Return the fetched results
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def insert_row(self, regID, name, email, age, phone_number=None):
        """Insert a new row into the user_records table."""
        try:
            if self.cursor is None:
                raise Exception("Cursor is not initialized. Please connect first.")

            insert_query = """
            INSERT INTO user_records (regID, name, email, age, phone_number)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (regID, name, email, age, phone_number))
            self.connection.commit()  # Commit the transaction
            self.last_inserted_time = self.get_last_inserted_time()
            message = "Row inserted successfully to MYSQL Database."

            # Calculate the width for the table boundary
            width = len(message) + 2

            # Print the top boundary
            print("+" + "-" * width + "+")

            # Print the message with boundaries
            print(f"| {message} |")

            # Print the bottom boundary
            print("+" + "-" * width + "+")
            self.prev_num = self.count_rows()

        except Error as e:
            print(f"Error inserting row: {e}")

    def close(self):
        """Close the database cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

    def fetch_and_print_table(self):
        """Fetch and print the contents of a table with boundaries."""
        try:
            query = "SELECT * FROM user_records"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            column_names = [i[0] for i in self.cursor.description]  # Fetch column names

            # Determine the width of each column
            column_widths = [max(len(str(item)) for item in [name] + [row[i] for row in rows]) for i, name in
                             enumerate(column_names)]

            # Print top border
            print("+" + "+".join("-" * (column_width + 2) for column_width in column_widths) + "+")

            # Print column names
            header = " | ".join(f"{name:<{column_widths[i]}}" for i, name in enumerate(column_names))
            print(f"| {header} |")

            # Print separator
            print("+" + "+".join("-" * (column_width + 2) for column_width in column_widths) + "+")

            # Print each row
            for row in rows:
                print("| " + " | ".join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row)) + " |")

            # Print bottom border
            print("+" + "+".join("-" * (column_width + 2) for column_width in column_widths) + "+")

        except Error as e:
            print(f"Error fetching data: {e}")

    def fetch_all_data(self):
        try:
            query = "SELECT regID FROM user_records"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")

    def delete_row_in_mysql(self, reg_id):
        """Delete a row from MySQL database based on regID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM user_records WHERE regID = %s"
            cursor.execute(query, (reg_id,))
            self.connection.commit()

            message = f"Deleted regID {reg_id} from MySQL database."

            # Calculate the width for the table boundary
            width = len(message) + 2

            # Print the top boundary
            print("+" + "-" * width + "+")

            # Print the message with boundaries
            print(f"| {message} |")

            # Print the bottom boundary
            print("+" + "-" * width + "+")
        except Error as e:
            print(f"Error deleting row in MySQL: {e}")

    def count_rows(self):
        try:
            query = "SELECT COUNT(*) FROM user_records;"
            self.cursor.execute(query)
            result = self.cursor.fetchone()  # Fetch the result
            return result[0]  # Return the count
        except Error as e:
            print(f"Error fetching row count: {e}")
            return None

# class Database:
#     def __init__(self, host, user, password):
#         self.host = host
#         self.user = user
#         self.password = password
#         self.connection = None
#         self.cursor = None
#
#     def query(self, i):
#         if i == 1:
#             return "SHOW DATABASES;"
#         elif i == 2:
#             return "USE SUPERJOIN;"
#         elif i == 3:
#             return "SELECT * FROM SUPERJOIN_TABLE;"
#
#     def connect(self):
#         """Establish a connection to the database."""
#         try:
#             self.connection = connect(
#                 host=self.host,
#                 user=self.user,
#                 password=self.password
#             )
#             self.cursor = self.connection.cursor()
#             print("Database connection established.")
#         except Error as e:
#             print(f"Error connecting to the database: {e}")
#
#     def execute_query(self, query_):
#         """Execute a given SQL query."""
#         try:
#             if self.cursor is None:
#                 raise Exception("Cursor is not initialized. Please connect first.")
#             self.cursor.execute(query_)
#             return self.cursor.fetchall()  # Return the fetched results
#         except Error as e:
#             print(f"Error executing query: {e}")
#             return None
#
#     def close(self):
#         """Close the database cursor and connection."""
#         if self.cursor:
#             self.cursor.close()
#         if self.connection:
#             self.connection.close()
#         # print("Database connection closed.")


# from mysql.connector import connect, Error
# from datetime import datetime

# Example usage
# if __name__ == '__main__':
#     db = Database(host="localhost", user="root", password="10702", database="superjoin")
#     db.connect()
#
#     print(db.count_rows())
