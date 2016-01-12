# -*- coding: utf-8 -*-

#base58인코딩부분에서 공부 다시 시작
#https://github.com/gferrin/bitcoin-code/blob/master/utils.py
#http://www.righto.com/2014/02/bitcoins-hard-way-using-raw-bitcoin.html

import ecdsa
import ecdsa.der
import hashlib
import unittest
import random
import re
import struct

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

#import utils

#개인키를 wif(Wallet Interchange Format)으로 바꿔줌
def privateKeyToWif(key_hex):
    return base58CheckEncode(0x80, key_hex.decode('hex'))

#만들어진 개인키를 공개키로 바꿔줌
#입력값은 16진수 문자열(헥스 스트링)
def privateKeyToPublicKey(s):
    #헥사(16진수)형태로 들어온 랜덤 개인키를 원래의 16진수로 디코딩시킨 후, 
    #타원곡선알고리즘(SECP256k1)을 이용해서 싸인 키(개인키)를 만듬
    #(들어온 개인키는 SECP256k1알고리즘에 의해 이미 만들어진 키를 받아야 한다.)
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    #싸인키(개인키)로부터 확인키(공개키)를 추출함
    vk = sk.verifying_key
    
    #'\04'의 의미?
    #비압축 공개키는 04접두부(x,y좌표 모두 포함됨)
    #압축 공개키는 02,03접두부를 사용한다(02: x좌표, 04: y좌표)
    #주소의 버전 접두부인 \x : 0x00이 붙었다.
    return ('\04'+vk.to_string()).encode('hex')

#퍼블릭키를 비트코인 주소로 바꿔주는 함수
def pubKeyToAddr(s):
    #ripemd160객체를 생성
    ripemd160 = hashlib.new('ripemd160')
    #입력된 문자열을 헥스로 디코딩하고, sha256방식으로 다이제스트시킨 후
    #ripemd160객체에 넣어준다(업데이트)
    ripemd160.update(hashlib.sha256(s.decode('hex')).digest())
    
    return base58CheckEncode(0,ripemd160.digest())

def keyToAddr(s):
    return pubKeyToAddr(privateKeyToPublicKey(s))

def base58CheckEncode(version, payload):
    s = chr(version)+payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s+checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1'*leadingZeros+base58encode(base256decode(result))

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

def base58encode(n):
    result = ''
    while n>0:
        result = b58[n%58]+result
        n /= 58
    return result

def base58decode():
    result = 0
    for i in range(0,len(s)):
        result = result * 58 + b58.index(s[i])
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def privateKeyToWif(key_hex):
    return base58CheckEncode(0x80, key_hex.decode('hex'))


def makePrivKey():
    priv_key =''.join(['%x'% random.randrange(16) for x in range(0,64)])
    return priv_key

if __name__=="__main__":
    #private_key = ''.join(['%x' % random.randrange(16) for x in range(0, 64)])
    #private_key = '72c478e230c777079302dee84a0eea0d5a60376d3034c1c1a67d29bde9a48826'
    #private_key = 'f19c523315891e6e15ae0608a35eec2e00ebd6d1984cf167f46336dabd9b2de4'
    print private_key
    print privateKeyToWif(private_key)
    print keyToAddr(private_key)
