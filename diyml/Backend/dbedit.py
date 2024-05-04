import sqlite3
import os

def main():
    DB = 'ml.db'
    db_path = os.path.join(os.path.dirname(__file__), DB)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Select the table you want to access:")
    print("1. Users")
    print("2. Projects")
    print("3. Images")
    print("4. Labels")
    print("5. Image_Labels")
    print("6. Training")
    print("7. Models")
    print("8. Inferences")
    print("9. Tests")
    print("10. Reports")
    table_choice = input("Enter your choice: ")

    if table_choice == '1':
        table_name = 'Users'
        fields = ['username', 'password_hash', 'email', 'is_active', 'created_at', 'last_login']
    elif table_choice == '2':
        table_name = 'Projects'
        fields = ['user_id', 'name', 'type', 'created_at', 'updated_at']
    elif table_choice == '3':
        table_name = 'Images'
        fields = ['project_id', 'file_path', 'uploaded_at']
    elif table_choice == '4':
        table_name = 'Labels'
        fields = ['project_id', 'name']
    elif table_choice == '5':
        table_name = 'Image_Labels'
        fields = ['image_id', 'label_id']
    elif table_choice == '6':
        table_name = 'Training'
        fields = ['project_id', 'start_time', 'end_time', 'status']
    elif table_choice == '7':
        table_name = 'Models'
        fields = ['session_id', 'model_file_path', 'created_at']
    elif table_choice == '8':
        table_name = 'Inferences'
        fields = ['model_id', 'image_id', 'status', 'result', 'inferred_at']
    elif table_choice == '9':
        table_name = 'Tests'
        fields = ['model_id','status', 'test_results', 'tested_at']
    elif table_choice == '10':
        table_name = 'Reports'
        fields = ['session_id', 'report_content', 'created_at']
    else:
        clear_database(db_path)
        return

    print(f"Selected table: {table_name}")
    print("Choose action:")
    print("1. Add")
    print("2. Delete")
    action_choice = input("Enter your choice (1/2): ")

    if action_choice == '1':
        add_record(cursor, table_name, fields)
    elif action_choice == '2':
        delete_record(cursor, table_name)
    else:
        print("Invalid choice.")
        return

    conn.commit()
    conn.close()

def add_record(cursor, table_name, fields):
    values = []
    for field in fields:
        value = input(f"Enter {field}: ")
        values.append(value)
    placeholders = ', '.join(['?' for _ in fields])
    cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})", values)
    print("Record added successfully.")

def delete_record(cursor, table_name):
    record_id = input(f"Enter ID of the record to delete from {table_name}: ")
    cursor.execute(f"DELETE FROM {table_name} WHERE {table_name[:-1]}_id = ?", (record_id,))
    print("Record deleted successfully.")

def clear_database(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iterate over the tables, clear them, and reset their auto-increment values
    for table in tables:
        table_name = table[0]
        
        # Skip the special sqlite_sequence table
        if table_name == 'sqlite_sequence':
            continue
        
        # Delete all records from the table
        cursor.execute(f"DELETE FROM {table_name};")
        
        # Reset the auto-increment value by deleting the sequence entry
        cursor.execute("DELETE FROM sqlite_sequence WHERE name=?;", (table_name,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
