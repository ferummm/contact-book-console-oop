from dataclasses import dataclass, asdict, field
from typing import Optional, List, Self

import uuid
import json
import re
import os


@dataclass
class Contact():
    """Contact in phone book.

    Attributes:
    - _id -- uuid of contact as string
    - first_name, last_name, patronymic -- first name, last name, patronymic of contact
    - company -- name of organization to which contact belongs
    - work -- work number of contact
    - mobile -- mobile number of contact
    """
    _id: str = field(default="")

    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    patronymic: Optional[str] = ""

    company: Optional[str] = ""
    work: Optional[str] = ""
    mobile: Optional[str] = ""

    _card_form = "Contact card: {}\n" \
            + 'Full name: {}\n' \
            + 'Company: {}\n' \
            + 'Work: {}\n' \
            + 'Mobile: {}\n'
    
    def __post_init__(self) -> None:
        if not self._id:
            self._id = str(uuid.uuid4())

    def __str__(self) -> str:
        return self._card_form.format('', self.full_name(), self. company,\
                                      self.work, self.mobile)
    
    def __dict__(self) -> dict[str, str]:
        res = asdict(self)
        del res['_id']
        return res 

    def full_name(self) -> str:
        "Return full name (first name, last_name and patronymic) in a string"
        full_name = [self.first_name, self.last_name, self.patronymic]
        return ' '.join(full_name)
    
    @staticmethod
    def validate_number(number:str, mobile:bool=False) -> bool:
        """Return True if number is valid and False if not. 
        Key arguments:
        - number -- phone number as string
        - mobile -- if True valid number must contain 11 digits
        """
        pattern1 = r'^\+?[0-9]{11}$' 
        pattern2 = r'^[0-9]{6}$' 
        if number == '':
            return True
        if mobile:
            return re.match(pattern1, number)
        else:
            return re.match(pattern1, number) or re.match(pattern2, number)

    def card_with_num(self, index:int) -> str:
        """Return contact card with number of card

        Key arguments:
        - index -- number of card 
        """
        return self._card_form.format(index, self.full_name(), self. company,\
                                      self.work, self.mobile)

    def get_id(self) -> str:
        """Return _id of contact"""
        return self._id
    
    def set_id(self, id:str) -> Self:
        self._id = id
        return self

    
class ContactBook:
    """Phone book with info about contacts.

    Attributes:
    - source -- JSON file for storing contacts info
    - contacts -- dictionary with _id of contact as key and contact info as value
    """
    def __init__(self, source:str) -> None:
        if os.path.isfile(source):
            with open(source, 'r') as f:
                try:
                    self._contacts = json.load(f).get('contacts')
                    self.source = source
                except BaseException as e:
                    raise ValueError(f'The file contain invalid JSON. \n Details: {str(e)}')
        else:
            self._contacts = { }
            self.source = source
            with open(source, 'x+') as f:
                self.save()

    def __str__(self) -> str:
        if not self._contacts:
            return "Contact list is empty \n"
        
        res = self.get_contacts_list()
        return '\n'.join([x.card_with_num(i) for (i, x) in enumerate(res, 1)])
    
    def __dict__(self) -> dict:
            return {'source': self.source,
                    'contacts': self._contacts}
    
    def add_contact(self, cont: Contact) -> None:
        """Add contact to phone book without saving to source"""
        id = cont.get_id()
        self._contacts[id] = cont.__dict__()

    def save(self) -> None:
        """Save _contacts to source (JSON file)"""
        with open(self.source, 'w') as f:
                json.dump(self.__dict__(), f, indent=4, ensure_ascii=False)            

    def search(self, **kwargs) -> List[Contact]:
        """Return list of contacts by search criteria"""
        search_res = []
        for id, card in self._contacts.items():
            for attr, value in kwargs.items():
                if value.lower() not in card[attr].lower():
                    break
            else:
                search_res.append(Contact(**card).set_id(id))
        return search_res
    
    def get_contacts_list(self) -> List[Contact]:
        """Return list of contacts from contact book"""
        res = [Contact(**params).set_id(id) for id, params in self._contacts.items()]
        return res

    def find_by_id(self, id) -> dict[str, str]:
        """Return contact info by id"""
        return self._contacts[id]
    
    def edit_card_by_id(self, id, **kwargs) -> None:
        """Replace contact info with new one by id"""
        self._contacts[id] = kwargs

    def delete_card_by_id(self, id) -> None:
        """Delete contact from contact book by id without saving to sourse"""
        del self._contacts[id]
    
        
if __name__ == '__main__':
    repo = ContactBook("test_book.json")
    
    repo.add_contact(Contact(first_name="Marina", mobile="89112010202"))
    repo.add_contact(Contact(first_name="Mary", mobile="89108087123"))
    repo.save()
    print(repo)
    