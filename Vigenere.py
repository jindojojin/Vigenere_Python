from hashlib import sha224, sha256, sha384, sha512
import os
UPDATE_SIZE_BLOCK= 1024*10 # update every 1KB finish
HASH_FUNC=[sha224,sha256,sha384,sha512]
def get_hash_func(r:str):
    return HASH_FUNC[ord(r)%len(HASH_FUNC)]

class Vigenenere:
    def __init__(self, encryptPassword:str):
        self.password = encryptPassword if len(encryptPassword) else "password"
        self.renew_pass()
        
    
    def renew_pass(self):
        self.hash_func = get_hash_func(self.password[0])
        self.password = self.hash_func(self.password.encode('utf-8')).hexdigest()
        self.m = len(self.password)
        self.K = [ord(p) for p in self.password]
    
    def encrypt(self, file_path:str, output_file_path=None, onProgressUpdate=None, delete_after_done=False, onExeption = None, decryptMode=False):
        if(not output_file_path):
            if not decryptMode:output_file_path = file_path
            else:
                head, tail = os.path.split(file_path)
                output_file_path = os.path.join(head,"VigDecrypted_"+tail.replace('.vig',''))
        inputFile = open(file_path, "rb")
        outputFile = open(output_file_path+'.vig', "wb")
        byte = inputFile.read(1)
        kidx = 0
        finishedByte= 0
        mode = -1 if decryptMode else 1
        while byte != b"":
            outputFile.write(((ord(byte) + mode*self.K[kidx]) % 256).to_bytes())
            kidx = (kidx+1) % self.m
            if(kidx==0): self.renew_pass()
            finishedByte += 1
            if finishedByte % UPDATE_SIZE_BLOCK == 0 and onProgressUpdate:
                onProgressUpdate(finishedByte)
            byte = inputFile.read(1)
        inputFile.close()
        outputFile.close()
        if onProgressUpdate: onProgressUpdate(finishedByte)
        if delete_after_done: 
            try:
                os.remove(file_path)
            except Exception as e:
                if onExeption: onExeption(e)
                else: e.__traceback__
                pass

    def decrypt(self,file_path:str, output_file_path=None, onProgressUpdate=None, delete_after_done=False, onExeption = None):
        self.encrypt(file_path,output_file_path,onProgressUpdate,delete_after_done,onExeption,True)
       


if __name__ == "__main__":
    vg = Vigenenere("TranQuangLinh")
    vg.encrypt("text.test")
    vg2= Vigenenere("TranQuangLinh")
    vg2.decrypt("text.test.vig")

