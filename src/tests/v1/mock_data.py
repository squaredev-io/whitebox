register_payload = dict(
    username="mark",
    first_name="Mark",
    last_name="Knight",
    email="mark@knight.com",
    password="pass",
    is_business=False,
)
login_payload = dict(username="mark@knight.com", password="pass")
client_update_payload = dict(
    username="markus",
    password="pass1",
    email="mark@knight1.com",
    first_name="Markus",
    last_name="Knight the 2nd",
)

app_create_payload = dict(name="App 1")
app_update_payload = dict(name="App 1.1")

user_create_payload = dict(name="User", ext_id="123")
user_update_payload = dict(name="Userius", ext_id="1234")