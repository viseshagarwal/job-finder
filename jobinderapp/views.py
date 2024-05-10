from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import mimetypes

import mysql.connector as mydb

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

connection = mydb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
    auth_plugin=os.getenv("DB_AUTH_PLUGIN"),
)

cur = connection.cursor()


def email(request):
    if request.method == "POST":
        subject = "Thank you for registering to our site"
        message = " it  means a world to us "
        email_id = request.POST["forget_email"]
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, email_id)
        # print(email_id)
        return redirect(Homepage)
    else:
        return redirect(Homepage)


def Homepage(request):
    # seek_id=request.COOKIES['Job_Seeker_Id']
    seek_id = 0
    comp_id = 0
    if request.COOKIES.get("Job_Seeker_Id"):
        seek_id = request.COOKIES["Job_Seeker_Id"]
    if request.COOKIES.get("Company_Id"):
        comp_id = request.COOKIES["Company_Id"]
    cur.execute(
        # "SELECT company_mst.Name, Count(job_mst.Company_Id), company_mst.Logo, company_mst.Company_Id FROM company_mst INNER JOIN job_mst ON company_mst.Company_Id = job_mst.Company_Id GROUP BY company_mst.Name, job_mst.Company_Id, company_mst.Logo;"
        "SELECT company_mst.Name, Count(job_mst.Company_Id), company_mst.Logo, company_mst.Company_Id FROM company_mst INNER JOIN job_mst ON company_mst.Company_Id = job_mst.Company_Id GROUP BY company_mst.Name, job_mst.Company_Id HAVING (((Count(job_mst.Company_Id))>=3)) ORDER BY Count(job_mst.Company_Id) DESC"
    )
    data = cur.fetchall()

    cur.execute("Select * from city")
    data2 = cur.fetchall()

    cur.execute(
        "SELECT Distinct(Job_Post_Experience) from job_mst order by Job_Post_Experience"
    )
    data3 = cur.fetchall()

    return render(
        request,
        "user/index.html",
        {
            "comp": data,
            "seek": seek_id,
            "company_id": comp_id,
            "location": data2,
            "expr": data3,
        },
    )


def Aboutpage(request):
    return render(request, "user/about.html")


def Contactpage(request):
    return render(request, "user/contact.html")


def Errorpage(request):
    return render(request, "user/404_error.html")


def AddPostpage(request):

    cur.execute("SELECT * FROM category_mst")
    data = cur.fetchall()

    cur.execute("SELECT * FROM state")
    data1 = cur.fetchall()

    cur.execute("SELECT * FROM city")
    data2 = cur.fetchall()

    return render(
        request,
        "user/add_postin.html",
        {"categories": data, "state1": data1, "city1": data2},
    )


def AddPost_Add_Process(request):
    if request.method == "POST":
        # print(request.POST)
        company = request.session["Company_Id"]
        title = request.POST["job_title"]
        category = request.POST["job_category"]
        jobtype = request.POST["job_type"]
        salary = request.POST["job_salary"]
        exp = request.POST["Experience"]
        description = request.POST["job_description"]
        resp = request.POST["job_responsibilities"]
        state = request.POST["job_state"]
        city = request.POST["job_city"]
        quali = request.POST["Qualification"]
        cur.execute(
            "INSERT INTO `job_mst`(`Company_Id`,`Category_Id`, `City_Id`, `Job_Post_Name`,`Job_Post_Type`,`Job_Post_Experience`,`Job_Post_Responsibility`,`Job_Post_Salary` , `Job_Post_Description`, `Job_Post_Educational_Qualification`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                company,
                category,
                city,
                title,
                jobtype,
                exp,
                resp,
                salary,
                description,
                quali,
            )
        )
        conn.commit()
        return redirect(AddPostpage)
    else:
        return redirect(AddPostpage)


def Register_User_Add(request):
    if request.method == "POST":
        # print(request.POST)
        name = request.POST["user_name_txt"]
        email = request.POST["user_email_txt"]
        passwd = request.POST["user_password_txt"]
        address = request.POST["user_address_txt"]
        mobile = request.POST["user_mobile_txt"]
        dob = request.POST["user_dob"]
        gen = request.POST["js_gender"]

        myfile = request.FILES["js_resume"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        myfile1 = request.FILES["js_photo"]
        fs1 = FileSystemStorage()
        filename1 = fs1.save(myfile1.name, myfile1)
        profile_pic = fs1.url(filename1)

        cur.execute(
            "INSERT INTO `seek_mst`(`Password`,`Name`,`Address`,`Date_Of_Birth`,`EMail_Id`,`Gender`,`Mobile_Number`,`Resume`,`Profile_Photo`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                passwd,
                name,
                address,
                dob,
                email,
                gen,
                mobile,
                uploaded_file_url,
                profile_pic,
            )
        )
        conn.commit()
        return redirect(Registerpage)
    else:
        return redirect(Registerpage)


def Registerpage(request):
    return render(request, "user/register.html")


def Jobpage(request):
    cur.execute(
        "SELECT job_mst.Job_Post_Name,company_mst.Name,company_mst.Address,job_mst.Job_Post_Type,job_mst.Job_Post_Salary,job_mst.Job_Post_Id,company_mst.logo, company_mst.Company_Id FROM job_mst,company_mst where job_mst.Company_Id=company_mst.Company_Id"
    )
    data = cur.fetchall()

    cur.execute("Select * from category_mst")
    data1 = cur.fetchall()

    cur.execute("Select * from city")
    data2 = cur.fetchall()

    cur.execute(
        "SELECT Distinct(Job_Post_Experience) from job_mst order by Job_Post_Experience"
    )
    data3 = cur.fetchall()

    return render(
        request,
        "user/job_list.html",
        {"jobs": data, "cat": data1, "location": data2, "expr": data3},
    )


def job_filter(request):
    cur.execute(
        "SELECT job_mst.Job_Post_Name,company_mst.Name,company_mst.Address,job_mst.Job_Post_Type,job_mst.Job_Post_Salary,job_mst.Job_Post_Id,company_mst.logo, company_mst.Company_Id FROM job_mst,company_mst where job_mst.Company_Id=company_mst.Company_Id"
    )
    data = cur.fetchall()

    cur.execute("Select * from category_mst")
    data1 = cur.fetchall()

    cur.execute("Select * from city")
    data2 = cur.fetchall()

    cur.execute(
        "SELECT Distinct(Job_Post_Experience) from job_mst order by Job_Post_Experience"
    )
    data3 = cur.fetchall()

    return render(
        request,
        "user/job_list.html",
        {"jobs": data, "cat": data1, "location": data2, "expr": data3},
    )


def Pricingpage(request):
    return render(request, "user/pricing.html")


def Payment(request):
    return render(request, "user/payment.html")


def Applied_user(request):
    seek_id = request.COOKIES["Job_Seeker_Id"]
    cur.execute(
        # "Select * from apply_mst where Job_Seeker_Id = {}".format(seek_id)
        "SELECT company_mst.Name, job_mst.Job_Post_Name, job_mst.Job_Post_Description, apply_mst.Job_Application_Date, apply_mst.Job_Application_Time, apply_mst.Job_Application_Status FROM (company_mst INNER JOIN apply_mst ON company_mst.Company_Id = apply_mst.Company_Id) INNER JOIN job_mst ON (job_mst.Job_Post_Id = apply_mst.Job_Post_Id) AND (company_mst.Company_Id = job_mst.Company_Id) where Job_Seeker_Id = {}".format(
            seek_id
        )
    )
    data = cur.fetchall()
    return render(request, "user/applied_user.html", {"seek_data": data})


def Applied_company(request):
    comp_id = request.COOKIES["Company_Id"]
    print(comp_id)
    cur.execute(
        " SELECT seek_mst.Name, seek_mst.EMail_Id, seek_mst.Gender, seek_mst.Mobile_Number, seek_mst.Resume, job_mst.Job_Post_Name, apply_mst.Job_Application_Date, apply_mst.Job_Application_Time, apply_mst.Job_Seeker_Id FROM job_mst INNER JOIN (seek_mst INNER JOIN apply_mst ON seek_mst.Job_Seeker_Id = apply_mst.Job_Seeker_Id) ON job_mst.Job_Post_Id = apply_mst.Job_Post_Id where job_mst.Company_Id = {}".format(
            comp_id
        )
    )
    data = cur.fetchall()
    return render(request, "user/applied_company.html", {"comp_data": data})


def Changepage(request):
    return render(request, "user/change.html")


def ChangePass_Process(request):
    if request.method == "POST":
        old = request.POST["old_pass"]
        new = request.POST["new_pass1"]
        id = 5
        # new = request.POST['c_pass1']
        # cur.execute()
        cur.execute(
            "Update seek_mst set Password = {} where Job_Seeker_Id = {} ".format(
                new, id
            )
        )
        conn.commit()
        return redirect(Changepage)
    else:
        return redirect(Changepage)


"""
def Job_single(request):
    return render(request, 'user/job_single.html')
"""


def Candidate_single(request, id):
    cur.execute("select * from seek_mst where Job_Seeker_Id = {}".format(id))
    data = cur.fetchone()
    return render(request, "user/candidate.html", {"cand": data})


def Company_single(request, id):
    cur.execute(
        " SELECT company_mst.Name, company_mst.Address, company_mst.Company_Type, company_mst.About_Company, company_mst.Website, company_mst.Mobile_Number, company_mst.EMail_Id, company_mst.Logo, Count(job_mst.Company_Id),company_mst.Company_Id  FROM company_mst INNER JOIN job_mst ON company_mst.Company_Id = job_mst.Company_Id where company_mst.Company_Id =  {} GROUP BY company_mst.Name, company_mst.Address, company_mst.Company_Type, company_mst.About_Company,  company_mst.Website,  company_mst.Mobile_Number,  company_mst.EMail_Id, company_mst.Logo, job_mst.Company_Id".format(
            id
        )
    )
    data = cur.fetchone()
    return render(request, "user/company_single.html", {"comp": data})


"""
def Register_user(request):
    return render(request, 'user/signup_user.html')
"""


def Register_company(request):
    return render(request, "user/signup_comp.html")


def Register_Company_Add(request):
    if request.method == "POST":
        # print(request.POST)
        name = request.POST["comp_name_txt"]
        email = request.POST["comp_email_txt"]
        passwd = request.POST["comp_enter_password_txt"]
        comptype = request.POST["comp_type_txt"]
        address = request.POST["comp_address_txt"]
        mobile = request.POST["comp_mobile_txt"]
        web = request.POST["comp_website_txt"]

        myfile = request.FILES["comp_logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        logo = fs.url(filename)

        """
        filename = request.FILES['comp_logo'].name
        try:
            logo = request.FILES['comp_logo']

            f = open("jobfinder/logos/"+filename, 'wb')

            for i in resume:
                f.write(i)
            f.close()
        except:
            pass
        """
        cur.execute(
            "INSERT INTO `company_mst`(`Password`,`Name`,`Company_Type`,`Address`,`EMail_Id`,`Mobile_Number`,`Website`,`Logo`,`IsAdmin`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','0')".format(
                passwd, name, comptype, address, email, mobile, web, logo
            )
        )
        conn.commit()
        return redirect(Register_company)
    else:
        return redirect(Register_company)


def Job_single_Page(request, id):
    cur.execute(
        " SELECT job_mst.Job_Post_Description, job_mst.Job_Post_Name, company_mst.Logo, company_mst.Company_Id, company_mst.Name, City.City_Name, job_mst.Job_Post_Salary, job_mst.Job_Post_Experience, job_mst.Job_Post_Responsibility, job_mst.Job_Post_Educational_Qualification, category_mst.Category_Name,job_mst.Job_Post_Id FROM category_mst INNER JOIN (company_mst INNER JOIN (City INNER JOIN job_mst ON City.City_Id = job_mst.City_Id) ON company_mst.Company_Id = job_mst.Company_Id) ON category_mst.Category_Id = job_mst.Category_Id where job_mst.Job_Post_Id =  {}".format(
            id
        )
    )
    data = cur.fetchone()
    return render(request, "user/job_single.html", {"job": data})


def Search_job(request):
    if request.method == "GET":
        # print(request.POST)
        # exp=12
        Search_job = request.GET["keyword"]
        location = request.GET["Location"]
        exp = request.GET["Exp"]
        cur.execute(
            # "SELECT job_mst.Job_Post_Name,company_mst.Name,company_mst.Address,job_mst.Job_Post_Type,job_mst.Job_Post_Salary, company_mst.Logo, company_mst.Company_Id,job_mst.Job_Post_Id FROM job_mst,company_mst where job_mst.Company_Id=company_mst.Company_Id and job_mst.Job_Post_Experience ='{}'  or  job_mst.City_Id = '{}' or  MATCH(job_mst.Job_Post_Name) AGAINST('{}') ".format(exp,location,Search_job))
            "SELECT job_mst.Job_Post_Name, company_mst.Name, company_mst.Address, job_mst.Job_Post_Type, job_mst.Job_Post_Salary, company_mst.Logo, company_mst.Company_Id, job_mst.Job_Post_Id FROM company_mst INNER JOIN job_mst ON company_mst.Company_Id = job_mst.Company_Id where MATCH(job_mst.Job_Post_Name) AGAINST('{}') and  job_mst.City_Id = '{}' and job_mst.Job_Post_Experience <='{}' ".format(
                Search_job, location, exp
            )
        )
    data = cur.fetchall()

    cur.execute("Select * from category_mst")
    data1 = cur.fetchall()

    cur.execute("Select * from city")
    data2 = cur.fetchall()

    cur.execute(
        "SELECT Distinct(Job_Post_Experience) from job_mst order by Job_Post_Experience"
    )
    data3 = cur.fetchall()

    return render(
        request,
        "user/job_search.html",
        {"sjobs": data, "cat": data1, "location": data2, "expr": data3},
    )


def Loginpage(request):
    if request.method == "POST":
        # print(request.POST)
        user_email = request.POST["user_email"]
        user_pass = request.POST["user_pass"]
        cur.execute(
            "select * from `seek_mst` where `EMail_Id` = '{}' and `Password` = '{}'".format(
                user_email, user_pass
            )
        )
        data = cur.fetchone()

        if data is not None:

            if len(data) > 0:
                # Fetch Data
                user_db_id = data[0]
                user_db_email = data[5]
                # print(user_db_id)
                # print(user_db_email)
                # Session Create Code

                request.session["Job_Seeker_Id"] = user_db_id
                request.session["EMail_Id"] = user_db_email
                # Session Create Code
                # Cookie Code
                messages.add_message(request, messages.SUCCESS, "Sucessfull login")
                response = redirect(Homepage)
                response.set_cookie("Job_Seeker_Id", user_db_id)
                response.set_cookie("EMail_Id", user_db_email)
                return response
                # Cookie Code
            else:
                messages.add_message(request, messages.WARNING, "fail login")
                return render(request, "user/login.html")
        messages.add_message(request, messages.WARNING, "Login Failed")
        return render(request, "user/login.html")

    # return redirect(dashboard)
    else:
        return render(request, "user/login.html")


def Forgetpage(request):
    return render(request, "user/forget.html")


def ForgetPasswordAction(request):
    # if request.method == 'POST':
    email_id = request.POST["txt1"]
    cur.execute("select * from `seek_mst` where `EMail_Id` = '{}'".format(email_id))
    data = cur.fetchone()
    user_db_email = data[1]
    subject = "Forgot Password"
    message = "Password is " + user_db_email

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email_id,
    ]
    send_mail(subject, message, email_from, recipient_list)
    # print(email_id)
    return redirect(Homepage)
    # else:
    #   return redirect(Changepage)


def dashboard(request):
    if "EMail_Id" in request.COOKIES and request.session.has_key("EMail_Id"):

        user_emails = request.session["EMail_Id"]
        user_emailc = request.COOKIES["EMail_Id"]

        # print("Session is  " + admin_emails)
        # print("Cookie is  " + admin_emailc)

        return render(Homepage)
    else:
        return redirect(Loginpage)


def logout(request):
    del request.session["EMail_Id"]
    del request.session["Job_Seeker_Id"]
    response = redirect(Loginpage)
    response.delete_cookie("Job_Seeker_Id")
    response.delete_cookie("EMail_Id")
    return response


def Loginpage_company(request):
    if request.method == "POST":
        # print(request.POST)
        user_email = request.POST["user_email"]
        user_pass = request.POST["user_pass"]
        cur.execute(
            "select * from `company_mst` where `EMail_Id` = '{}' and `Password` = '{}'".format(
                user_email, user_pass
            )
        )
        data = cur.fetchone()

        if data is not None:

            if len(data) > 0:
                # Fetch Data
                user_db_id = data[0]
                user_db_email = data[6]
                # print(user_db_id)
                # print(user_db_email)
                # Session Create Code
                request.session["Company_Id"] = user_db_id
                request.session["EMail_Id"] = user_db_email
                # Session Create Code
                # Cookie Code
                response = redirect(Homepage)
                response.set_cookie("Company_Id", user_db_id)
                response.set_cookie("EMail_Id", user_db_email)
                return response
                # Cookie Code
            else:
                return render(request, "user/login_company.html")
        return render(request, "user/login_company.html")

    # return redirect(dashboard)
    else:
        return render(request, "user/login_company.html")


def dashboard_company(request):
    if "EMail_Id" in request.COOKIES and request.session.has_key("EMail_Id"):

        user_emails = request.session["EMail_Id"]
        user_emailc = request.COOKIES["EMail_Id"]

        # print("Session is  " + admin_emails)
        # print("Cookie is  " + admin_emailc)

        return render(Homepage)
    else:
        return redirect(Loginpage_company)


def logout_company(request):
    # del request.session['Company_Id']
    # del request.session['EMail_Id']
    response = redirect(Loginpage_company)
    response.delete_cookie("Company_Id")
    response.delete_cookie("EMail_Id")
    return response


def Applied_Add_Process(request):
    if request.method == "POST":
        company = request.POST["comp_id"]
        post_id = request.POST["job_post_id"]
        seeker = request.COOKIES["Job_Seeker_Id"]
        dt = datetime.today().strftime("%Y-%m-%d")
        tt = datetime.today().strftime("%H:%M:%S")
        status = "Submitted"
        cur.execute(
            "INSERT INTO `apply_mst`(`Company_Id`,`Job_Seeker_Id`,`Job_Post_Id`,`Job_Application_Date`,`Job_Application_Time`,`Job_Application_Status`) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                company, seeker, post_id, dt, tt, status
            )
        )
        conn.commit()
        return redirect(Applied_user)
    else:
        return redirect(Applied_user)


def job_by_category(request, id):
    cur.execute(
        "SELECT job_mst.Job_Post_Name,company_mst.Name,company_mst.Address,job_mst.Job_Post_Type,job_mst.Job_Post_Salary, company_mst.Logo, company_mst.Company_Id,job_mst.Job_Post_Id FROM job_mst,company_mst where job_mst.Company_Id=company_mst.Company_Id and job_mst.Category_Id = '{}' ".format(
            id
        )
    )
    data = cur.fetchall()

    return render(request, "user/job_search.html", {"sjobs": data})


def job_by_location(request, id):
    cur.execute(
        "SELECT job_mst.Job_Post_Name,company_mst.Name,company_mst.Address,job_mst.Job_Post_Type,job_mst.Job_Post_Salary, company_mst.Logo, company_mst.Company_Id,job_mst.Job_Post_Id FROM job_mst,company_mst where job_mst.Company_Id=company_mst.Company_Id and job_mst.City_Id = '{}' ".format(
            id
        )
    )
    data = cur.fetchall()

    return render(request, "user/job_search.html", {"sjobs": data})


def JobSeeker_Edit(request, id):
    cur.execute("select * from `seek_mst` where `Job_Seeker_Id` = {}".format(id))
    data = cur.fetchone()
    return render(request, "user/edit-jobseeker.html", {"seek": data})


def JobSeeker_Update(request):
    if request.method == "POST":
        jobseeker_id = request.POST["js_id_txt"]
        jobseeker_name = request.POST["user_name_txt"]
        # jobseeker_passwd = request.POST['js_passwd_txt']
        jobseeker_dob = request.POST["user_dob"]
        jobseeker_address = request.POST["user_address_txt"]
        jobseeker_email = request.POST["user_email_txt"]
        # jobseeker_gender = request.POST['js_gender_txt']
        jobseeker_mob = request.POST["user_mobile_txt"]
        # jobseeker_pic = request.POST['js_photo']
        # jobseeker_resume = request.POST['js_resume']

        myfile = request.FILES["js_resume"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        myfile1 = request.FILES["js_photo"]
        fs1 = FileSystemStorage()
        filename1 = fs1.save(myfile1.name, myfile1)
        profile_pic = fs1.url(filename1)

        cur.execute(
            "update `seek_mst` set `Name` ='{}', `Address` ='{}', `Date_Of_Birth` ='{}', `EMail_Id` ='{}', `Mobile_Number` ='{}', `Resume` ='{}', `Profile_Photo` ='{}' where `Job_Seeker_Id`='{}'".format(
                jobseeker_name,
                jobseeker_address,
                jobseeker_dob,
                jobseeker_email,
                jobseeker_mob,
                uploaded_file_url,
                profile_pic,
                jobseeker_id,
            )
        )
        conn.commit()
        return redirect(Homepage)
    else:
        return redirect(Homepage)


def Company_Edit(request, id):
    cur.execute("select * from `company_mst` where `Company_Id` = {}".format(id))
    data = cur.fetchone()
    return render(request, "user/edit-Company.html", {"comp": data})


def Company_Update(request):
    if request.method == "POST":
        comp_id = request.POST["comp_id_txt"]
        comp_name = request.POST["comp_name_txt"]
        comp_type = request.POST["comp_type_txt"]
        comp_address = request.POST["comp_address_txt"]
        comp_email = request.POST["comp_email_txt"]
        comp_mobile = request.POST["comp_mobile_txt"]
        company_about = request.POST["comp_about_txt"]
        company_website = request.POST["comp_website_txt"]

        myfile = request.FILES["comp_logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        logo = fs.url(filename)

        cur.execute(
            "update `company_mst` set `Name` ='{}', `Company_Type` ='{}', `Address` ='{}', `Email_Id` ='{}', `Mobile_Number` ='{}', `Website` ='{}', `About_Company` ='{}', `Logo` ='{}'  where `Company_Id`='{}'".format(
                comp_name,
                comp_type,
                comp_address,
                comp_email,
                comp_mobile,
                company_website,
                company_about,
                logo,
                comp_id,
            )
        )
        conn.commit()
        return redirect(Homepage)
    else:
        return redirect(Homepage)


def AddPost_Edit_Process(request, id):

    cur.execute("SELECT * FROM category_mst")
    data = cur.fetchall()

    cur.execute("SELECT * FROM state")
    data1 = cur.fetchall()

    cur.execute("SELECT * FROM city")
    data2 = cur.fetchall()

    cur.execute("select * from `job_mst` where `Job_Post_Id` = {}".format(id))
    data3 = cur.fetchone()
    return render(
        request,
        "user/edit-postin.html",
        {"categories": data, "state1": data1, "city1": data2, "job": data3},
    )


def AddPost_update_Process(request):
    # print(request.POST)
    company = request.session["Company_Id"]
    job_post_id = request.POST["post_id"]
    title = request.POST["job_title"]
    category = request.POST["job_category"]
    jobtype = request.POST["job_type"]
    salary = request.POST["job_salary"]
    exp = request.POST["Experience"]
    qual = request.POST["Qualification"]
    description = request.POST["job_description"]
    resp = request.POST["job_responsibilities"]
    state = request.POST["job_state"]
    city = request.POST["job_city"]
    cur.execute(
        # "INSERT INTO `job_mst`(`Company_Id`,`Category_Id`, `City_Name`, `Job_Post_Name`,`Job_Post_Type`,`Job_Post_Experience`,`Job_Post_Responsibility`,`Job_Post_Salary` where job_mst.City_Id = city.City_Id) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(company, category, title, jobtype, exp, salary, resp, city))
        # "INSERT INTO `job_mst`(`Company_Id`,`Category_Id`, `City_Name`, `Job_Post_Name`,`Job_Post_Type`,`Job_Post_Experience`,`Job_Post_Responsibility`,`Job_Post_Salary` where job_mst.City_Id = city.City_Id) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(company, category, title, jobtype, exp, salary, resp, city))
        "UPDATE `job_mst` SET `Job_Post_Name` = '{}', `Job_Post_Type` = '{}', `Job_Post_Description` = '{}', `Job_Post_Responsibility` = '{}', `Job_Post_Educational_Qualification` = '{}', `Job_Post_Experience` = '{}', `Job_Post_Salary` = '{}',`Company_Id` = '{}', `Category_Id` = '{}', `City_Id` = '{}' WHERE (`Job_Post_Id` = '{}')".format(
            title,
            jobtype,
            description,
            resp,
            qual,
            exp,
            salary,
            company,
            category,
            city,
            job_post_id,
        )
    )
    conn.commit()
    return redirect(AddPostpage)


def AddPost_delete(request, id):
    cur.execute("delete from `job_mst` where `Job_Post_Id` = {}".format(id))
    conn.commit()
    return redirect(Homepage)
