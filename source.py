import sys
import sqlite3
import os

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
    print(str(j) + '. ' + result[j][0] + ' - ' + result[j][1])


def excepting():
    row_num = int(input("\nPlease select a module number from above: Ex: 12 :"))
    try:
        print('\nYou have chosen the Ansible Module "' + str(result[row_num][0]) + '"')
        print("Description:", result[row_num][1])
    except IndexError:
        print("\nError - Please enter number within the available limit!!! \n")
        excepting()
excepting()
with open(os.getcwd()+"\\A\\playbook.yml", "w") as file:
    file.write(final_playbook)
print(final_playbook + '\n...')
