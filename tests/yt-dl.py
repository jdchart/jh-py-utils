import jhutils.online_files
import os


url = "https://youtu.be/pA2vWc2eeNE?si=TGtaN-XmrcunTWu4"
#url = "https://peertube.arvest.app/w/b2aFoT9Ft3SQGw51Fdi6Dq"

path = jhutils.online_files.download(url, dir = os.path.join(os.getcwd(), "dls"))


print(path)