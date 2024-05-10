from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import mysql.connector as mydb

connection = mydb.connect(
    host="mysql-spd-visesh-spd.a.aivencloud.com",
    user="visesh",
    passwd="AVNS_QVWrxlXGSJWEd9a9TUi",
    database="job_finder",
    port=26275,
    auth_plugin="mysql_native_password",
)

cur = connection.cursor()


def Admin_Homepage(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):
        return render(request, "myAdmin/index.html")
    else:
        return redirect(Admin_Login)


def Admin_Error_500(request):
    return render(request, "myAdmin/error-500.html")


def Admin_Error_404(request):
    return render(request, "myAdmin/error-404.html")


"""
def Admin_Chart(request):
    if 'EMmail_Id' in request.COOKIES and request.session.has_key('EMmail_Id'):
        return render(request, 'myAdmin/chartist.html')
    else:
        return redirect(Admin_Login)

def Admin_Form(request):
    return render(request, 'myAdmin/entry_record.html')

def Admin_Register(request):
    return render(request, 'myAdmin/register.html')

def Admin_Table(request):
    return render(request, 'myAdmin/table.html')
"""


def Admin_Login(request):
    return render(request, "myAdmin/login.html")


def Admin_Category(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):
        cur.execute("SELECT * FROM category_mst")
        data = cur.fetchall()
        cat = {"categories": data}
        return render(request, "myAdmin/view-category.html", cat)
    else:
        return redirect(Admin_Login)


def Chat(request):
    return render(request, "myAdmin/view-chat.html")


def Category_form(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):
        return render(request, "myAdmin/add-category_form.html")
    else:
        return redirect(Admin_Login)


"""

def Category_form_edit(request):
    return render(request, 'myAdmin/edit-category_form.html')
"""


def Category_Add_Process(request):
    if request.method == "POST":
        # print(request.POST)
        category_name = request.POST["cat_name"]
        cur.execute(
            "INSERT INTO `category_mst`(`Category_Name`) VALUES ('{}')".format(
                category_name
            )
        )
        conn.commit()
        return redirect(Category_form)
    else:
        return redirect(Category_form)


def Category_Edit(request, id):
    cur.execute("select * from `category_mst` where `category_id` = {}".format(id))
    data = cur.fetchone()
    return render(request, "myAdmin/edit-category_form.html", {"cat": data})


def Category_Update(request):
    if request.method == "POST":
        # print(request.POST)
        cat_id = request.POST["cat_id_txt"]
        cat_name = request.POST["cat_name_txt"]
        cur.execute(
            "update `category_mst` set `Category_Name` ='{}' where `Category_Id`='{}'".format(
                cat_name, cat_id
            )
        )
        conn.commit()
        return redirect(Admin_Category)
    else:
        return redirect(Admin_Category)


def Category_Delete(request, id):
    cur.execute("delete from `category_mst` where `Category_Id` = {}".format(id))
    conn.commit()
    return redirect(Admin_Category)


def Admin_Company(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):
        cur.execute("SELECT * FROM company_mst")
        data = cur.fetchall()
        comp = {"company": data}
        return render(request, "myAdmin/view-company.html", comp)
    else:
        return redirect(Admin_Login)


def Company_form(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):
        return render(request, "myAdmin/add-company_form.html")
    else:
        return redirect(Admin_Login)


def Company_Add_Process(request):
    if request.method == "POST":
        # company_id = request.POST['comp_id']
        company_name = request.POST["comp_name"]
        company_passwd = request.POST["comp_passwd"]
        company_type = request.POST["comp_type"]
        company_address = request.POST["comp_address"]
        company_email = request.POST["comp_email"]
        company_mob = request.POST["comp_mobile"]
        company_is_admin = request.POST["is_admin"]
        company_about = request.POST["about_comp"]
        company_website = request.POST["website"]

        myfile = request.FILES["comp_logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        logo = fs.url(filename)

        cur.execute(
            "INSERT INTO `company_mst`(`Password`,`Name`,`About_Company`,`Company_Type`,`Address`,`Email_Id`,`Mobile_Number`,`Logo`,`Website`,`IsAdmin`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                company_passwd,
                company_name,
                company_about,
                company_type,
                company_address,
                company_email,
                company_mob,
                logo,
                company_website,
                company_is_admin,
            )
        )
        conn.commit()
        return redirect(Company_form)
    else:
        return redirect(Company_form)


def Company_Edit(request, id):
    cur.execute("select * from `company_mst` where `Company_Id` = {}".format(id))
    data = cur.fetchone()
    return render(request, "myAdmin/edit-company_form.html", {"comp": data})


def Company_Update(request):
    if request.method == "POST":
        comp_id = request.POST["comp_id_txt"]
        comp_name = request.POST["comp_name_txt"]
        comp_type = request.POST["comp_type_txt"]
        comp_address = request.POST["comp_address_txt"]
        comp_email = request.POST["comp_email_txt"]
        comp_mobile = request.POST["comp_mobile_txt"]
        company_about = request.POST["about_comp"]
        company_website = request.POST["website"]

        myfile = request.FILES["comp_logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        logo = fs.url(filename)

        cur.execute(
            "update `company_mst` set `Name` ='{}', `Company_Type` ='{}', `Address` ='{}', `Email_Id` ='{}', `Mobile_Number` ='{}', `Website` ='{}', `About_Company` ='{}', `Logo`='{}'  where `Company_Id`='{}'".format(
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
        return redirect(Company_form)
    else:
        return redirect(Company_form)


def Company_Delete(request, id):
    cur.execute("delete from `company_mst` where `Company_Id` = {}".format(id))
    conn.commit()
    return redirect(Admin_Company)


def Admin_Payment(request):
    cur.execute(
        "select payment_mst.payment_id,company_mst.name,payment_mst.payment_details,payment_mst.payment_date,payment_mst.payment_time,payment_mst.payment_status from payment_mst, company_mst where payment_mst.company_id=company_mst.company_id and company_mst.isadmin=0;"
    )
    data = cur.fetchall()
    pay = {"payment": data}
    return render(request, "myAdmin/view-payment.html", pay)


def Admin_Applied(request):
    cur.execute(
        "select apply_mst.job_application_id, company_mst.name,seek_mst.name,job_mst.job_post_name, apply_mst.job_application_date,apply_mst.job_application_time,apply_mst.job_application_status from apply_mst,job_mst,seek_mst,company_mst where apply_mst.company_id=company_mst.company_id and apply_mst.job_seeker_id=seek_mst.job_seeker_id and apply_mst.job_post_id=job_mst.job_post_id and company_mst.isadmin=0;"
    )
    data = cur.fetchall()
    app = {"apply": data}
    return render(request, "myAdmin/view-applied.html", app)


def Seeker_form(request):
    return render(request, "myAdmin/add-seeker_form.html")


def Admin_JobSeekers(request):
    cur.execute("SELECT * FROM seek_mst")
    data = cur.fetchall()
    seek = {"seeker": data}
    return render(request, "myAdmin/view-job_seeker.html", seek)


def JobSeeker_Add_Process(request):
    if request.method == "POST":
        jobseeker_id = request.POST["js_id"]
        jobseeker_name = request.POST["js_name"]
        jobseeker_passwd = request.POST["js_passwd"]
        jobseeker_dob = request.POST["js_dob"]
        jobseeker_address = request.POST["js_address"]
        jobseeker_email = request.POST["js_email"]
        jobseeker_gender = request.POST["js_gender"]
        jobseeker_mob = request.POST["js_mobile"]

        myfile = request.FILES["js_resume"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        myfile1 = request.FILES["js_photo"]
        fs1 = FileSystemStorage()
        filename1 = fs1.save(myfile1.name, myfile1)
        profile_pic = fs1.url(filename1)

        cur.execute(
            # "INSERT INTO `seek_mst`(`Password`,`Name`,`Address`,`Date_Of_Birth`,`EMail_Id`,`Gender`,`Mobile_Number`,`Resume`,`Profile_Photo`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            "INSERT INTO `seek_mst`(`Password`,`Name`,`Address`,`Date_Of_Birth`,`EMail_Id`,`Gender`,`Mobile_Number`,`Resume`,`Profile_Photo`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                jobseeker_passwd,
                jobseeker_name,
                jobseeker_address,
                jobseeker_dob,
                jobseeker_email,
                jobseeker_gender,
                jobseeker_mob,
                uploaded_file_url,
                profile_pic,
            )
        )
        conn.commit()
        return redirect(Seeker_form)
    else:
        return redirect(Seeker_form)


def JobSeeker_Edit(request, id):
    cur.execute("select * from `seek_mst` where `Job_Seeker_Id` = {}".format(id))
    data = cur.fetchone()
    return render(request, "myAdmin/edit-seeker_form.html", {"seek": data})


def JobSeeker_Update(request):
    if request.method == "POST":
        jobseeker_id = request.POST["js_id_txt"]
        jobseeker_name = request.POST["js_name_txt"]
        # jobseeker_passwd = request.POST['js_passwd_txt']
        jobseeker_dob = request.POST["js_dob_txt"]
        jobseeker_address = request.POST["js_address_txt"]
        jobseeker_email = request.POST["js_email_txt"]
        # jobseeker_gender = request.POST['js_gender_txt']
        jobseeker_mob = request.POST["js_mobile_txt"]

        myfile = request.FILES["js_resume"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        myfile1 = request.FILES["js_photo"]
        fs1 = FileSystemStorage()
        filename1 = fs1.save(myfile1.name, myfile1)
        profile_pic = fs1.url(filename1)

        cur.execute(
            "update `seek_mst` set `Name` ='{}', `Address` ='{}', `Date_Of_Birth` ='{}', `EMail_Id` ='{}', `Mobile_Number` ='{}',`Resume`='{}',`Profile_Photo`='{}' where `Job_Seeker_Id`='{}'".format(
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
        return redirect(Admin_JobSeekers)
    else:
        return redirect(Admin_JobSeekers)


def JobSeeker_Delete(request, id):
    cur.execute("delete from `seek_mst` where `Job_Seeker_Id` = {}".format(id))
    conn.commit()
    return redirect(Admin_JobSeekers)


def Admin_Job(request):
    cur.execute(
        "SELECT job_mst.Job_Post_Id, company_mst.Name, category_mst.Category_Name, City.City_Name, job_mst.Job_Post_Name, job_mst.Job_Post_Type, job_mst.Job_Post_Description, job_mst.Job_Post_Responsibility, job_mst.Job_Post_Educational_Qualification, job_mst.Job_Post_Experience, job_mst.Job_Post_Salary FROM City INNER JOIN (category_mst INNER JOIN (company_mst INNER JOIN job_mst ON company_mst.Company_Id = job_mst.Company_Id) ON category_mst.Category_Id = job_mst.Category_Id) ON City.City_Id = job_mst.City_Id and company_mst.isadmin=0 order by job_mst.job_post_id"
    )
    data = cur.fetchall()
    job = {"jobdata": data}
    return render(request, "myAdmin/view-job.html", job)


def Job_Delete(request, id):
    # print(id)
    cur.execute("delete from `job_mst` where `Job_Post_Id` = {}".format(id))
    conn.commit()
    return redirect(Admin_Job)


def Admin_Login(request):
    if request.method == "POST":
        print(request.POST)
        admin_email = request.POST["admin_email"]
        admin_pass = request.POST["admin_password"]
        cur.execute(
            "select * from `company_mst` where `EMail_Id` = '{}' and `Password` = '{}'".format(
                admin_email, admin_pass
            )
        )
        data = cur.fetchone()

        if data is not None:
            if len(data) > 0:
                # Fetch Data
                admin_db_id = data[0]
                admin_db_email = data[1]
                print(admin_db_id)
                print(admin_db_email)
                # Session Create Code
                request.session["Company_Id"] = admin_db_id
                request.session["EMmail_Id"] = admin_db_email
                # Session Create Code
                # Cookie Code
                response = redirect(Admin_Homepage)
                response.set_cookie("Company_Id", admin_db_id)
                response.set_cookie("EMmail_Id", admin_db_email)
                return response
                # Cookie Code
            else:
                return render(request, "myAdmin/login.html")
        return render(request, "myAdmin/login.html")

    # return redirect(dashboard)
    else:
        return render(request, "myAdmin/login.html")


def dashboard(request):
    if "EMmail_Id" in request.COOKIES and request.session.has_key("EMmail_Id"):

        admin_emails = request.session["EMmail_Id"]
        admin_emailc = request.COOKIES["EMmail_Id"]

        print("Session is  " + admin_emails)
        print("Cookie is  " + admin_emailc)

        return render(Admin_Homepage)
    else:
        return redirect(Admin_Login)


def logout(request):

    # del request.session['admin_id']
    # del request.session['admin_email']
    response = redirect(Admin_Login)
    response.delete_cookie("EMmail_Id")
    response.delete_cookie("Company_Id")
    return response
