class AUTH:
    def __init__(self):
        with open('./auth/password.txt', 'r') as f:
            self.password = f.read()
        with open('./auth/users.txt', 'r') as f:
            self.users = f.readlines()
            self.users = [line.strip() for line in self.users]

    def is_user_auth(self, chat_id : int) -> bool:
        if str(chat_id) in self.users:
            return True
        return False
    
    def auth_user(self, chat_id : int, password : str) -> list:
        if str(chat_id) in self.users:
            return 1, f'USER {chat_id} ALREADY AUTH'
        if str(chat_id) not in self.users and password == self.password:
            with open('./auth/users.txt', 'a') as f:
                f.write(str(chat_id) +'\n')
            return 1, f'USER {chat_id} AUTHED SUCCESFULLY!'
        if str(chat_id) not in self.users and password != self.password:
            return 0, f'⛔ WRONG PASSWORD BRO! ask @uomo_succo ❌'