from faker import Faker
from model import Contact, ContactBook
import random

source = "phone_book.json"
def generate_users(source, count):
    seed = 1234
    fake = Faker()
    fake.seed_instance(seed)
    random.seed(seed)

    repo = ContactBook(source)
    for _ in range(count):
        pattern = random.choice(['#' * 11,'%#####'])
        plus = random.choice(['+',''])
        contact = Contact(first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          company=fake.company(),
                          work=fake.numerify(text=pattern),
                          mobile=plus + fake.numerify(text='#' * 11))
        repo.add_contact(contact)
        repo.save()

if __name__ == '__main__':
    generate_users(source, 100)