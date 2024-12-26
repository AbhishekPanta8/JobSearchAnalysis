import psycopg2

def save_to_database(table_name, data):
    conn = psycopg2.connect(
        host="localhost",
        database="job_insight_tool",
        user="username",
        password="password"
    )
    cursor = conn.cursor()

    for item in data:
        columns = ', '.join(item.keys())
        values = ', '.join([f"%({k})s" for k in item.keys()])
        sql = f"""
            INSERT INTO {table_name} ({columns}) 
            VALUES ({values}) 
            ON CONFLICT DO NOTHING;
        """
        cursor.execute(sql, item)

    conn.commit()
    cursor.close()
    conn.close()

def clean_text(text):
    return ' '.join(text.split())

if __name__ == "__main__":
    print("Utility module for scraping.")
