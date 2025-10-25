from .db import get_connection

def create_record(location, start_date, end_date, weather_json):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather_records (location, start_date, end_date, weather_json) VALUES (?, ?, ?, ?)",
        (location, start_date, end_date, weather_json)
    )
    conn.commit()
    conn.close()

def read_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_records ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_record(record_id, location=None, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    # simple update logic
    cursor.execute("""
        UPDATE weather_records
        SET location = COALESCE(?, location),
            start_date = COALESCE(?, start_date),
            end_date = COALESCE(?, end_date)
        WHERE id = ?
    """, (location, start_date, end_date, record_id))
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
