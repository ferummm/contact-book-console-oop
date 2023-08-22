from model import Contact, ContactBook
from typing import List, Callable
import dialog

def max_page(n:int, per:int) -> int:
    """
    Return the maximum number of pages \
        required to display n elements per page.
    """
    
    div, mod = divmod(n, per)
    return div if not mod else div + 1


def pagination(source:List[Contact], page:int = 1, per:int = 5) -> str:
    """
    Return sring with contacts cards from source.

    Keyword arguments:
    - source -- list of contacts for pagination(List[Contact])
    - page -- number of page (default 1)
    - per -- number of contacts per page (default 5)
    """

    last = page * per   
    first = last - per
    enum_slice = enumerate(source[first:last], first + 1)
    return '\n'.join([x.card_with_num(i) for (i, x) in enum_slice])


def output_with_pagination(contacts:List[Contact], page:int, per:int):
    """
    Print contacts cards with pagination.

    Keyword arguments:
    - contacts -- list of contacts for pagination(List[Contact])
    - page -- number of page (default 1)
    - per -- number of contacts per page (default 5)
    """
     
    print("\nContact List------------------------") 
    repo_len = len(contacts)
    print(f'Page {page}/{max_page(repo_len, per)}')
    print(pagination(contacts, page, per))

#----------------------------------------------------------------------------
 
def print_page(cmd: str, state: dict):
    """
    Display page according to state.

    Keyword arguments:
    - state -- dict with current state of application
    - cmd -- command for page navigation
    """
    if not state['contacts']:
        print("\nContact list is empty\n")
        state['page'] = 0
        state['browser'] = False
        return 
    
    state['browser'] = True
    if cmd == 'p' and state['page'] != 1:
        state['page'] -= 1
    elif cmd == 'n' and len(state['contacts']) > state['per'] * state['page']:
        state['page'] += 1
    output_with_pagination(state['contacts'], state['page'], state['per'])


def modification_action(repo:ContactBook, action_name:str, action:Callable, state:dict):
    """
    Dialog for modification action.

    Keyword arguments:
    - repo -- phone book
    - action_name -- name of modification action
    - action -- function that modifies repo
    - state -- dict with current state of application
    """
     
    print_page(cmd['current_page'], state)
               
    if state['page'] != 0:
        print(nav_menu)
        inp = input(f"Enter card number to {action_name} the contact\n" \
                    + "or press Enter to skip \n:")
        
        if inp in ('p', 'n', 'b', ''):
            print("You returned to browser mode\n")
            print_page(inp, state)

        else:
            try:
                num = int(inp)
                if (num - 1) < len(state['contacts']):
                    print(Contact.card_with_num(state['contacts'][num - 1], num))
                    if dialog.confirm():
                        action(repo, state['contacts'][num - 1].get_id()) 
                else:
                    print('!!!Wrong card number \n')
            except ValueError:
                print('!!!Wrong command \n')
    else:
        print(f"No contacts to {action_name}\n")

#---------------------------------------------------------------------------------------

def delete(repo:ContactBook, id:str):
    """
    Delete contact by id and save changes.

    Keyword arguments:
    - repo -- phone book
    - id -- uuid of contact
    """
    repo.delete_card_by_id(id)
    repo.save()
    print("Changes saved \n")


def edit(repo:ContactBook, id:str):
    """
    Dialog for editing contact by id and saving changes.

    Keyword arguments:
    - repo -- phone book
    - id -- uuid of contact
    """
    old_contact = repo.find_by_id(id)
    params = dialog.get_contact_info_from_user(editing=True)
    for attr, val in params.items():
        if val == '':
            params[attr] = old_contact[attr]
        if val == ' ':
            params[attr] = ''
    if any(params.values()):
        print("Save changes?")
        if dialog.confirm():
            repo.edit_card_by_id(id, **params)
            repo.save()
            print("Changes saved \n")
        else:
            print("No changes have been made\n")
    else:
        print("Contact must contain at least one filled field\n")
        
#---------------------------------------------------------------------------------------

def init_start_state(repo:ContactBook):
    """
    Return dict with start state of application where keys:
    - contacts -- list of contacts for pagination (from repo)
    - browser -- is application in browsing contacts mode (False)
    - page -- number of current page (1)
    - per -- number of contacts per page (4)

    Keyword arguments:
    - repo -- phone book
    """
    state = {'contacts': repo.get_contacts_list(),
             'browser': False,
             'page': 1,
             'per': 4}    
    
    return state

main_menu = "Action menu: \n" \
    + "q - quit \n" \
    + "l - contact list \n" \
    + "a - add new contact \n" \
    + "r - remove a contact \n" \
    + "e - edit a contact \n" \
    + "s - search \n"

nav_menu = "Navigation: \n" \
    + "b - back \n" \
    + "p - previous page \n" \
    + "n - next page \n" 

cmd = {'prev': 'p',
       'next': 'n',
       'current_page': ' '}

if __name__ == '__main__':
    repo_source = "phone_book.json"
    repo = ContactBook(repo_source)

    state = init_start_state(repo)

    print(main_menu)
    inp = str(input("Type command and press Enter \n:"))
    while True:
        match inp:
            case 'q': break

            case 'l':
                state = init_start_state(repo)
                print_page(cmd['current_page'], state)

            case 'a': 
                state = init_start_state(repo)
                print("\nNew contact:------------------------")
                params = dialog.get_contact_info_from_user()
                if any(params.values()):
                    new_contact = Contact(**params)
                    repo.add_contact(new_contact)
                    repo.save()
                    print("Contacts saved \n")
                else:
                    print("Contact must contain at least one filled field")

            case 'r': 
                print("\nRemove:-----------------------------")
                modification_action(repo=repo,
                        action_name=delete.__name__,
                        action=delete,
                        state=state)

            case 'e': 
                print("\nEdit:-------------------------------")
                modification_action(repo=repo,
                        action_name=edit.__name__,
                        action=edit,
                        state=state)

            case 's':
                state = init_start_state(repo)
                print("\nSearch:-----------------------------")
                params = dialog.get_contact_info_from_user(search=True)
                search_res = repo.search(**params)
                state['contacts'] = search_res
                print_page(cmd['current_page'], state)
            
            case 'b': 
                if state['browser']:
                    state = init_start_state(repo)
                else:
                    print('!!!Wrong command\n')            

            case 'p' | 'n':
                if not state['browser']:
                    print('!!!Wrong command\n')
                else:
                    print_page(inp, state)
                    
            case _:
                print('!!!Wrong command\n')
                
        if state['browser']:
            print(nav_menu)
        print(main_menu)
        inp = str(input("Type command and press Enter \n:"))
    