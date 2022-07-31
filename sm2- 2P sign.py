import random
import hashlib
x_G=0x421debd61b62eab6746434ebc3cc315e32220b3badd50bdc4c4e6c147fedd43d
y_G=0x0680512bcbb42c07d47349d2153b70c4e5d7fdfcbfa36ea1a85841b9e46e09a2
G=(int(x_G),int(y_G))       #椭圆曲线的基点
n=0x8542d69e4c044f18e8b92435bf6ff7dd297720630485628d5ae74ee7c32e79b7
M=input("Please enter the message:")
def Hash(str):     #采用sha256作为hash函数
    m=hashlib.sha256()
    m.update(str.encode(encoding='utf-8'))
    str_sha256=m.hexdigest()
    return str_sha256
d1=random.randint(1,n)
def PART1_1(n):
    P1=(pow(d1,n-2,n)*G[0],pow(d1,n-2,n)*G[1])       #利用费马小定理求模逆
    return P1
d2=random.randint(1,n)
def PART2_1(n):
    P1=PART1_1(n)
    P=(pow(d2,n-2,n)*P1[0]-G[0],pow(d2,n-2,n)*P1[1]-G[1])
    print("Pub-Key is:",P)
    return P
k1=random.randint(1,n)
def PART1_2(n):
    P=PART2_1
    Z=Hash('1'+ '23'+str(G[0])+str(G[1]))    #Z为用户标识，部分椭圆曲线参数和用户公钥的杂凑
    M1=str(Z)+M
    e=int('0x'+Hash(M1),16)
    Q1=(k1*G[0],k1*G[1])
    return Q1,e
k2=random.randint(1,n)
k3=random.randint(1,n)
def PART2_2(n):
    Q1,e=PART1_2(n)
    Q2=(k2*G[0],k2*G[1])
    x1=k2*Q1[0]+Q2[0]
    y1=k2*Q1[1]+Q2[1]
    r=(x1+e)%n
    s2=(d2*k3)%n
    s3=d2*(r+k2)%n
    return r,s2,s3
def PART1_3(n):
    r,s2,s3=PART2_2(n)
    print("PART1接收完毕")
    s=((d1*k1)*s2+d1*s3-r)%n
    if (s!=0) or (s!=n-r):
        print("签名为：",(str(r),str(s)))
    else:
        print("error!")
def sign(n):
    PART1_1(n)
    print("PART1已发送")
    print("PART2正在接收")
    PART2_1(n)
    print("PART2接收完毕")
    print("PART2已发送")
    print("PART1正在接收")
    PART1_2(n)
    print("PART1接受完毕")
    print("PART1已发送")
    print("PART2正在接收")
    PART2_2(n)
    print("PART2接收完毕")
    print("PART2已发送")
    print("PART1正在接收")
    PART1_3(n)
sign(n)
