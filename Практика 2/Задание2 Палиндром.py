def Palindrome(a):
    a = a.lower()
    a = a.replace(' ', '')
    return a == a[::-1]

a = input()
print(Palindrome(a))
