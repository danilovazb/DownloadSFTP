import psutil
import time
import sys
def monitor(pid):
        while True:
                time.sleep(5)
                if psutil.pid_exists(int(pid)) == True:
                        p = psutil.Process(int(pid))
                        if p.status() == psutil.STATUS_ZOMBIE:
                                print("Processo ZOMBIE: %s" % (pid))
                        else:
                                print("Existe: %s" % (pid))
                else:
                        print("Processo MORTO: %s" % (pid))
pid = sys.argv[1]
monitor(pid)
