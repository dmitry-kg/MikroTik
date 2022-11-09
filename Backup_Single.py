from netmiko import ConnectHandler
from  datetime import datetime
class Routers:
    def __init__(self, host: str, port: str, username: str, password:str, command: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.command = command
    def mikrotik(self):
        someRouter = {
            'device_type': 'mikrotik_routeros',
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password
        }

        sshCli = ConnectHandler(**someRouter)
        output = sshCli.send_command(self.command,expect_string=r"\S+\s\>\s$")
        sshCli.disconnect()

        with open(f'{self.host}-{datetime.now().strftime("%Y-%m-%d")}.txt', "w+") as file:
            file.writelines(output)



if __name__ == "__main__":
    homeMikroTik = Routers('ip or host', '22', 'username', 'password', '/export')
    homeMikroTik.mikrotik()
