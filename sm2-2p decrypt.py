import random
import hashlib
import math
import binascii
x_G=0x421debd61b62eab6746434ebc3cc315e32220b3badd50bdc4c4e6c147fedd43d
y_G=0x0680512bcbb42c07d47349d2153b70c4e5d7fdfcbfa36ea1a85841b9e46e09a2
G=(int(x_G),int(y_G))        #基点
n=0x8542d69e4c044f18e8b92435bf6ff7dd297720630485628d5ae74ee7c32e79b7
d1=random.randint(1,n)
d2=random.randint(1,n)
P=((pow(d1*d2,n-2,n)-1)*G[0],(pow((d1*d2),n-2,n)-1)*G[1])   #利用费马小定理求模逆
d=pow(d1*d2,n-2,n)-1       #利用费马小定理求模逆
print("public key is:",P)
print("private key is:",d)
def Hash(str):     #采用sha256作为hash函数
    m=hashlib.sha256()
    m.update(str.encode(encoding='utf-8'))
    str_sha256=m.hexdigest()
    return str_sha256
def KDF(x,klen):
    ct=0x00000001
    K=''
    for i in range(1,klen//256):
        ct=ct+1
        K=K+Hash(x+bin(ct)[2:].zfill(32))[1]
    if klen%256 !=0:
        K=K+Hash(x+bin(ct)[2:].zfill(32))[1][:(klen-256*int(klen//256))//4]
    else:
        K=K+Hash(x+bin(ct)[2:].zfill(32))[1]
    K=bin(int(K,16))[2:].zfill(klen)
    return K
def xor(a,b):
    res=""
    for i in range(len(a)):
        add=int(a[i])+int(b[i])
        if add==1:
            res=res+"1"
        else:
            res=res+"0"
    return res
Message=input("please enter the message:")
M=Message.encode(encoding='utf-8',errors='strict')
k=random.randint(1,n)
C1=(k*G[0],k*G[1])
x2=k*P[0]
y2=k*P[1]
Q=bytes.hex(M)        #将消息明文转换为16进制
m=int(Q,16)
bit_M=bin(m)[2:]
bit_M=(8-len(bit_M)%8)*'0'+bit_M
print("消息的二进制表示为：",bit_M)
C3=Hash(bin(int(x2))[2:].zfill(256)+bit_M+bin(int(y2))[2:].zfill(256))
def PART1_1():
    if C1!=0:
        T1=(pow(d1,-1)*C1[0],pow(d1,-1)*C1[1])
        return T1
def PART2_1():
    T1=PART1_1()
    T2=(pow(d2,-1)*T1[0],pow(d2,-1)*T1[1])
    return T2
def PART1_2():
    t=KDF(bin(int(x2))[2:].zfill(256)+bin(int(y2))[2:].zfill(256),len(bit_M))
    C2=xor(bit_M,t)
    M1=xor(C2,t)
    u=Hash(bin(int(x2))[2:].zfill(256)+M1+bin(int(y2))[2:].zfill(256))
    if u==C3:
           print("解密成功，消息二进制为：",M1)
    else:
        print('error')
print("PART1已发送")
print("PART2已接收")
PART1_2()
    
