# Projects

This directory contains 5 various mini-projects.

+ [Doctor Appointment System](#doctor-appointment-system)
+ [Heap Manager](##heap-manager)
+ [Medical Store](##medical-store)
+ [Numeral Recognition](##numeral-recognition)
+ [SpotifyAPI](##spotifyAPI)


## Doctor Appointment System

It is a web application built using MERN stack which is useful booking an appointment to the patient for any registered doctor. A patient/doctor has to register to the system and then login to use the system. Admin does not have register feature, there details should be entered directly in the database and then can login from the login page. Local-Strategy module is used to maintain session, and for security purpose. Information of all the modules used can be obtained from the package.json file. The system has three users,
1. Patient
    Features:
    1) Book an appointment
    2) Cancel an appointment
    3) Update Profile
    4) Dashboard to display the profile and upcoming appointments
    5) Remove account

2. Doctor
    Features:
    1) Make schedule (i.e select date and timeslots for that day)
    2) Update Profile

3. Admin
    Features:
    1) Remove registered Patients or Doctors
    2) Update profile

> The doctor can make a schedule for himself upto 3 days only, similarly the patient is able to book an appointment upto 3 days and for the doctor who has already setup his schedule.

To run the app, run the command in your terminal,
```
node app
```

## Heap Manager
It is program which to allocate, deallocate and keep a record of free memory(heap memory). Is is built using C language. The Data Structure used for the book keeping of various memory blocks is spare matrix. Custom malloc, calloc and free functions are used to allocate and free a memory during runtime. The memory blocks are allocated of the size in power of 2. The algorithm used to organize the blocks is buddy allocater and are allocated by first fit mechanism.

This is the implementation of basic dynamic memory allocation functions like malloc, calloc, free and realloc. The function which requests memory from the OS is sbrk() which is a system call. This function gives a memory chunck of requested size having continuos memory locations.

The Data Structure used for the book keeping of various memory blocks is spare matrix, which stores the starting address and size of the memory blocks that are allocated or free. This memory manager uses buddy allocator to provide required memory blocks to the users as per their requirements.The blocks provided for data allocation are given on the basis of best fit algorithm which searches for the block closely available with the size requested.

Talking about the working of the manager it has two different 2-D arrays of structure one of which stores blocks with free memory and the other with allocated memory. Initially sbrk() calls a memory block of 1024 bytes or in the power of 2 greater than 1024 bytes. This information is initialized in the free data structure. Whenever user requests some memory the blocks are split into halves upto the block with can closely fit the request. Then the block is removed from the free array and is inserted in the allocated array. Similarly the process of malloc and calloc works.

If user frees the memory then that block is removed from the allocated array and again inserted in the free array. Also once inserted, it checks if the block with same size and adjacent memory location is present next or before the block. If present it merges the blocks.

When realloc is called it searches for the new block of reqired size, if found copies the data to the new address and frees the previous allocated block.

To run the program, type in your terminal,
```
make project
```

## Medical Store
This is a project which is can be used in the medical store to keep a record of the import of stock, suppliers, rate of medicine and sale of medicine. It is built using Django and MySQL. You must have a SQL database already setup.

To run the app, run this command in your terminal,
```
python manage.py runserver
```
