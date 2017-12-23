def Matrix(n):
    MAT = []
    for i in range(n):
        str = input()   
        MAT.append(str.split(' '))
    return MAT

#  입력 예시
#
#  1 2 3 4
#  5 6 7 8
#  4 3 2 1
#  8 7 6 5
#
# 행의 원소는 모두 한줄이고 구분은 띄어쓰기를 이용한다.
