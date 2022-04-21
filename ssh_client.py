from paramiko import SSHClient, AutoAddPolicy
from rich import print, pretty, inspect
pretty.install()

client = SSHClient()
# Can Use Keys
# client.load_host_keys('/home/rohan/.ssh')
# client.load_system_host_keys()

client.set_missing_host_key_policy(AutoAddPolicy())

# client.connect('127.0.0.1',username = 'rohan')
# Or can use password
client.connect('127.0.0.1',username = 'rohan',password='Rohan@13')
#inspect(client, methods=True)

# Executing command on remote host and acquiring output
stdin, stdout, stderr = client.exec_command('hostname')
print('STDOUT STATUS:',stdout.channel.recv_exit_status())# 0 for Success
print('STDOUT:',stdout.read().decode('utf8').strip())
print('STDERR:',stderr.read().decode('utf8').strip())

stdin.close()
stdout.close()
stderr.close()


stdin, stdout, stderr = client.exec_command('cat ')
# Giving in stdin
stdin.write('Rasengan\n')
stdin.channel.shutdown_write()

print('STDOUT:',stdout.read().decode('utf8'))
print('STDERR:',stderr.read().decode('utf8'))

stdin.close()
stdout.close()
stderr.close()

client.close()
