import csv
from xlwt import *
import time
 
#读取csv文件
sCsvFileName='202221027 (2).csv'

#避免读取CSV文件出现中文显示乱码，加encoding='utf-8'
workbook=Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('sheet1')
 
#i=0
with open(sCsvFileName,newline='',encoding='UTF-8') as csvfile:
    rows=csv.reader(csvfile)
    print('==================================')
 
    for iRow,row in enumerate(rows):
 
        #判断有几列
        if iRow==1:
            iCols=len(row)
 
        #读取第4行
        if iRow==3:
            print('一条记录：'+','.join(row))
 
        #读取第6行第2列的数值
        if iRow==5:
            a=','.join(row).split(',')[1]
            print('第6行第2列的值：'+a)
 
        #写入到Excel文件中
        for iCol in range(0,len(row)):
            worksheet.write(iRow,iCol,','.join(row).split(',')[iCol])
 
sFileName='Test_' + time.strftime("%Y%m%d_%H%M%S",time.localtime()) + '.xls'
workbook.save(sFileName)            
 
print('记录数:'+str(iRow))
print('列数:'+str(iCol))
print('write over')
 
print('==================================')