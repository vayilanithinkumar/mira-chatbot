from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

onprogress_orders = {}

@app.post('/')
async def handle_request(request: Request):

    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper_revi.extract_session_id(output_contexts[0]['name'])


    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }
    return intent_handler_dict[intent](parameters)



def remove_from_order(parameters: dict, session_id: str):
    if session_id not in onprogress_orders:
        return JSONResponse(content={
            'fulfillment_text': 'I am having a trouble'
        })

    current_order = onprogress_orders[session_id]
    food_items = parameters['food-item']

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

   if len(removed_items) > 0:
       fulfillment_text = f'removed {",".join(removed_items)} from your order'

   if len(no_such_items)  > 0:
       fulfillment_text = f'Removed {",".join(no_such_items)} from your order'

   if len(current_order.keys()) == 0:
       fulfillment_text += 'your order is empty'
   else:
       order_str = db_helper_revi.get_str_from_food_dict(current_order)
       fulfillment_text += f'Here is left in your order:{order_str}'

   return JSONResponse(content={
       'fulfillment_text': fulfillment_text
   })


def add_to_order(parameters: dict):
    food_items = parameters['food-item']
    quantities = parameters['number']

    if len(food_items) != len(quantities):
        fulfillment_text = f'Sorry i dont understand'
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in onprogress_orders:
            current_food_dict = onprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            onprogress_orders[session_id] = current_food_dict
        else:
            onprogress_orders[session_id] = new_food_dict

        order_str = generic_helper_revi.get_set_from_food_dict(onrogress_orders[session_id])
        fulfillment_text = f'so far you have {order_str}'
    return JSONResponse(content={
        'fulfillmentText': fulfillment_text
    })



def complete_order(parameters: dict, session_id: str):
    if session_id not in onprogress_orders:
        fulfillment_text = 'I am troubling please specify the food items'
    else:
        order = onprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "sorry, i couldn't process this order"
        else:
            order_total = db_helper_revi.get_total_order_price(order_id)
            fulfillment_text= f'awesome we have placed your order for {order_total}'

        del onprogress_orders[order_id]
    return JSONResponse(content={
        'fulfillmentText': fulfillment_text
    })


def save_to_db(order: dict):

    next_order_id = db_helper_revi.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper_revi.insert_order_item(
            food_item,
            quantity,
            insert_order_id
        )
        if rcode == -1:
            return -1
    db_helper_revi.insert_order_tracking(next_order_id, "in progress")

    return nex_order_id




def  track_order(parameters: dict):
    order_id = int(parameters['order_id'])
    order_status = db_helper_revi.get_orde_status(order_id)

    if order_status:
        fulfillment_text = f'the status od the order id: {order_id} is: {order_status}'
    else:
        fulfillment_text = f"No order found with this order id: {order_id}"
    return JSONResponse(content={
        'fulfillmentText': fulfillment_text
    })