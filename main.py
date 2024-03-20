# importo il file system dal rispettivo file
from file_system import FileSystem

# definisco la funzione principale.
def main():
    fs = FileSystem()

    while True:
        choice = input(">: ").split(" ")
        choice[0] = choice[0].lower()
        if choice[0] == "login" and len(choice) == 2:
            username = choice[1]
            fs.LOG_IN(username)
            while True:
                sub_choice = input(">: ").split(" ")
                sub_choice[0] = sub_choice[0].lower()

                if sub_choice[0] == "touch" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    data = None
                    fs.CREATE_FILE(file_name, data)
                elif sub_choice[0] == "mkdir" and len(sub_choice) == 2:
                    dir_name = sub_choice[1]
                    fs.CREATE_DIRECTORY(dir_name, username)
                elif sub_choice[0] == "open" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    fs.OPEN_FILE(file_name, username)
                elif sub_choice[0] == "wq" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    fs.CLOSE_FILE(file_name, username)
                elif sub_choice[0] == "cd" and len(sub_choice) == 2:
                    dir_name = sub_choice[1]
                    fs.CHANGE_DIRECTORY(dir_name, username)
                elif sub_choice[0] == "mv" and len(sub_choice) == 3:
                    current_name = sub_choice[1]
                    new_name = sub_choice[2]
                    fs.RENAME_ENTRY(current_name, new_name, username)
                elif sub_choice[0] == "vi" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    data = input("Enter data to write: ")
                    fs.WRITE_FILE(file_name, data, username)
                elif sub_choice[0] == "cat" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    print(fs.READ_FILE(file_name))
                elif sub_choice[0] == "rm" and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    fs.DELETE_FILE(file_name)
                elif sub_choice[0] == "rmdir" and len(sub_choice) == 2:
                    dir_name = sub_choice[1]
                    fs.DELETE_DIRECTORY(dir_name, username)
                elif sub_choice[0] == 'mvfile' and len(sub_choice) == 2:
                    file_name = sub_choice[1]
                    target_dir = sub_choice[2]
                    fs.MOVE_FILE(file_name, username)
                elif sub_choice[0] == 'mvdir' and len(sub_choice) == 3:
                    dir_name = sub_choice[1]
                    target_dir = sub_choice[2]
                    fs.MOVE_DIRECTORY(dir_name, target_dir, username)
                elif sub_choice[0] == "ls" and len(sub_choice) == 1:
                    fs.READ_DIRECTORY()
                elif sub_choice[0] == "pwd" and len(sub_choice) == 1:
                    fs.GET_PATHNAME()
                elif sub_choice[0] == "logout" and len(sub_choice) == 1:
                    fs.LOG_OUT(username)
                    break
                elif sub_choice[0] == 'format' and len(sub_choice) == 1:
                    fs.FORMAT()
                elif sub_choice[0] == 'help':
                    print("touch : Use this command to create a file and its content in the curret directory")
                    print("mkdir : Use this command to create a directory either in your current path")
                    print("open : Use this command to open a file")
                    print("wq : Use this command to close a file")
                    print("cd : Use this command to navigate through the files and directories")
                    print("mv : Use this command to rename entry. First enter old name and then write new name -> eg. mv old_name new_name")
                    print("mvfile : Use this command to move a file from the current folder to another folder -> eg. mvfile file_name target_dir")
                    print("mvdir : Use this command to move a sub-directory from the current folder to another folder -> eg. mvdir directoryvi _name target_dir")
                    print("vi : Use this command to write text into an OPENED file. You can't write text to a file without opening it before")
                    print("cat : Use this command to read an OPENED file. You can't read a file without opening it before")
                    print("rm : Use this command to delete files within a directory")
                    print("rmdir : Use this command to permanently delete an empty directory")
                    print("ls : Use this command to list files and subdirectories within a directory")
                    print("pwd : Use this command to find the path of your current working directory.")
                    print("logout : Use this command to log out, all the directories and files wil be closed and you'll need to log again")
                    print("format : Use this command to format the whole file system. All files and directories wille be deleted")
                else:
                    print('please enter a valid command, type "help" to see the list of commands')
        elif choice[0] == 'quit' and len(choice)==1:
            break
        else:
            print('Please either log in or quit.')
            print('You have currently the following commands:') 
            print('login : to log in write "login" and then provide your username')
            print('Usernames are composed by a single word -> e.g. login John')
            print('quit : you quit the file system')                  

main()
                     
###############################################

# linee di codice extra scartate

#def main():
#    fs = FileSystem()
#    #file_name = input()
#    #dir_name = input()
#    #current_name = input()
#    #new_name = input()
#
#    while True:
#        #print("Welcome to the TXT file system")
#        #print("1. Login")
#        #print("2. Quit")
#        choice = input(">: ").split(" ")
#        choice[0] = choice[0].lower()
#        if choice[0] == "login" and len(choice) == 2:
#            #username = input("Enter your username: ")
#            username = choice[1]
#            fs.LOG_IN(username)