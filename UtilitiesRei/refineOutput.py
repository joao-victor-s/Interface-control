class refineOutput:
    
    def byteToFloat(self, recv):
        recv = recv.decode("UTF-8")
        recv = recv.rstrip("\n\x00")
        return float(recv)

    def byteToString(self, recv):
        print("fail8")
        recv = bytes(recv)
        recv = recv.decode("UTF-8")
        recv = recv.rstrip('\n')
        recv = recv.rstrip('\x00')
        print("sucess")
        return recv