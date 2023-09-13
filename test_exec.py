import os
os.execl("/usr/bin/python3", "python3", "hello.py")
print("this should not print")