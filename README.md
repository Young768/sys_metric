# System Metrics

These scripts are used to collect the system resource usage in a distributed environment.

#Prerequisites for monitor
psutil, python3

#Prerequisites for client-server RPC update
python2

For testing RPC

1. creta two folders: test1 and test2

2. create test1.txt in test1, add the port inside the text file http://127.0.0.1:3000

3. create test2.txt in test2, add the port inside the text file http://127.0.0.1:3001

4. creat another text file testfile.txt in folder test2

5. open one terminal： python client.py test1/urltest1.txt  test1/  http://127.0.0.1:3001

   another terminal： python client.py test2/urltest2.txt  test2/  http://127.0.0.1:3000


6. use the command： fetch testfile.txt to copy the file from test2 to test1.
