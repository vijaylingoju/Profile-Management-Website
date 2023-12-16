
def fun(profile_links,scrapped_data,roll_no):
    person_count=0
    for link in profile_links:
        print(link)
        r = requests.get(link)
        
        if r.status_code==200:
            data = BeautifulSoup(r.content,'html.parser')
            res = {"Roll No":roll_no[person_count],"Name":"","Rank":0,"Total Problems Solved":0,"Easy":0,"Medium":0,"Hard":0,"Badges Acheived":0,"Total Submissions this year":0,"Active Days":0,"Max Streak":0,"Contest Ranking":0}
            
            name=data.find('div',class_='text-label-1 dark:text-dark-label-1 break-all text-base font-semibold')
            res["Name"]=name.text

            rank=data.find('span',class_='ttext-label-1 dark:text-dark-label-1 font-medium')
            res["Rank"]=rank.text
            
            total=data.find('div',class_='text-[24px] font-medium text-label-1 dark:text-dark-label-1')
            res["Total Problems Solved"]=int(total.text)

            hardness_array = data.find_all('span',class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')
            d=[]
            for category in hardness_array:
                d.append(int(category.text))
            res["Easy"] = d[0]
            res["Medium"] = d[1]
            res["Hard"] = d[2]
            
            badge=data.find('div',class_='text-label-1 dark:text-dark-label-1 mt-1.5 text-2xl leading-[18px]')
            res["Badges Acheived"]=int(badge.text)

            sub=data.find('span',class_='lc-md:text-xl mr-[5px] text-base font-medium')
            res["Total Submissions this year"] = sub.text

            active=data.find_all('span',class_='font-medium text-label-2 dark:text-dark-label-2')
            d=[]
            for ele in active[::-1]:
                d.append(ele.text)
            res["Max Streak"] = int(d[0])
            res["Active Days"] = int(d[1])

            contest_rank=data.find('div',class_='text-label-1 dark:text-dark-label-1 flex items-center text-2xl')
            if contest_rank:
                res["Contest Ranking"] = contest_rank.text
            else:
                res["Contest Ranking"] = "Not available"
                
            
            scrapped_data.append(res)
            
        else:
            scrapped_data.append({})
            
        person_count+=1





from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

cur_dir = os.getcwd()
print(cur_dir)
excel_file_path = 'C:\Webscraping\input_data_links.xlsx'
df = pd.read_excel(excel_file_path)
profile_links = df['Leetcode profile Link'].tolist()
roll_no = df['Roll No'].tolist()

scrapped_data = []

fun(profile_links,scrapped_data,roll_no)


result_df = pd.DataFrame(scrapped_data)
output_excel_path = os.path.join(cur_dir, 'result_data.xlsx')

result_df.to_excel(output_excel_path,index=False, engine='openpyxl')
print("Done")





