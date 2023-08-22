from model import Contact

def get_contact_info_from_user(editing=False, search=False):
    """
    Dialog for getting contact parameters from console on different mode.
    
    Keyword arguments:
    - editing -- True if get info for editing contact
    - search --  True if get info for search criteria
    """
    if not editing:
        print("Press Enter to skip")
    else:
        print("Press Enter to save old value\n" \
              +"Enter Space for an empty value\n")
    contact = { }
    contact['first_name'] = str(input("Enter first name: "))
    contact['last_name'] = str(input("Enter last name: "))
    contact['patronymic'] = str(input("Enter patronymic: "))
    contact['company'] = str(input("Enter company name: "))

    work_num = str(input("Enter work number: "))
    mobile_num = str(input("Enter mobile number: "))
    
    if not search:
        contact['work'] = set_valid_number(work_num, editing)
        contact['mobile'] = set_valid_number(mobile_num, editing, mobile=True)
    else:
        contact['work'], contact['mobile'] = work_num, mobile_num
    return contact


def set_valid_number(number, editing, mobile = False):
    """
    Dialog for getting only valid phone number from console.
    
    Keyword arguments:
    - editing -- True if get info for editing contact
    - mobile --  True if get mobile number (must contain 11 digits)
    """
    work_ex = ['443322','89008007070', '+59008007070']
    mobile_ex = ', '.join(work_ex[1:3])

    while not Contact.validate_number(number, mobile) and not (number == ' ' and editing):
        number = str(input("Enter number \n" \
                         + f"ex. {mobile_ex if mobile else ', '.join(work_ex)} \n" \
                         + "or press Enter to skip: "))
    return number


def confirm():
    """
    Dialog for confirmation.
    """
    confirm = input("Enter [yes] to confirm \n:")
    return confirm == 'yes'


if __name__ == '__main__':
    pass 