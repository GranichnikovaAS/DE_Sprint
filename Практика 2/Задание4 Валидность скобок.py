a,b,c = 0,0,0 #Подсчет разных типов скобочек
#Как только одно из чисел становится меньше 0, проверка не пройдена, строка False

def Check():
    if a < 0 or b < 0 or c < 0:
        return False
    else: return True

str = input()
flag = True
for i in str:
    if i == '[': a+=1 
    if i == ']': a-=1
    if i == '(': b+=1
    if i == ')': b-=1
    if i == '{': c+=1
    if i == '}': c-=1
    if flag: flag = Check()
if a > 0 or b > 0 or c > 0: flag = False #Если по итогу есть незакрытые скобки    
print(flag)
   