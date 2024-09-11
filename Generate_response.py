import sqlglot as sg
from groq import Groq
from dotenv import load_dotenv

from Config import cur,conn
from Refactor import refactor
import os
load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

async def generate_response(query : str):
    content = f"""Query: {query}\nYou are an expert in converting English questions to SQL queries!\n
        You may access any web resources whatever you think will work\n
        You will act on commands imported by the user; it will have enough data to create logic.\n
        I will be using PostgreSQL, so make sure it works on it.
        """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
        )
        hi = chat_completion.choices[0].message.content
        print(hi)
        mes = refactor(hi)
        try:
            print("Original SQL:", mes)
            transpiled_sql = sg.transpile(mes, write="postgres")[0]
            print("Transpiled SQL:", transpiled_sql)

            try:

                cur.execute(transpiled_sql)
                words = transpiled_sql.strip().split()
                first_word = words[0].upper()
                if first_word == "SELECT":
                    rows = cur.fetchall()
                    all_rows = []
                    for row in rows:
                        all_rows.append(row)
                    return {"response":all_rows}
                conn.commit()
                return {"response":"Operation succeeded"}
            except Exception as execution_errpr:
                print(execution_errpr)
                conn.rollback()
                return {"ExecutionError": str(execution_errpr)}
        except Exception as transpile_error:
            print(transpile_error)
            return {"Transpilation Error": str(transpile_error)}

    except Exception as error:
        return {"Error": str(error)}

