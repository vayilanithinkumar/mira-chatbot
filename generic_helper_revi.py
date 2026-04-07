import re

def extract_session_id(session_str: str):
    match =  re.search(f'sessions/(.*?)/contexts,', session_str)
    if match:
        extracted_string = match.group[1]
        return extracted_string
    return ""

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f'{int(value)} {key}' for key, value in food_dict.items()])




def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        cursor.commit()

        cursor.close()

        return 1
    except mysql.connector.Error as err:
        print(f'Error inserting order item: {err}')

        cnx.rollback()

    except Exception as e:
        print(f'Error found in: {e}')
        cnx.rollback()

