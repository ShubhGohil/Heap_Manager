from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime

# Create your views here.

import mysql.connector as sqlcon
conn = sqlcon.connect(host='localhost', user='shubh', passwd='shubh123', auth_plugin='mysql_native_password', database='MedicalStore')
cur = conn.cursor()


def index(request):
	try:
		params = []
		med = []
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
		
		return render(request, 'store/index.html', {'params': params})

	except Exception as e:
		print(e)
		return render(request, 'store/index.html', {'params': [0,0]})
				

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
				
				return HttpResponse('Record Successfully Saved!!!')
			else:
				return HttpResponse('Record Already Exists!!!')
			
		except Exception as e:
			print(e)
			return HttpResponse('Some Error Occured!!!')
	
	else:
		return render(request, 'store/staff_form.html')
		
def staff_all(request):
	cur.execute('SELECT * FROM employee;')
	records = cur.fetchall()
	return render(request, 'store/staff_all.html', {'records':records})


def staff_delete(request, pk):
	query = f'DELETE FROM employee WHERE emp_id={pk}'
	cur.execute(query)
	conn.commit()
	return redirect('store:staff-all')


def staff_update(request, pk):
	
	query = f'SELECT * FROM employee WHERE emp_id={pk}'
	cur.execute(query)
	val = cur.fetchone()
	emp={
		'emp_id':val[0],
		'firstname':val[1].split()[0],
		'lastname':val[1].split()[1],
		'gender':val[2],
		'age':val[3],
		'salary':val[4]
	}
	print(emp)
	if request.method == 'POST':
		emp_id = request.POST['emp_id'] 
		name = request.POST['firstname'] + " " + request.POST['lastname']
		gender = request.POST['gender']
		age = int(request.POST['age'])
		salary = int(request.POST['salary'])
		query = f"UPDATE employee SET emp_name = '{name}', emp_gender = '{gender}', emp_age = {age}, emp_salary = {salary} where emp_id = {emp_id};"	
		cur.execute(query)
		conn.commit()
		return redirect('store:staff-all')

	return render(request, 'store/staff_update.html',{'emp':emp})

		
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
			return HttpResponse("This medicine is not registered. Please register first from /register/medicine.")
			
		try:
			query=f"SELECT supplier_id FROM supplier WHERE supplier_name=\'{supplier}\'"
			cur.execute(query)
			supid=cur.fetchall()[0][0]
		except:
			return HttpResponse("This supplier is not registered. Please register first from /register/supplier.")
						
		query = f"INSERT INTO stock (quantity, price, mfg_date, exp_date, stock_arrival_date, supplier_id, med_id) VALUES ({quantity}, {price}, \'{mfg_date}\', \'{exp_date}\', \'{arr_date}\', {supid}, {medid})"
		cur.execute(query)
		conn.commit()
		return HttpResponse("Record Saved!!!")
	#while accepeting date change the format
	else:
		return render(request, 'store/stock_form.html')
		
def stock_all(request):
	cur.execute('SELECT * FROM stock')
	records = cur.fetchall()
	return render(request, 'store/stock_all.html', {'records':records})
	

def bill_register(request):
	if request.method=='POST':
		value = []
		customername = request.POST['name'][0]
		medname = request.POST.getlist('medicine')
		qua = request.POST.getlist('quantity')
		try:
			for name in request.POST.getlist('medicine'):
				query=f"SELECT price FROM medicine where med_name=\'{name}\'" 
				cur.execute(query)
				res = cur.fetchall()
				value.append(res[0][0])
				
			count = 0
			for q in request.POST.getlist('quantity'):
				value[count] *= int(q)
				count = count + 1
			
			for i in len(value):
				query=f"INSERT INTO bill (cust_name, med_name, quantity, price) VALUES (\'{customername}\', \'{medname[i]}\', {qua[i]}, {value[i]}))"
				cur.execute(query)
				conn.commit()
				return HttpResponse("Bill generated!!!")
		except:
			return HttpResponse("Medicine out of stock!!!")
			
		#query = f"SELECT price FROM medicine where med_name=\'{}\'"
		
	return render(request, 'store/index.html')
	
def medicine_register(request):
	if request.method=='POST':
		try:
			medicinename = request.POST["medname"]
			query = f"SELECT COUNT(med_id) FROM medicine WHERE med_name=\'{medicinename}\'"
			cur.execute(query)
			count = int(cur.fetchall()[0][0])
			if not count:				
				cur.execute("INSERT INTO medicine (med_name) VALUES (\'{}\')". format(medicinename))
				conn.commit()
				
				return HttpResponse('Record Successfully Saved!!!')
			else:
				return HttpResponse('Record Already Exists!!!')
			
		except Exception as e:
			print(e)
			return HttpResponse('Some Error Occured!!!')

	else:
		return render(request, 'store/medicine_form.html')

#def supplier_

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
				
				return HttpResponse('Record Successfully Saved!!!')
			else:
				return HttpResponse('Record Already Exists!!!')
			
		except Exception as e:
			print(e)
			return HttpResponse('Some Error Occured!!!')
	
	else:
		return render(request, 'store/supplier_form.html')

