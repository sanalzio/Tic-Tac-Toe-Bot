class bgm:
    def __init__(self):
        self.data=[]

    def loaddata(self, inplist):
        self.data=[inplist]

    def loadfile(self, file):
        with open(file) as f:
            datas=f.read().split("\n\n")
            for data in datas:
                self.data.append(data.replace("\n", " ").split(" "))

    def createmodel(self, modelname):
        import pickle
        with open(modelname+".h5", "wb") as f:
            pickle.dump(self.data, f)

    def loadmodel(self, modelname):
        import pickle
        with open(modelname+".h5", "rb") as f:
            self.data=pickle.load(f)

    def getprediction(self, board):
        if len(self.data) == 0:
            raise Exception("Model not loaded.")
        matching_results = []
        for bdat in self.data:
            tb = bdat[:len(bdat)-1]
            for ei in range(0, len(tb)):
                e = tb[ei]
                if e == ".":
                    tb[ei] = board[ei]
                    if tb[ei] != board[ei]:
                        break
                if tb == board:
                    matching_results.append(bdat)
        if len(matching_results)!=0:
            if len(matching_results)==1:
                return int(matching_results[0][len(matching_results[0])-1])
            import random
            tli=random.randint(0, len(matching_results)-1)
            tl=matching_results[tli]
            return int(tl[len(tl)-1])
        else:
            return None