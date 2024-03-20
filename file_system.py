# File System
# Obiettivo: creare un basilare filesystem virtuale che implementi le seguenti funzionalità: 
# LOG_IN, per permettere ad un utente di entrare nel file system e di essere riconosciuto in maniera univoca. 
# CREATE_FILE, per permettere ad un utente di creare un nuovo file nella cartella corrente. 
# CREATE_DIRECTORY, per permettere ad un utente di creare una nuova cartella nella cartella corrente. 
# OPEN_FILE, per permettere ad un utente di aprire un file nella cartella corrente. 
# CLOSE_FILE, per permettere ad un utente di chiudere un file nella cartella corrente. 
# CHANGE_DIRECTORY, per permettere ad un utente di navigare fra le cartelle, un livello alla volta. Se in nome inserito inizia con “..” la cartella padre diventerà la cartella corrente. 
# RENAME_ENTRY, per permettere ad un utente di rinominare una cartella/file nella cartella corrente. 
# WRITE_FILE, per permettere ad un utente di scrivere dati su un file aperto. 
# READ_FILE, per permettere ad un utente di leggere i dati da un file aperto. 
# DELETE_FILE, per permettere ad un utente di eliminare un file nella cartella corrente. 
# DELETE_DIRECTORY, per permettere ad un utente di eliminare una cartella nella cartella corrente. 
# LOG_OUT, per permettere ad un utente nel file system di uscirne, chiudendo tutti i file da esso aperti. 
# READ_DIRECTORY, per permettere ad un utente di visualizzare la lista di file/cartelle presenti nella cartella corrente. 
# GET_PATHNAME, per permettere ad un utente di visualizzare il percorso della cartella corrente. 
# FORMAT, per eliminare tutti i file e le cartelle presenti nel file system. 
# 
# Come funzionalità aggiuntiva, è inoltre possibile implementare le seguenti funzionalità: 
# MOVE_FILE, per permettere di spostare un file dalla cartella corrente di un utente alla cartella corrente di un altro utente. 
# MOVE_DIRECTORY, per permettere di spostare una cartella (e il suo contenuto) dalla cartella corrente di un utente alla cartella corrente di un altro utente. 
# N.B. entrambi gli utenti visualizzano lo stesso file system. 

import os

class FileSystem:
    # classe dell'intero file system
    def __init__(self):
        # definisco la root delle directory
        self.root = Directory("/root")
        # ogni volta che il file system parte la directory corrente è la root
        self.current_directory = self.root
        # dizionario dei file a cui si ha accesso e si ha aperto (per lettura, modifiche, rimoozione ecc)
        self.open_files = {}
        # dizionario degli utenti
        self.users = {}
        # dizionario dell'ultima directory
        self.last_directory = {}

    # funzione per loggarti
    #def LOG_IN(self, user):
    #    if user not in self.users:
    #        user = User(user)
    #    self.current_directory = self.root
    #    user.current_directory = self.current_directory
    #    print(f"User {user.name} logged in successfully.")

    def LOG_IN(self, user):
        self.users[user] = self.root
        print(f"User {user} logged in successfully.")

        # funzione per fare il logout. vengono eliminati i file aperti dell'utente 
    def LOG_OUT(self, user):
        #self.last_directory[directory] = user.current_directory
        if user in self.users:
            del self.users[user]
            if user in self.open_files:
                del self.open_files[user]
            print(f"User {user} logged out.")
        else:
            print(f"User {user} is not logged in.")

    # funzione per creare un file: il file viene caricato e inserito nella directory corrente
    def CREATE_FILE(self, name, content=None):
        if "/" in name:
            print('Invalid character!')
        else:
            if name in self.current_directory.files:
                    print("File already exists")
            else:
                file = File(name, content) # il file richiama la classe definita all'inizio
                self.current_directory.files[name] = file
                print(f"File {name} created in {self.current_directory}.")
                print(type(file))

    # funzione per creare una directory all'interno della root o nella cartella corrente
    def CREATE_DIRECTORY(self, name, user):
        if "/" in name:
            print('Invalid character!')
        else:
            if name in self.current_directory.directories:
                    print("Directory already exists")
            else:
                directory = Directory(name, self.current_directory)
                self.current_directory.directories[name] = directory
                print(f"Directory {name} created in {self.current_directory}.")
                print(type(directory))

    # funzione per aprire un file (si può aprire un file solo se l'utente ha avuto accesso)
    def OPEN_FILE(self, name, user):
        file = self.current_directory.files.get(name)
        if isinstance(file, File):
            self.open_files[user] = file
            print(f"File {file.name} opened.")
        else:
            print("not a file.")

    # stessa cosa di prima ma per chiudere il file
    def CLOSE_FILE(self,name, user):
        file = self.current_directory.files.get(name)
        if isinstance(file, File):
            del self.open_files[user]
            print(f"File {file.name} closed.")
        else:
            print("No file is open.")

    # funzione per cambiare la directory corrente.
    def CHANGE_DIRECTORY(self, name, user):
        # se indico solo '..' ritorna alla cartella parent
        if name == '..':
            if self.current_directory != self.root: 
                directory = self.current_directory.parent
                self.current_directory = directory
                self.users[user] = self.current_directory
                print(f"Current directory changed to {self.current_directory}.")
        # se indico SOLO il nome della sotto-cartella, mi sposto nella sotto-cartella figli di quella corrente (se non esiste mi da errore)
        elif '/' not in name:
            directory = self.current_directory.directories.get(name)
            if isinstance(directory, Directory):
                self.current_directory = directory
                self.users[user] = self.current_directory
                print(f"Current directory changed to {self.current_directory}.")
            else:
                print(f"{name} is not a directory.")
        # se indico il percorso verso la cartella (e quindi iniziando con "/", e.g /root/a/b/c/d...) mi porta direttamente al cartella di cui indico il path
        elif '/' in name:
            # prendo il path e lo splitto tramite / 
            directory_path = name.split("/")
            # se mi voglio spostare alla root (cioé scrivo /root), il processo si stoppa automaticamente alla root
            i = 1
            if directory_path[i] == "root": #and len(directory_path) == 2
                # impongo come directory iniziale la root
                self.current_directory = self.root
                self.users[user] = self.current_directory
                i += 1
                print(f"Current directory changed to {self.current_directory}.")
            # altimenti mi percorre tutte le cartelle partendo dalla root per arrivare alla cartella selezionate
            if len(directory_path) > 2:
                # impongo come directory iniziale la root
                #self.current_directory = self.root
                for stringa in directory_path[i:]:
                    print(stringa)
                    
                    temp = self.current_directory.directories.get(stringa)
                    is_dir = isinstance(temp, Directory)

                    # -- METODO ALTERNATIVO --
                    #if stringa in self.current_directory.directories.keys():
                    #    self.current_directory = self.current_directory.directories[stringa]

                    if is_dir == True:
                        self.current_directory = temp
                        #self.users[user] = self.current_directory
                        looped = True
                    else:
                        looped = False
                        break
                    i += 1
                if looped == True:
                    self.users[user] = self.current_directory
                    print(f"Current directory changed to {self.current_directory}.")
                else:
                    print('Invalid path in loop!')
            #else:
            #    print('Invalid declared path!')

            # per ogni children nella path mi seleziono il children nella lista di stringhe del path 



    # funzione per rinominare i nomi dei file all'interno delle directory. Se la entry che difinisco è contenuta nella directory corrente, possono definire un nuvo nome da attribuirgli
    # se la entry non si trova nella directory corrente, mi da errore
    def RENAME_ENTRY(self, old_name, new_name):
        if old_name in self.current_directory.files:
            if new_name in self.current_directory.files:
                print("Entry already has this name")
            else:
                self.current_directory.files[new_name] = self.current_directory.files.pop(old_name)
                print("Entry renamed")
        elif old_name in self.current_directory.directories:
            if new_name in self.current_directory.directories:
                print("Entry already has this name")
            else:
                self.current_directory.directories[new_name] = self.current_directory.directories.pop(old_name)
                print("Entry renamed")
        else:
            print("Entry does not exist")

    # funzione per scrivere all'interno di un file e quindi modificare il loro contenuto
    def WRITE_FILE(self, name, content, user):
        file = self.current_directory.files.get(name)
        if isinstance(file, File):
            file.content = content
            self.open_files[user] = file
            print(f"Content written to {file.name}.")
        else:
            print("No file is open.")

    # funzione per leggere il file. Viene printato sia nome che contenuto del file
    def READ_FILE(self, name):
        file = self.current_directory.files.get(name)
        if isinstance(file, File):
            print(f"Content of {file.name}: {file.content}")
        else:
            print("No file is open.")

    # funzione per eliniare i file. se il nome del "child" della directory che seleziono corrisponde ad un file, la funzione lo elimina, altrimenti mi da errore
    def DELETE_FILE(self, name):
        file = self.current_directory.files.get(name)
        if isinstance(file, File):
            del self.current_directory.files[name]
            print(f"File {name} deleted.")
        else:
            print(f"{name} is not a file.")

    # funzione per eliminare la directory. Il procedimento è lo stesso per l'eliminazione dei file, ma il nome del child questa volta corrisponde ad una directory
    def DELETE_DIRECTORY(self, name, user):
        directory = self.current_directory.directories.get(name)
        if isinstance(directory, Directory):
            del self.current_directory.directories[name]
            print(f"Directory {name} deleted.")
        else:
            print(f"{name} is not a directory.")

    # funzione per mostrare tutti i file all'interno della dirctory corrente
    def READ_DIRECTORY(self):
        print("Contents of current directory:")
        for item in self.current_directory.files.keys():
            print(f'file {item}')
        for item in self.current_directory.directories.keys():        
            print(f'dir {item}')

    # funzione per ottenere il percorso alla dirctory corrente
    def GET_PATHNAME(self):
        return print(self.current_directory.get_path())
    
    # funzione per formattare il file system. Tutte le liste e dizionari diventano vuoti 
    def FORMAT(self):
        self.root = Directory("root")
        self.current_directory = self.root
        self.open_files = {}
        self.users = {}
        print("File system formatted.")

    def MOVE_FILE(self, file_name, directory_name, user):
        # se il file da spostare o la target directory non sono nella root e o in ciascuna subdirectory, viene riportato errore
        if file_name not in self.current_directory.files:
            print("File does not exist")
            return
        if directory_name not in self.root.find_directory():
            print("Directory does not exist")
            return
        directory = self.root.find_directory(directory_name)
        if isinstance (directory, Directory):
            if file_name in directory.files:
                print("File already exists in directory")
                return
            file = self.current_directory.files.pop(file_name)
            directory.files[file_name] = file
            print(f'{file_name} moved to {directory_name}')

    # funzione per muovere una directory dalla director corrente ad una target.  
    def MOVE_DIRECTORY(self, dir_name, target_dir, user):
        # se la directory corrente è la root, non si può spostare
        if dir_name == "root":
            print("Cannot move root directory")
            return
        # se la cartella da spostare o la target directory non sono nella root e o in ciascuna subdirectory, viene riportato errore
        if dir_name not in self.root.find_directory():
            print("Directory does not exist")
            return
        if target_dir not in self.root.find_directory():
            print("Target directory does not exist")
            return 
        directory = self.root.find_directory(dir_name)
        target_directory = self.root.find_directory(target_dir)
        if target_directory == directory or directory == target_directory.parent:
            print("Directory already in target directory")
            return
        if dir_name == target_dir or directory.is_ancestor_of(target_directory):
            print("Invalid move operation")
            return
        # elimino la subdirectory da spostare dalla directory originale e la creo nela directory target
        directory.parent.directories.pop(directory)
        target_directory.directories[directory.name] = directory
        print(f'{dir_name} moved to {target_dir}')

    #def move_file(self, name, directory_name):
    #    if name not in self.current_directory.files:
    #        print("File does not exist")
    #        return
    #    if directory_name not in self.current_directory.directories:
    #        print("Directory does not exist")
    #        return
    #    self.current_directory.files[name].directory = self.current_directory.directories[directory_name]
    #    self.current_directory.directories[directory_name].files[name] = self.current_directory.files.pop(name)
#
    #def move_directory(self, name, directory_name):
    #    if name not in self.current_directory.directories:
    #        print("Directory does not exist")
    #        return
    #    if directory_name not in self.current_directory.directories:
    #        print("Directory does not exist")
    #        return
    #    self.current_directory.directories[name].directory = self.current_directory.directories[directory_name]
    #    self.current_directory.directories[directory_name].directories[name] = self.current_directory.directories.pop(name)

class File:
    # creo la classe dei file: creo la funzione per definire i file, i quali contengono nome e contenuto 
    def __init__(self, name, content=None):
        self.name = name
        self.content = content
    # il metodo str richiama solo il nome del file
    def __str__(self):
        return self.name


class Directory:
    # faccio lo stesso per la classe delle directory: ogni directory ha nome, 'parent' (se è una sub-directory)
    # 'files' e 'directories' (se si trovano delle sub-diectories o singoli file nella directory corrente) sono dizionari in cui vengono i inseriti gli elementi corrispondenti
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = {}
        self.directories = {}

    # per ottenere il percorso verso una cartella creo un funzione iterativa. 
    # Finché la parent della cartella in cui ci troviamo è None (ovvero quando ci troviamo nella root), 
    # la funzione si ripete e ottiene i nomi di tutte le cartelle parent fino alla root, divise da "/"
    def get_path(self):
        if self.parent is None:
            return self.name
        else:
            return self.parent.get_path() + '/' + self.name


    # questa funzione riporta i nomi di tutte le subirectory nella directory corrente. 
    # la funzione è iterativa e per ogni subdirectory cerca i nomi delle ulteriori sub-subdirectory (etc) all'interno di ciascuna subdirectory 
    #def walk_directories(self):
    #    yield self.name
    #    for directory in self.directories.values():
    #        yield from directory.walk_directories()

    # questa funzione permette di selezionare una cartella specifica all'interno della current directory
    def find_directory(self, name):
        if self is None:
            self = self.current_directory
        if self.name == name:
            return self
        for d in self.directories.keys():
            result = d.find_directory(name)
            if result is not None:
                return result
        return 

    # questa funzione permette di selezionare la parent directory della directory corrente.
    def is_ancestor_of(self, directory):
        parent = directory.parent
        while parent is not None:
            if parent == self:
                return True
            parent = parent.parent
        return False

    def __str__(self):
        return self.name


class User:
    def __init__(self, name):
        self.name = name
        self.current_directory = None



############################################

# FUNZIONE SCARTATA PER FIND_DIRECTORY

#def find_directory(self, directory_name):
#        if directory_name == "/":
#            return self.root
#
#        if directory_name.startswith("/"):
#            current = self.root
#            directory_name = directory_name[1:]
#        else:
#            current = self.current_directory
#
#        for name in directory_name.split("/"):
#            if name == "":
#                continue
#            found = False
#            for child in current.children:
#                if isinstance(child, Directory) and child.name == name:
#                    current = child
#                    found = True
#                    break
#            if not found:
#                raise FileNotFoundError(f"Directory '{directory_name}' not found")
#        return current


# FUNZIONI EXTRA SCARTATE PER LA CLASSE DIRECTORY
    
    #def add_file(self, name):
    #    self.files[name] = File(name)

    #def add_directory(self, name):
    #    self.directories[name] = Directory(name, parent=self)
    #    #directory.parent = self

# FUNZIONI SCARTATE PER READ_DIRECTORY

#    def READ_DIRECTORY(self):
#        print("Contents of current directory:")
#        #files = list(self.current_directory.files.keys())
#        #directories = list(self.current_directory.directories.keys())
#        #return files + directories
#        for item in self.current_directory.files.values():
#            #if isinstance (item, File):
#            print(f'file {item}')
#        for item in self.current_directory.directories.values():        
#            #if isinstance (item, Directory):
#            print(f'dir {item}')
#        #if not self.logged_in_user:
#        #    print("Not logged in")
#        #    return
