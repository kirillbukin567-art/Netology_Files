# Задание 3
def count_str(path):
    k=0
    with open(path,'r',encoding='UTF-8') as f:
        for line in f:
            k+=1
    return k
print(count_str('3.txt'))

def sort_files(sp):
    n=len(sp)
    for i in range(n):
        swapped = False
        for j in range(0,n-i-1):
            if count_str(sp[j]) <  count_str(sp[j+1]):
                sp[j],sp[j+1] = sp[j+1], sp[j]
                swapped = True
        if not swapped:
            break
    return sp

sp=['1.txt', '2.txt', '3.txt']
print(sort_files(sp))
 
def slerge(path,sp):
    with open(path,'w',encoding='utf-8') as f:
        for file in sp:
            f.write(file)
            f.write('\n')
            f.write(str(sp.index(file)+1))
            f.write('\n')
            with open(file,'r',encoding='utf-8') as slf:
                f.write(slf.read())
                f.write('\n')
            
sp1=sort_files(sp)
slerge('4.txt',sp1)