import sqlite3
import os
import json
import base64


class SalesDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        db_config_path = os.path.join(base_dir, "db_config.json")
        db_file_path = os.path.join(base_dir, "sales.db")

        with open(db_config_path, "r") as f:
            self.table_schemas = json.load(f)

        self.connection = sqlite3.connect(db_file_path)
        self.connection.row_factory = sqlite3.Row  # Enable dict-style rows
        self.cursor = self.connection.cursor()

        self.create_all_tables()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.connection.close()

    def create_all_tables(self):
        for table_name in self.table_schemas:
            self.create_table(table_name)

    def create_table(self, table_name):
        if table_name in self.table_schemas:
            create_table_string = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ("
                + ", ".join(self.table_schemas[table_name])
                + ");"
            )
            try:
                self.cursor.execute(create_table_string)
            except Exception as e:
                print("Exception:", e)

    def add_record(self, table_name, info):
        table_cols = [col.split()[0] for col in self.table_schemas[table_name]][1:]

        insert_string = f"INSERT INTO {table_name} ({', '.join(table_cols)}) VALUES ({', '.join(['?' for _ in table_cols])})"

        vals = []
        for col in table_cols:
            val = info.get(col)

            if col == "photo" and isinstance(val, str):
                try:
                    with open(val, "rb") as img_file:
                        val = img_file.read()
                except FileNotFoundError:
                    val = None

            vals.append(val)

        self.cursor.execute(insert_string, vals)
        self.connection.commit()

    def update_records(self, table_name, match_vals, updated_vals):
        set_parts = []
        set_vals = []
        for col, val in updated_vals.items():
            set_parts.append(f"{col} = ?")
            set_vals.append(val)

        where_parts = []
        where_vals = []
        for col, op, val in match_vals:
            where_parts.append(f"{col} {op} ?")
            where_vals.append(val)

        update_query = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {' AND '.join(where_parts)}"
        self.cursor.execute(update_query, set_vals + where_vals)
        self.connection.commit()

    def get_records(self, table_name, match_vals=None):
        table_cols = [col.split()[0] for col in self.table_schemas[table_name]]
        select_string = f"SELECT {', '.join(table_cols)} FROM {table_name}"

        where_parts = []
        params = []
        if match_vals:
            for col, op, val in match_vals:
                where_parts.append(f"{col} {op} ?")
                params.append(val)

        if where_parts:
            select_string += " WHERE " + " AND ".join(where_parts)

        self.cursor.execute(select_string, params)

        data = []
        for row in self.cursor.fetchall():
            data.append({k: v for k, v in zip(table_cols, row)})

        return data

    def delete_records(self, table_name, match_vals):
        where_parts = []
        params = []
        for col, op, val in match_vals:
            where_parts.append(f"{col} {op} ?")
            params.append(val)

        delete_query = f"DELETE FROM {table_name} WHERE {' AND '.join(where_parts)}"
        self.cursor.execute(delete_query, params)
        self.connection.commit()

    def get_user_profile(self, phone: str):
        self.cursor.execute("SELECT name, phone, photo FROM users WHERE phone=?", (phone,))
        row = self.cursor.fetchone()
        if row:
            name, phone, photo = row["name"], row["phone"], row["photo"]
            photo_base64 = base64.b64encode(photo).decode("utf-8") if photo else None
            return {"name": name, "phone": phone, "photo": photo_base64}
        return None

    def update_user_profile(self, phone: str, update_data: dict):
        fields = []
        values = []
        for key, value in update_data.items():
            if key == "photo" and value is not None:
                fields.append("photo=?")
                values.append(value)
            elif value is not None:
                fields.append(f"{key}=?")
                values.append(value)
        if not fields:
            return
        values.append(phone)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE phone=?"
        self.cursor.execute(sql, tuple(values))
        self.connection.commit()


# Quick test if needed
if __name__ == "__main__":
    with SalesDB() as sales_db:
        records = sales_db.get_records("users")
        print(records)
