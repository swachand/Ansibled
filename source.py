import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup

final_playbook = '---' + '\n' + '- name: Ansible Playbook' + '\n  hosts: '
hosts = input("Please enter the host string or IP: ")
final_playbook += hosts + '\n' + '  become: yes' + '\n' + '  become_user: root' + '\n\n' + '  tasks:\n'
user_input = input("Please enter the search keyword:")
conn = sqlite3.connect("D:\\A\\ansiblator.db")
res = conn.execute("SELECT name,description FROM MODULES WHERE name like ?", ('%'+user_input+'%',)).fetchall()
result = list()
for i in res:
    result.append(i)

for j in range(1, len(result)):
    print(str(j) + '. ' + result[j-1][0] + ' - ' + result[j-1][1])


def excepting():
    row_num = int(input("\nPlease select a module number from above: Ex: 12 :"))
    try:
        print('\nYou have chosen the Ansible Module "' + str(result[-1][0]) + '"')
        print("Description:", result[row_num-1][1])
        return result[row_num-1][0]
    except IndexError:
        print("\nError - Please enter number within the available limit!!! \n")
        excepting()
x = excepting()

# Listing the Parameters
def get_attributes(x):
    global final_playbook
    conn = sqlite3.connect("D:\\A\\ansiblator.db")
    res = conn.execute("SELECT name,parameter,description,req_flag FROM metadata WHERE name = ?", (x,)
                    ).fetchall()
    meta = list()
    for i in res:
        meta.append(i)
    print(meta)
    final_playbook += '  - name: ' + x + '\n'
    for value in meta:
        final_playbook += '    ' + value[1] + ':'
        if value[3] == 'Yes':
            final_playbook += '  #ToDo * Required Field \n'
        else:
            final_playbook += '  #ToDo \n'
    final_playbook += '\n'
get_attributes(x)

decision = input("Do you want to continue: [Y/N]")
while decision == 'Y':
    x = excepting()
    get_attributes(x)
    decision = input("Do you want to continue: [Y/N]")

final_playbook += '\n...'
print(final_playbook + '\n...')
with open(os.getcwd()+"\\A\\playbook.yml", "w") as file:
    file.write(final_playbook)
