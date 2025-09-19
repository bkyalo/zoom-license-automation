import mysql.connector
from mysql.connector import Error
from collections import defaultdict
from config import Config

def get_email_schedule():
    """
    Connects to the database, fetches user emails mapped to days,
    and returns them as a dictionary.
    """
    # Use defaultdict to easily append to lists
    schedule = defaultdict(list)
    connection = None  # Initialize connection to None
    
    # The SQL query joins the tables to get unique user emails by day for academic session 2
    sql_query = """
    SELECT DISTINCT
        d.id AS day_id,
        d.name AS day_name,
        u.email AS user_email
    FROM 
        course_unit_programme_mappings AS m
    JOIN 
        users AS u ON m.user_id = u.id
    JOIN 
        days AS d ON m.day_id = d.id
    WHERE 
        m.academic_session_id = 2
    ORDER BY
        d.id, u.email;  -- Order by day and then email for consistent output
    """

    try:
        # Establish the database connection using Config
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to the database.")
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute(sql_query)
            
            # Fetch all rows from the query result
            rows = cursor.fetchall()
            
            # Process the rows into the schedule dictionary
            if not rows:
                print("⚠️ No mappings found in the database.")
                return None

            for row in rows:
                day_id, day_name, user_email = row
                schedule[day_name].append(user_email)
            
            return schedule

    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None
        
    finally:
        # Ensure the connection is closed
        if connection and connection.is_connected():
            connection.close()
            print("✅ Database connection closed.")


def print_schedule(schedule):
    """Formats and prints the schedule to the console."""
    if not schedule:
        print("\nNo schedule to display.")
        return

    print("\n--- User Email Schedule ---")
    for day, emails in schedule.items():
        print(f"\n🗓️ {day.upper()}")
        print("-" * (len(day) + 3))
        for email in emails:
            print(f"  - {email}")
    print("\n---------------------------\n")


if __name__ == "__main__":
    # 1. Fetch the data from the database
    email_schedule = get_email_schedule()
    
    # 2. Print the formatted schedule
    if email_schedule:
        print_schedule(email_schedule)