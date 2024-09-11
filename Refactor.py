import re


def refactor(message):
    sql_commands = {"SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"}

    words = message.strip().split()
    first_word = words[0].upper()
    if first_word in sql_commands:
        print("helkjnhbgvfcgyuijklmnbgvfcgyuijlknmbhvgfcuijk")
        return message


    match = re.search(r'(?<=```sql)(.*?)(?=```)', message, re.DOTALL)
    if match:
        code = match.group(1).strip()
        wrapped_code = f"""{code}"""
        return wrapped_code
    return None

