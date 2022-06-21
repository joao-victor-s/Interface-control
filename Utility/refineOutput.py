class RefineOutput:
    
    def byteToFloat(recv):
        recv = recv.decode("UTF-8")
        recv = recv.rstrip("\n\x00")
        return float(recv)

    def byteToString(recv):
        recv = recv.decode("UTF-8")
        return recv