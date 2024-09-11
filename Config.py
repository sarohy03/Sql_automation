from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="hannan",
        user="postgres",
        password="mamdoot222"
    )
    cur = conn.cursor()
except Exception as e:
    print(f"Database connection error: {e}")
    exit()