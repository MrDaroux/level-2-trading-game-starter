#  Student starting file. The demonstration below is supplied code.
#
#  Replace the demonstration using your own component plan. You choose your
#  functions, collections, schema, SQL and other files. This callback is only
#  where the supplied browser shell passes input to your solution.


def handle_action(action, fields, database):
    #  Receive a button name, raw text fields and an open SQLite connection.

    #  Return the text to display. Do not use input(): it would wait in the
    #  server terminal, not the browser. Your code checks all game inputs,
    #  carries out game/database operations and decides what text to return.
    
    return ("No game code is connected yet.\n\n"
            f"Button: {action}\n"
            f"Market entered: {fields['market']}\n"
            f"Good entered: {fields['good']}\n"
            f"Quantity entered: {fields['quantity']}\n\n"
            "This only demonstrates the controls. No trade has occurred.")
