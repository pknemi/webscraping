from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_job_details(baseurl):
    titles_list=[]
    company_list=[]
    experience_list=[]
    salary_list=[]
    location_list=[]
    for count in range (0,1700,20):
        url=baseurl+"?&limit=20&offset="+str(count)
        res=requests.get(url)
        soup=BeautifulSoup(res.text,"html.parser")
        box=soup.find("div",{"class":"main-block fix_block"})
        if box:
            titles=box.find_all("span", {"class": "wrap-title seo_title"})
            companies= box.find_all("h3", {"class": "latest-jobs-title font-16 margin-none inline-block company-name"})
            experiences = box.find_all("div", {"class": "col-md-6 col-xs-6 col-lg-6 padding-none"})
            locations=box.find_all("a",{"class":"bold_font"})
            salaries = box.find_all("span", {"class": "qualifications display-block modal-open pull-left job-details-span"})

            for title, company,experience,location in zip(titles, companies,experiences,locations):
                titles_list.append(title.text.strip())
                company_list.append(company.text.strip())
                experience_list.append(experience.text.strip())
                location_list.append(location.text.strip())

            #salaries = box.find_all("span",{"class": "qualifications display-block modal-open pull-left job-details-span"})
            for salary in salaries:
                salary_text = salary.text.strip()
                if "Monthly" in salary_text or "Yearly" in salary_text or "Salary not disclosed" in salary_text:
                    salary_list.append(salary_text)

    salary_list = salary_list[:1660]
    company_list = company_list[:1660]
    titles_list = titles_list[:1660]
    experience_list = experience_list[:1660]
    location_list = location_list[:1660]

    print(f"salary{len(salary_list)}")
    print(f"title{len(titles_list)}")

    df=pd.DataFrame({"Titles":titles_list,"Company":company_list,"Experience":experience_list,"Salary":salary_list,"Location":location_list})
    df.to_csv("IT_job_scraping.csv")


url='https://www.freshersworld.com/jobs/jobsearch/it-jobs'
get_job_details(url)