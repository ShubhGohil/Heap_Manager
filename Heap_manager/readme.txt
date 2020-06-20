Project Name - Heap Manager

Name - Shubh Bharat Gohil

MIS No. - 111803052

Brief :-
	This is the implementation of basic dynamic memory allocation functions like malloc, calloc, free and realloc. The function which requests memory from the OS is sbrk() which is a system call. This function gives a memory chunck of requested size having continuos memory locations.
	I have used 2-D array of structures which stores the starting address and size of the memory blocks that are allocated or free. This memory manager uses buddy allocator to provide required memory blocks to the users as per their requirements.The blocks provided for data allocation are given on the basis of best fit algorithm which searches for the block closely available with the size requested.
	Talking about the working of the manager it has two different 2-D arrays of structure one of which strores blocks with free memory and the other with allocated memory. Initially sbrk() calls a memory block of 1024 bytes or in the power of 2 greater than 1024 bytes. This information is initialized in the free data structure. Whenever user requests some memory the blocks are split into halves upto the block with can closely fit the request. Thenthe block is removed from the free array and is inserted in the allocated array.Similarly the process of malloc and calloc works.
	If user frees the memory then the block with same is removed and again inserted in the free array. Also once inserted, it checks if the block with same size and adjacent memory is present next or before the block. If present it merges the blocks.
	When realloc is called it searches for the new block of reqired size, if found copies the data to the new address and and frees the preevious allocated block.
