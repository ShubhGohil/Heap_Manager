from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import datetime

# Create your views here.

import mysql.connector as sqlcon
conn = sqlcon.connect(host='localhost', user='shubh', passwd='shubh123', auth_plugin='mysql_native_password', database='MedicalStore')
cur = conn.cursor()

#Home Page
def index(request):
	try:
		params = []
		query = "SELECT COUNT(emp_id) FROM employee"
		cur.execute(query)
		count_of_employee = int(cur.fetchall()[0][0])
		params.append(count_of_employee)
		
		query = "SELECT exp_date from stock"
		cur.execute(query)
		result = cur.fetchall()
		count = 0

		for date in result:
			days = (date[0] - datetime.date.today()).days
			if days<= 30:
				count = count + 1 
		params.append(count)
		
		query = "SELECT med_name from medicine"
		cur.execute(query)
		res = cur.fetchall()
		params.append(res)
		
		date = datetime.date.today()
		query=f"SELECT SUM(price) from bill where bill_date=\'{date}\'"
		cur.execute(query)
		res = cur.fetchall()
		params.append(res[0][0])
		
		return render(request, 'store/index.html', {'params': params})

	except Exception as e:
		print(e)
		return render(request, 'store/index.html', {'params': [0,0]})
				

#Staff
def staff_register(request):
	if request.method == 'POST':
		try:
			firstname = request.POST["firstname"]
			lastname = request.POST["lastname"]
			name = firstname + " " + lastname
			
			gender = request.POST["gender"]
			age = int(request.POST["age"])
			salary = int(request.POST["salary"])
			query = f"SELECT COUNT(emp_id) FROM employee WHERE emp_name=\'{name}\' and emp_gender=\'{gender}\' and emp_age={age} and emp_salary={salary}"
			cur.execute(query)
			count = int(cur.fetchall()[0][0])
			if not count:				
				cur.execute("INSERT INTO employee (emp_name, emp_gender, emp_age, emp_salary) VALUES (\'{}\', \'{}\', {}, {})". format(name, gender, age, salary))
				conn.commit()
				
				messages.success(request, 'Record Saved Successfully !!!')
				return redirect("store:staff-all")
			else:
				messages.error(request,'Record Already Exists!!!')
				return redirect('store:staff-all')
			
		except Exception as e:
			print(e)
			messages.error(request,"Some Error Occured !!!")
			return redirect('store:staff-all')
	
	else:
		return render(request, 'store/staff_form.html')
		
def staff_all(request):
	cur.execute('SELECT * FROM employee;')
	records = cur.fetchall()
	return render(request, 'store/staff_all.html', {'records':records})


def staff_delete(request, pk):
	try:
		query = f'DELETE FROM employee WHERE emp_id={pk}'
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Deleted Successfully !!!")
	except:
		messages.error(request, "Can't Delete Record !!!")
	return redirect('store:staff-all')


def staff_update(request, pk):
	try:
		query = f'SELECT * FROM employee WHERE emp_id={pk}'
		cur.execute(query)
		val = cur.fetchone()
	except:
		messages.error(request, "Can't Update Record !")
		return redirect('store:staff-all')
		
	emp={
		'emp_id':val[0],
		'firstname':val[1].split()[0],
		'lastname':val[1].split()[1],
		'gender':val[2],
		'age':val[3],
		'salary':val[4]
	}

	if request.method == 'POST':
		emp_id = request.POST['emp_id'] 
		name = request.POST['firstname'] + " " + request.POST['lastname']
		gender = request.POST['gender']
		age = int(request.POST['age'])
		salary = int(request.POST['salary'])
		query = f"UPDATE employee SET emp_name = '{name}', emp_gender = '{gender}', emp_age = {age}, emp_salary = {salary} where emp_id = {emp_id};"	
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Updated Successfully !")
		return redirect('store:staff-all')

	return render(request, 'store/staff_update.html',{'emp':emp})

	
#Stock	
def stock_register(request):
	if request.method=='POST':
		medname = request.POST['name']
		quantity = request.POST['quantity']
		price = request.POST['price']
		supplier = request.POST['supplier']
		mfg_date = request.POST['mfg_date']
		exp_date = request.POST['exp_date']
		arr_date = request.POST['arr_date']
		
		try:
			query=f"SELECT med_id FROM medicine WHERE med_name=\'{medname}\'"
			cur.execute(query)
			medid=cur.fetchall()[0][0]
		except:
			messages.error(request, "Medicine Not Registered ! Please Register First From /register/medicine .")
			return redirect("store:medicine-register")
			
		try:
			query=f"SELECT supplier_id FROM supplier WHERE supplier_name=\'{supplier}\'"
			cur.execute(query)
			supid=cur.fetchall()[0][0]
		except:
			messages.error(request, "Supplier Not Registered ! Please Register First From /register/supplier .")
			return redirect("store:supplier-register")
						
		query = f"INSERT INTO stock (quantity, price, mfg_date, exp_date, stock_arrival_date, supplier_id, med_id) VALUES ({quantity}, {price}, \'{mfg_date}\', \'{exp_date}\', \'{arr_date}\', {supid}, {medid})"
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Registered Successfully !")
		return redirect("store:stock-all")
	else:
		return render(request, 'store/stock_form.html')
	
def stock_all(request):
	try:
		cur.execute('SELECT stock_id, quantity, price, mfg_date, exp_date, stock_arrival_date, med_name, supplier_name FROM stock NATURAL JOIN medicine NATURAL JOIN supplier ORDER BY exp_date;')
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:stock-all')
	
	return render(request, 'store/stock_all.html', {'records':records})
	

#Bill
def bill_register(request):
	if request.method=='POST':
		value = []
		customername = request.POST.getlist('name')[0]
		print(customername)
		medname = request.POST.getlist('medicine')
		qua = request.POST.getlist('quantity')
		try:
			for name in request.POST.getlist('medicine'):
				query=f"SELECT med_price FROM medicine where med_name=\'{name}\'" 
				cur.execute(query)
				res = cur.fetchall()
				value.append(res[0][0])
				
			count = 0
			for q in request.POST.getlist('quantity'):
				value[count] *= int(q)
				count = count + 1
			
			for i in range(len(value)):
				query=f"INSERT INTO bill (cust_name, med_name, quantity, price) VALUES (\'{customername}\', \'{medname[i]}\', {qua[i]}, {value[i]})"
				cur.execute(query)
				conn.commit()
			messages.success(request, "Bill Generated!!!")
			return redirect('store:store-home')
		except Exception as e:
			print(e)
			messages.error(request, "Some Error Occured!!!")
			return redirect('store:store-home')
		
	return render(request, 'store/index.html')
	
def bill_all(request):
	query = 'SELECT * FROM bill;'
	try:
		cur.execute(query)
	except:
		messages.error(request, "Some Error Occurred !!!")
		return redirect("store:store-home")
	
	records = cur.fetchall()

	return render(request, 'store/bill_all.html', {'records':records})
	
	
#Medicine
def medicine_register(request):
	if request.method=='POST':
		try:
			medicinename = request.POST["medname"]
			price = request.POST['price']
			
			query = f"SELECT COUNT(med_id) FROM medicine WHERE med_name=\'{medicinename}\'"
			cur.execute(query)
			count = int(cur.fetchall()[0][0])
			
			if not count:				
				cur.execute("INSERT INTO medicine (med_name, med_price) VALUES (\'{}\', {})". format(medicinename, price))
				conn.commit()
				messages.success(request, "Record Saved Successfully !!!")
				return redirect('store:medicine-all')
			else:
				messages.error(request, "Record Already Exixts !!!")
				return redirect('store:medicine-all')
			
		except Exception as e:
			print(e)
			messages.error(request, "Some Error Occurred !!!")
			return redirect('store:medicine-all')

	else:
		return render(request, 'store/medicine_form.html')

def medicine_all(request):
	query = 'SELECT * FROM medicine;'
	try:
		cur.execute(query)
	except:
		messages.error(request, "Some Error Occurred !!!")
		return redirect("store:medicine-all")
	
	records = cur.fetchall()

	return render(request, 'store/medicine_all.html', {'records':records})


def medicine_delete(request, pk):
	query = f'DELETE FROM medicine WHERE med_id = {pk}'
	try:
		cur.execute(query)
		conn.commit()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect("store:medicine-all")
	messages.success(request,"Record Saved Successfully !")
	return redirect('store:medicine-all')

def medicine_update(request, pk):
	query = f'SELECT * FROM medicine WHERE med_id = {pk}'
	try:
		cur.execute(query)
		med = cur.fetchone()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:medicine-all')

	if request.method == 'POST':
		name = request.POST['medname']
		price = request.POST['medprice']
		try:
			query = f"update medicine set med_name = '{name}', med_price = {price} where med_id = {pk};"
			print(query)
			cur.execute(query)
			conn.commit()
			messages.success(request, 'Record Successfully Updated !')
			return redirect('store:medicine-all')
		except:
			messages.error(request, 'Some Error Occurred !')
			return redirect('store:medicine-all')

	return render(request, 'store/medicine_update.html', {'med':med})

#Supplier
def supplier_register(request):
	if request.method == 'POST':
		try:
			suppliername = request.POST["supname"]
			city = request.POST["city"]			
			pincode = request.POST["pincode"]

			query = f"SELECT COUNT(supplier_id) FROM supplier WHERE supplier_name=\'{suppliername}\' and supplier_city=\'{city}\' and city_pincode={pincode}"
			cur.execute(query)
			count = int(cur.fetchall()[0][0])
			if not count:	
				cur.execute("INSERT INTO supplier (supplier_name, supplier_city, city_pincode) VALUES (\'{}\', \'{}\', {})". format(suppliername, city, pincode))
				conn.commit()
				messages.success(request, "Record Saved Successfully !!!")
				return redirect('store:supplier-all')
			else:
				messages.error(request, "Record Already Exists !!!")
				return redirect('store:supplier-all')
			
		except Exception as e:
			print(e)
			messages.error(request, "Some Error Occurred !!!")
			return redirect('store:supplier-all')
	
	else:
		return render(request, 'store/supplier_form.html')

def supplier_all(request):
	query = 'SELECT * FROM supplier;'
	try:
		cur.execute(query)
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred !!!")
		return redirect('store:supplier-all')
	
	return render(request, 'store/supplier_all.html', {'records':records})


def supplier_delete(request, pk):
	query = f'DELETE FROM supplier WHERE supplier_id = {pk};'
	try:
		cur.execute(query)
		conn.commit()
	except:
		messages.error(request, "Can't Delete Record !!!")
		return redirect('store:supplier-all')
	
	return redirect('store:supplier-all')


def supplier_update(request, pk):
	query = f'SELECT * FROM supplier WHERE supplier_id={pk}'
	#print(query)
	try:
		cur.execute(query)
		supplier = cur.fetchone()
	except:
		messages.error(request, "Some Error Occurred !!!")
		return redirect('store:supplier-all')
	#print(supplier)
	if request.method == 'POST':
		supplier_id = request.POST['supplier_id']
		suppliername = request.POST["supname"]
		city = request.POST["city"]			
		pincode = request.POST["pincode"]
		query = f"update supplier set supplier_name = '{suppliername}', supplier_city = '{city}', city_pincode = {pincode} where supplier_id = {supplier_id};"

		try:
			cur.execute(query)
			conn.commit()
			messages.success(request, "Record Updated Successfully !!!")
			return redirect('store:supplier-all')
		except:
			messages.error(request, "Some Error Occurred !!!")
			return redirect('store:supplier-all')

	return render(request, 'store/supplier_update.html', {'supplier':supplier})
	
def info(request):
	return render(request, 'store/info.html')

