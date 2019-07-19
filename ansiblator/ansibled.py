import sys
import sqlite3
import os
import requests
import subprocess


class Ansibled:
    """

    """
    def __init__(self):
        """

        """
        self.generate()

    def get_vars_data(self):
        """

        :return:
        """
        var = dict()
        count = int(input("Please enter number of variable definitions [max 10]: "))
        if count > 10:
            self.get_vars_data()
        else:
            for i in range(count):
                var_name = input("Please enter the Variable Name: ")
                var_value = input("Please enter the value for '" + var_name + "': ")
                var[var_name] = var_value
        print(var)
        return var

    def create_roles(self):
        count = int(input("Please enter no. of. roles to be created: [Max 5]"))
        if count > 5:
            self.create_roles()
        else:

            for i in range(1, count + 1):
                name = input("Please enter the name of role {}: ".format(i))
                leaf = ['tasks', 'vars', 'files', 'handlers', 'meta', 'templates']
                try:

                    for j in leaf:
                        dir = '/etc/ansible/' + name + '/' + j
                        os.makedirs(dir)
                    for k in leaf:
                        if k == 'handlers' or k == 'tasks' or k == 'vars':
                            f = '/etc/ansible/' + name + '/' + k + '/main.yml'
                            open(f, 'w').close()
                        if k == 'templates':
                            f = '/etc/ansible/' + name + '/' + k + '/httpd.conf.j2'
                            open(f, 'w').close()
                except FileExistsError:
                    print("Cannot create the file / directory when that it already exists")



    def generate(self):
        """

        :return:
        """
        decide = input("Do you want to create a simple Playbook or Roles? [P/R]")
        if decide.lower() == 'r':
            self.create_roles()
        else:
            final_playbook = '---' + '\n' + '- name: Ansible Playbook' + '\n  hosts: '
            hosts = input("Please enter the host string or IP: ")
            vars_in = input("Do you want to define variables directly into Playbook ? [Y/N]:")
            if vars_in == 'Y' or vars_in == 'y':
                var = self.get_vars_data()

            final_playbook += hosts + '\n' + '  become: yes' + '\n' + '  become_user: root' + '\n\n' + '  vars:\n'
            # for key, values in var.items():
            #     final_playbook += '      ' + key + ': ' + values + '\n'
            final_playbook += '\n  tasks:\n'
            user_input = input("Please enter the search keyword for Module:")
            conn = sqlite3.connect("D:\\A\\ansiblator.db")
            res = conn.execute("SELECT name,description FROM MODULES WHERE name like ?",
                               ('%' + user_input + '%',)).fetchall()
            result = list()
            for i in res:
                result.append(i)

            for j in range(1, len(result)):
                print(str(j) + '. ' + result[j - 1][0] + ' - ' + result[j - 1][1])

            def excepting():
                row_num = int(input("\nPlease select a module number from above: Ex: 12 :"))
                try:
                    print('\nYou have chosen the Ansible Module "' + str(result[-1][0]) + '"')
                    print("Description:", result[row_num - 1][1])
                    return result[row_num - 1][0]
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
            while decision == 'Y' or decision == 'y':
                x = excepting()
                get_attributes(x)
                decision = input("Do you want to continue: [Y/N]")

            final_playbook += '\n...'
            print(final_playbook + '\n...')
            with open(os.getcwd() + "\\A\\playbook.yml", "w") as file:
                file.write(final_playbook)

