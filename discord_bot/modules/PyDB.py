"""# PyDB
# A Simple Database Module"""

__version__ = 2.0
__name__ = "pydb"

class pydb:
    """
    ## Example:
    ```py
    import PyDB
    db=PyDB.pydb("Filename")
    ```
    """
    def __init__(self, file:str):
        try:
            f=open(file+".pydb", "r", encoding="utf-8")
            f.close()
        except FileNotFoundError:
            f=open(file+".pydb", "w", encoding="utf-8")
            f.close()
        self.file=file+".pydb"
        self.data=self.fileToDICT()
    def __getattr__(self, name):
        if name in self.data:
            return self.getData(name)
        else:
            raise AttributeError(f"'pydb' object has no attribute '{name}'")
    def getData(self, key):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        print(db.getData("key1"))
        ```
        ### Output:
        ```
        hello
        ```
        """
        key=str(key)
        with open(self.file, 'r', encoding="utf-8") as f:
            l = f.readlines()
            for i in l:
                if i.find(":")==-1:
                    l.pop(l.index(i))
            il=[]
            for i in l:
                il.append(i.split(':')[0])
            if not key in il:
                return None
            else:
                for i in l:
                    a=i.split(':')
                    if a[0]==str(key):
                        if len(a) == 2:
                            if a[1]=="{True}\n":
                                return True
                            elif a[1]=="{False}\n":
                                return False
                            elif a[1]=="{None}\n":
                                return None
                            else:
                                return a[1].replace("\n", "").replace("\\n", "\n")
                        elif len(a)>2:
                            return ":".join(a[1:]).replace("\n", "")
    def keys(self):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        print(db.keys())
        ```
        ### Output:
        ```
        ('key1','key2')
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            keys=[]
            lines = f.readlines()
            for i in lines:
                keys.append(i.split(':')[0].replace("\n", "").replace("\\n", "\n"))
            return tuple(keys)
    def values(self):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        print(db.values())
        ```
        ### Output:
        ```
        ('hello','hallo')
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            keys=[]
            lines = f.readlines()
            for i in lines:
                if len(i.split(':')) < 3:
                    keys.append(i.split(':')[1].replace("\n", "").replace("\\n", "\n"))
                else:
                    keys.append(":".join(i.split(':')[1:]).replace("\n", "").replace("\\n", "\n"))
            return tuple(keys)
    def items(self):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        print(db.items())
        ```
        ### Output:
        ```
        (('key','hello'),('key2','hallo'))
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            items=[]
            lines = f.readlines()
            for i in lines:
                if len(i.split(':')) < 3:
                    items.append([i.split(':')[0].replace("\\n", "\n"), i.split(':')[1].replace("\n", "").replace("\\n", "\n")])
                else:
                    items.append([i.split(':')[0].replace("\\n", "\n"), ":".join(i.split(':')[1:]).replace("\n", "").replace("\\n", "\n")])
            return tuple(items)
    def addData(self, key, value):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.addData("key3", "holla")
        ```
        ### New file.db file:
        ```
        key1:hello
        key2:hallo
        key3:holla
        ```
        """
        key=str(key)
        with open(self.file, 'r+', encoding="utf-8") as f:
            valu=value
            if value==True:
                valu="{True}"
            if value==False:
                valu="{False}"
            if value==None:
                valu="{None}"
            else:
                valu=value.replace("\n","\\n")
            keys=[]
            lines = f.readlines()
            for i in lines:
                keys.append(i.split(':')[0])
            if not key in keys:
                if lines!=[]:
                    if lines[len(lines)-1].find('\n') == -1:
                        lines[len(lines)-1]=lines[len(lines)-1]+'\n'
                lines.append(str(key).replace("\n", "\\n").replace(":", "")+':'+str(valu).replace("\n", "\\n")+'\n')
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    def removeData(self, key):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        key3:holla
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.removeData("key3")
        ```
        ### New file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        key=str(key)
        with open(self.file, 'r+', encoding="utf-8") as f:
            lines = f.readlines()
            for i in lines:
                if i.split(':')[0]==str(key):
                    lines.remove(i)
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    def clear(self):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.clear()
        ```
        ### New file.db file:
        ```
        (Empty)
        ```
        """
        with open(self.file, 'w') as f:
            f.write('')
    def backUp(self, newfile:str):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.backUp("newFile")
        ```
        ### newFile.db file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            with open(newfile+".pydb", 'w') as f:
                f.writelines(lines)
    def setData(self, key, newValue):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.setData("key2", "holla")
        ```
        ### newFile.db file:
        ```
        key1:hello
        key2:holla
        ```
        """
        key=str(key)
        if newValue==True:
            valu="{True}"
        if newValue==False:
            valu="{False}"
        if newValue==None:
            valu="{None}"
        valu = str(newValue).replace("\n","\\n")
        with open(self.file, 'r+', encoding="utf-8") as f:
            lines = f.readlines()
            for i in lines:
                if i.split(':')[0]==str(key):
                    lines[lines.index(i)]=str(key).replace("\n", "").replace(":", "")+':'+valu+'\n'
                    f.seek(0)
                    with open(self.file, 'w') as fi:
                        fi.writelines(lines)
    def fileToDICT(self):
        """
        ## Example:
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.fileToDICT()
        ```
        ### Output:
        ```
        {'key1':'hello','key2','hallo'}
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            dictionary={}
            lines= f.readlines()
            for i in lines:
                if i.find(":")!=-1:
                    a=i.split(':')
                    if len(a)==2:
                        if a[1]=="{True}":
                            dictionary[a[0]]=True
                        if a[1]=="{False}":
                            dictionary[a[0]]=False
                        if a[1]=="{None}":
                            dictionary[a[0]]=None
                        dictionary[a[0]]=a[1].replace("\n", "")
                    if len(a)>2:
                        dictionary[a[0]]=":".join(a[1:]).replace("\n", "")
            return dictionary
    def dictToFILE(self, dictionary:dict):
        """
        ## Example:
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pydb("filename")
        db.dictToFILE({'key1':'hello','key2','hallo'})
        ```
        ### file.db file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        with open(self.file, 'w', encoding="utf-8") as f:
            lines=[]
            for k,v in dictionary.items():
                if v==True:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{True}"))
                if v==False:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{False}"))
                if v==None:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{None}"))
                lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),str(v).replace("\n","\\n")))
            f.writelines(lines)
    def control(self, key):
        """
        ### This Command Checks Whether There Is a Counterpart to the Key
        """
        key=str(key)
        with open(self.file, 'r', encoding="utf-8") as f:
            l= f.readlines()
            for i in l:
                if i.find(":")== -1:
                    l.pop(l.index(i))
            for i in l:
                if i.split(':')[0]==str(key):
                    return True
            return False

class pylist:
    """
    ## Example:
    ```py
    import PyDB
    db=PyDB.pylist("Filename")
    ```
    """
    def __init__(self, file:str):
        self.f=file+".pydb"
    def getData(self, index:int):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        print(db.getData(0))
        ```
        ### Output:
        ```
        hello
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:
            l=f.readlines()
            if len(l)-1 < index:
                return None
            else:
                if l[int(index)].replace("\n", "") == "{True}":
                    return True
                elif l[int(index)].replace("\n", "") == "{False}":
                    return False
                elif l[int(index)].replace("\n", "") == "{None}":
                    return None
                else:
                    return l[int(index)].replace("\n", "").replace("\\n", "\n")
    def listFile(self):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        print(db.listFile())
        ```
        ### Output:
        ```
        ['hello','hallo']
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:
            liste=f.readlines()
            op = []
            for i in liste:
                if i.replace("\n","")=="{True}":
                    op.append(True)
                    continue
                if i.replace("\n","")=="{False}":
                    op.append(False)
                    continue
                if i.replace("\n","")=="{None}":
                    op.append(None)
                    continue
                a=i.replace("\n","").replace("\\n", "\n")
                op.append(a)
            return op
    def listToFILE(self, lst):
        """
        ## Example:
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.listToFILE(['hello','hallo'])
        ```
        ### New db.list file:
        ```
        hello
        hallo
        ```
        """
        with open(self.f, 'w', encoding="utf-8") as f:
            liste= []
            for i in lst:
                if i==True:
                    liste.append("{True}\n")
                    continue
                if i==False:
                    liste.append("{False}\n")
                    continue
                if i==None:
                    liste.append("{None}\n")
                    continue
                liste.append(str(i).replace("\n","\\n")+"\n")
            f.writelines(liste)
    def addData(self, value):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.addData("holla")
        ```
        ### New db.list file:
        ```
        hello
        hallo
        holla
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:
            lines = f.readlines()
            if value==True:
                lines.append("{True}\n")
            if value==False:
                lines.append("{False}\n")
            if value==None:
                lines.append("{None}\n")
            else:
                lines.append(str(value).replace("\n","\\n")+"\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    def setData(self, index:int, value):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.setData(1, "holla")
        ```
        ### New db.list file:
        ```
        hello
        holla
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:
            lines = f.readlines()
            if value==True:
                lines[int(index)]="{True}\n"
            if value==False:
                lines[int(index)]="{False}\n"
            if value==None:
                lines[int(index)]="{None}\n"
            else:
                lines[int(index)]=str(value).replace("\n","\\n")+"\n"
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    def removeData(self, index:int):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.removeData(2)
        ```
        ### New db.list file:
        ```
        hello
        hallo
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:
            lines=f.readlines()
            lines.pop(int(index))
            f.seek(0)
            f.writelines(lines)
            f.truncate()
    def clear(self):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.clear()
        ```
        ### New db.list file:
        ```
        (Empty)
        ```
        """
        f= open(self.f, 'w', encoding="utf-8")
        f.write("")
        f.close()
    def backUp(self, newfile:str):
        """
        ## Example:
        ### file.db file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        db.backUp("newFile")
        ```
        ### newFile.db file:
        ```
        hello
        hallo
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            with open(newfile+".pydb", 'w') as f:
                f.writelines(lines)
    def lenFile(self):
        """
        ## Example:
        ### db.list file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```py
        import PyDB
        db=PyDB.pylist("filename")
        print(db.lenFile())
        ```
        ### Output:
        ```
        3
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:
            liste=f.readlines()
            op = []
            for i in liste:
                a=i.replace("\n","")
                op.append(a)
            return len(op)
    def index(self, value):
        if not value==True or not value==False or not value==None:
            if str(value) in self.listFile():
                return self.listFile().index(str(value))
            else:
                return -1
        else:
            if value in self.listFile():
                return self.listFile().index(value)
            else:
                return -1

class convert:
    def csv_to_pydb(csv_file, new_file_name):
        """
        ## Example:
        ### database.csv file content:
        ```csv
        keys,variables
        key1,var1
        key2,var2
        ```
        ### Python code:
        ```py
        import PyDB
        PyDB.convert.csv_to_pydb("database.csv", "database")
        ```
        ### Created database.pydb file content:
        ```
        key1:var1
        key2:var2
        ```
        """
        import csv
        result_dict = {}
        with open(csv_file, mode='r', encoding='utf-8') as file:
            line1=file.readline().replace("\n", "")
            file.seek(0)
            csv_reader = csv.DictReader(file)
            args=line1.split(",")
            key=args[0]
            var=args[1]
            for row in csv_reader:
                result_dict[row[key]] = row[var]
        with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:
            lines=[]
            for k,v in result_dict.items():
                if v==True:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{True}"))
                if v==False:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{False}"))
                if v==None:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{None}"))
                lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),str(v).replace("\n","\\n")))
            f.writelines(lines)
        return new_file_name+".pydb"

    def json_to_pydb(json_file, new_file_name):
        """
        # Examples:
        ## Dictionary
        ### database.json file content
        ```json
        {
        "key1": "var1",
        "key2": "var2"
        }
        ```
        ### Python code:
        ```py
        import PyDB
        PyDB.convert.json_to_pydb("database.json", "database")
        ```
        ### Created database.pydb file content:
        ```
        key1:var1
        key2:var2
        ```
        ## List
        ### database.json file content
        ```json
        [
        "var1",
        "var2"
        ]
        ```
        ### Python code:
        ```py
        import PyDB
        PyDB.convert.json_to_pydb("database.json", "database")
        ```
        ### Created database.pydb file content:
        ```
        var1
        var2
        ```
        """
        import json
        data=None
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if type(data)==dict:
            with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:
                lines=[]
                for k,v in data.items():
                    if v==True:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{True}"))
                    if v==False:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{False}"))
                    if v==None:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),"{None}"))
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""),str(v).replace("\n","\\n")))
                f.writelines(lines)
        elif type(data)==list:
            with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:
                liste= []
                for i in data:
                    if i==True:
                        liste.append("{True}\n")
                        continue
                    if i==False:
                        liste.append("{False}\n")
                        continue
                    if i==None:
                        liste.append("{None}\n")
                        continue
                    liste.append(str(i).replace("\n","\\n")+"\n")
                f.writelines(liste)
        return new_file_name+".pydb"

def dictToTABLE(dictionary):
    """
    ## Example:
    ```py
    import PyDB
    print(PyDB.dictToTABLE({"apple": "den", "armuts": "den2", 1: 2}))
    ```
    ## Output:
    ```
    +--------+-------+
    | Key    | Value |
    +--------+-------+
    | apple  | den   |
    +--------+-------+
    | armuts | den2  |
    +--------+-------+
    | 1      | 2     |
    +--------+-------+
    ```
    """
    if dictionary=={}:
        return ""
    dictin={"Key":"Value"}
    for k,v in dictionary.items():
        dictin[k]=v
    max_key_len = max(len(str(k)) for k in dictin.keys())
    max_val_len = max(len(str(v)) for v in dictin.values())
    ll = "+" + "-" * (max_key_len + 2) + "+" + "-" * (max_val_len + 2) + "+\n"
    table = ll
    for k, v in dictin.items():
        table += "| {:<{}} | {:<{}} |\n".format(str(k), max_key_len, str(v), max_val_len)
        table += ll
    return table

def listToTABLE(inplist):
    """
    ## Example:
    ```py
    import PyDB
    print(PyDB.listToTABLE(["as","asd","jkasdg", True]))
    ```
    ## Output:
    ```
    +---+--------+
    | 0 | as     |
    +---+--------+
    | 1 | asd    |
    +---+--------+
    | 2 | jkasdg |
    +---+--------+
    | 3 | True   |
    +---+--------+
    ```
    """
    if tuple(inplist)==tuple(()):
        return ""
    dictin={}
    sayis=range(len(inplist))
    for i in sayis:
        dictin[i]=inplist[i]
    max_key_len = max(len(str(k)) for k in sayis)
    max_val_len = max(len(str(v)) for v in inplist)
    ll = "+" + "-" * (max_key_len + 2) + "+" + "-" * (max_val_len + 2) + "+\n"
    table = ll
    for k, v in dictin.items():
        table += "| {:<{}} | {:<{}} |\n".format(str(k), max_key_len, str(v), max_val_len)
        table += ll
    return table
