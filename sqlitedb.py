import sqlite3
import pandas as pd

class DDB:
    def __init__(self, db_name='eg.db'):
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()
        print(f"Connected to SQLite database: {db_name}")

    def get_all_tables(self):
        try:
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in self.cur.fetchall()]
            return tables
        except Exception as e:
            print(f"Error fetching tables: {e}")
            return []

    def get_table_columns(self, table_name):
        try:
            self.cur.execute(f"PRAGMA table_info(`{table_name}`)")
            columns_info = self.cur.fetchall()
            columns = []
            for col in columns_info:
                columns.append({
                    'name': col[1],
                    'type': col[2],
                    'nullable': 'YES' if col[3] == 0 else 'NO',
                    'key': 'PRI' if col[5] == 1 else '',
                    'default': col[4],
                    'extra': ''
                })
            return columns
        except Exception as e:
            print(f"Error fetching columns: {e}")
            return []

    def create_custom_table(self, table_name, columns_with_types):
        try:
            type_mapping = {
                'int': 'INTEGER',
                'varchar': 'TEXT',
                'text': 'TEXT',
                'float': 'REAL',
                'datetime': 'TEXT',
                'boolean': 'INTEGER'
            }
            
            column_defs = []
            for col_name, col_type in columns_with_types.items():
                sqlite_type = type_mapping.get(col_type.lower(), 'TEXT')
                column_defs.append(f"`{col_name}` {sqlite_type}")

            column_defs.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
            columns_str = ", ".join(column_defs)
            query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_str})"
            
            self.cur.execute(query)
            self.db.commit()
            print(f"Table '{table_name}' created successfully!")
            return True
            
        except Exception as e:
            print(f"Error creating table: {e}")
            return False

    def insert_into_custom_table(self, table_name, data):
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ", ".join(["?"] * len(values))
            columns_str = ", ".join([f"`{col}`" for col in columns])
            
            query = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
            
            self.cur.execute(query, values)
            self.db.commit()
            print(f"Data inserted into '{table_name}' successfully!")
            return True
            
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False

    def fetch_custom_table(self, table_name):
        try:
            query = f"SELECT * FROM `{table_name}`"
            self.cur.execute(query)
            data = self.cur.fetchall()
            
            self.cur.execute(f"PRAGMA table_info(`{table_name}`)")
            columns_info = self.cur.fetchall()
            columns = [col[1] for col in columns_info]
            
            df = pd.DataFrame(data, columns=columns)
            print(f"Data from '{table_name}':")
            print(df)
            return df
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def describe_custom_table(self, table_name):
        try:
            self.cur.execute(f"PRAGMA table_info(`{table_name}`)")
            data = self.cur.fetchall()
            df = pd.DataFrame(data, columns=['cid', 'Field', 'Type', 'NotNull', 'Default', 'PK'])
            print(f"Structure of '{table_name}':")
            print(df)
            return df
            
        except Exception as e:
            print(f"Error describing table: {e}")
            return None

    def delete_from_custom_table(self, table_name, id):
        try:
            query = f"DELETE FROM `{table_name}` WHERE id = ?"
            self.cur.execute(query, (id,))
            self.db.commit()
            print(f"Record deleted from '{table_name}' successfully!")
            return True
            
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False

    def update_record(self, table_name, record_id, data):
        try:
            set_clauses = []
            values = []
            for column, value in data.items():
                set_clauses.append(f"`{column}` = ?")
                values.append(value)
            
            values.append(record_id)
            
            query = f"UPDATE `{table_name}` SET {', '.join(set_clauses)} WHERE id = ?"
            
            self.cur.execute(query, values)
            self.db.commit()
            print(f"Record updated in '{table_name}' successfully!")
            return True
            
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def get_record_by_id(self, table_name, record_id):
        try:
            query = f"SELECT * FROM `{table_name}` WHERE id = ?"
            self.cur.execute(query, (record_id,))
            record = self.cur.fetchone()
            
            if record:
                columns = self.get_table_columns(table_name)
                column_names = [col['name'] for col in columns]
                return dict(zip(column_names, record))
            return None
            
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None

    def close(self):
        self.db.close()
        print("Database connection closed.")
