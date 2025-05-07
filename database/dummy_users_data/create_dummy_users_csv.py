import csv
import uuid
import random
import string
def generate_dummy_user(index):
    user_id = str(uuid.uuid4())
    username = f'user{index}'
    email = f'user{index}@example.com'
    password_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # simple dummy hash
    return [user_id, username, email, password_hash]

def create_dummy_users_csv(filename='users.csv', N=10):
    header = ['user_id', 'username', 'email', 'password_hash']
    rows = [generate_dummy_user(i) for i in range(1, N + 1)]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"{N} dummy users written to {filename}")
create_dummy_users_csv(N=10000)