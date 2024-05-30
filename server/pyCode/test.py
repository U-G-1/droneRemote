import sys

def getName(n1,n2):
    sum = int(n1) +int(n2)
    print(sum)

if __name__ == '__main__':
    getName(sys.argv[1], sys.argv[2])