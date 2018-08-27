import time, os

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == "__main__":
    logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
    loglines = follow(logfile)
    for line in loglines:
        if "[Client thread/INFO]: [CHAT]" in line:
            message = line[40:]
            liste = message.split(' ')
            liste.append("-")
            liste.append("-")
            liste.append("-")
            if liste[3] == 'hat' or liste[3] == 'hat\n':#2tes nur für lokal
                joining = ''
                for ele in liste:
                    joining += ele
                    joining += ' '
                print('Spieler:', liste[2])
                print('Betrag:', liste[5])
                
                    
            
