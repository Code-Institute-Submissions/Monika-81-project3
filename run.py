import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('buy_me')

def view_shopping_list():
    """
    Lets the user choose if they what to see both shopping
    lists as one or one separate list, either standard list or
    the list for extra supplies. A complete list contains values 
    from both lists but only one heading.
    """
    
    while True:
        print('Welcome to your personal shopping list!\n')
        print('Would you like to see a complete list?')
        print('Or your editable shopping list?')
        print('Choose between: Complete, Standard or Extra.\n')
        list_choice = input('Please choose a list: \n').lower()
        
        if list_choice == 'standard':
            print('You chose the standard shopping list.\n')
            shop_list = SHEET.worksheet('standard').get_all_values()
            pprint(shop_list)
            break

        elif list_choice == 'extra':
            print('You chose the extra shopping list.\n')
            shop_list = SHEET.worksheet('extra').get_all_values()
            pprint(shop_list)
            break

        elif list_choice == 'complete':
            print('\nYou chose the complete shopping list.')
            print('At the moment this list is view only.')
            print('Choose another list if you like to edit the list.\n')
            standard_list = SHEET.worksheet('standard').get_all_values()
            extra_list = SHEET.worksheet('extra').get_all_values()

            headings = [standard_list[0]]
            standard_list_values = standard_list[1:]
            extra_list_values = extra_list[1:]

            shop_list = headings + standard_list_values + extra_list_values  ##add sort on location
            pprint(shop_list)
            print('\nThis list is view ONLY.\n')
                       
        else:
            print("Incorrect list choice. Please try again!\n")
        

    return shop_list


def edit_list():
    """
    Lets the user choose if they like to edit the list.
    """
    print('\nWould you like to edit the list?\n')
    edit = input('Y/N?\n').lower()

    if edit == 'y':
        pass

    elif edit == 'n':
        print('Going back to the main menu.\n')
        main()
    else:
        print('Wrong input, please try again.\n')  


def edit_menu():
    """
    Displays a menu to let the user choose how to edit the list.
    """    
    print('\nChoose an edit action:\n')
    print('     1. Check item')
    print('     2. Change quantity')
    print('     3. Change location')
    print('     4. Add an item')
    print('     5. Delete item\n')

    while True:
        edit_action = input('Action number:')
        if validate_action(edit_action):
            break
        
    return edit_action


def validate_action(value):
    """
    Validates item index of chosen item as an integer.
    Or informs the user to input a number.
    """
    menu_range = range(1,6)
    try:
        value = int(value)
        if value in menu_range:
            print(f'You chose action no. {value}')

    except ValueError:
        print(f'You need to choose a number between 1 - 5, you chose {value}. Please try again!\n')
        return False

    return True


def item_to_edit():
    """
    Lets the user choose which item on the list to edit.
    """
    while True:
        print('Choose the number of the item you like to edit.\n')
        item_index = input('Item number:')
            
        if validate_int(item_index):
            break

        else:
            print('Wrong input, please try again.\n')   
    
    return item_index
        

def validate_int(value):
    """
    Validates item index of chosen item as an integer.
    Or informs the user to input a number.
    """
    try:
        value = int(value)  ##add validation of column length in list, and max int lenght after list lenght
    except ValueError:
        print(f'Invalid data: {value} is not a whole number (no decimals). Please try again! \n')
        return False

    return True


def edit_action_event(edit_action_value, shopping_list):
    """
    Identifies the action the user like to proceed with.
    """
    if edit_action_value == '1':
        edit_item = item_to_edit()
        check_item_in_worksheet(edit_item, shopping_list)

    elif edit_action_value == '2':
        edit_item = item_to_edit()
        change_quantity(edit_item, shopping_list)

    # elif edit_action_value == '3':
    #     change_quantity(edit_item, shopping_list)

    elif edit_action_value == '4':
        add_item(shopping_list)

    # elif edit_action_value == '4':
    #     change_quantity(edit_item, shopping_list)
    
    else:
        print('Something went wrong, please restart the program.')


def check_item_in_worksheet(edit_item, shopping_list):
    """
    If the item the user chose to check is in the list,
    the function finds the item and changes the value in 
    google sheet to either yes or no (to buy or not to buy).
    """ 
    index_num = int(edit_item)
    
    if shopping_list == SHEET.worksheet('standard').get_all_values():
        standard = SHEET.worksheet('standard').col_values(1)
        standard_col = SHEET.worksheet('standard').col_values(3) 
        
        if edit_item in standard:
            update_value = standard_col[index_num]

            if update_value == 'yes':
                check_position = int(standard.index(edit_item))
                SHEET.worksheet('standard').update_cell(check_position + 1, 3, 'no')
                print(f"Item number {edit_item} has been set to No!")
            
            elif update_value == 'no':
                check_position = int(standard.index(edit_item))
                SHEET.worksheet('standard').update_cell(check_position + 1, 3, 'yes')
                print(f"Item number {edit_item} has been set to Yes!")
            
        else:
            print('Item value not in list, please pick another value.\n')

    elif shopping_list == SHEET.worksheet('extra').get_all_values():
        extra = SHEET.worksheet('extra').col_values(1)
        extra_col = SHEET.worksheet('extra').col_values(3) 
                
        if edit_item in extra:
            update_value = (extra_col[index_num])

            if update_value == 'yes':
                check_position = int(extra.index(edit_item))
                SHEET.worksheet('extra').update_cell(check_position + 1, 3, 'no')
                print(f"Item number {edit_item} has been set to No!")
            
            elif update_value == 'no':
                check_position = int(extra.index(edit_item))
                SHEET.worksheet('extra').update_cell(check_position + 1, 3, 'yes')
                print(f"Item number {edit_item} has been set to Yes!")

        else:
            print('Item value not in list, please pick another value.\n')

    else:
        print('Not possible to edit complete list atm')  ##complete list is merger of two lists


def change_quantity(edit_item, shopping_list): 
    """
    Changes the quantity of an item on the list.
    """  
    while True:
        quantity = input('Input new quantity value:\n')  
        if validate_int(quantity):
            break
        else:
            print('Please insert a whole numeric number.')
        
    if shopping_list == SHEET.worksheet('standard').get_all_values():
        standard = SHEET.worksheet('standard').col_values(1) 
        
        if edit_item in standard:

            position = int(standard.index(edit_item))
            SHEET.worksheet('standard').update_cell(position + 1, 4, quantity)
            print(f"The quantatity has been set to {quantity}.")
            
        else:
            print('Item value not in list, please pick another value.\n')

    elif shopping_list == SHEET.worksheet('extra').get_all_values():
        extra = SHEET.worksheet('extra').col_values(1)
                
        if edit_item in extra:
           
            position = int(extra.index(edit_item))
            SHEET.worksheet('extra').update_cell(position + 1, 4, quantity)
            print(f"The quantatity has been set to {quantity}.")

        else:
            print('Item value not in list, please pick another value.\n')

    else:
        print('Not possible to edit complete list atm')  ##complete list is merger of two lists

    
def add_item(shopping_list):
    """
    Adds an item row to chosen list.
    """
    while True:
        print('\nYou wish to add an item to the list.\n')
        item = input('Name of item:\n').capitalize()
        if item.isalpha():
            break
        else:
            print('Input needs to be alphabetic. Try again.\n')
    
    while True:
        quantity = input('Quantity: \n')
        try:
            quantity = int(quantity)
            if quantity in range(0,100):
                break
            else:
                print('Max quantity is 100. Please try again.\n')

        except ValueError:
            print(f'Invalid data: {quantity} is not a whole number (no decimals). Please try again!\n')

    while True:
        print('Location in store exampel: "Bakery", "Bevereges", "Bulk", "Dairy", "Deli",')
        print(' "Floral", "Household", "Meat", "Personal care" "Vegetables" \n')
        location = input('Location in store: \n').capitalize()

        if location.isalpha():
            break
        else:
            print('Input needs to be alphabetic. Try again.\n')

    print(f'Do you wish to add {item}, quantity of {quantity} at location {location} to the list?')

    add_acceptance = input('Y/N?:\n')
    if add_acceptance == 'y':
        if shopping_list == SHEET.worksheet('standard').get_all_values():
            standard = SHEET.worksheet('standard').col_values(1)
            
            new_index = (int(standard[-1]) + 1)
            add_row = [new_index] + [item] + ['yes'] + [quantity] + [location]
            SHEET.worksheet('standard').append_row(add_row)
            print('\nNew item added to list.')
        
        elif shopping_list == SHEET.worksheet('extra').get_all_values():
            extra = SHEET.worksheet('extra').col_values(1)

            new_index = (int(extra[-1]) + 1)
            add_row = [new_index] + [item] + ['yes'] + [quantity] + [location]
            SHEET.worksheet('extra').append_row(add_row)
            print('\nNew item added to list.')

        else:
            print('Not possible to edit complete list atm')    
 
    elif add_acceptance == 'n':
        print('Going back to add item.\n')
        add_item(shopping_list)

    else:
        print('Wrong input, please try again.\n')
        add_item(shopping_list)

# def validate_new_row():
#     """
#     Validates input supplied for the new item to add at list 
#     """
#     try:
#         if item == isalpha(item):
#             pass
#         else:




def main():
    """
    Run all program functions.
    """
    shopping_list = view_shopping_list()
    edit_list()
    edit_action_value = edit_menu()
    edit_action_event(edit_action_value, shopping_list)
    
main()