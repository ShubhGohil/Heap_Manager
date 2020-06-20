/*This is a data structure which keeps a record of various memory allocations and  deallocations.*/

#include<stdio.h>
#include<unistd.h>
#include<string.h>
#define MEM 1024


typedef struct used_memory_manager {
	int size;                    //stores the size of block
	void *curr_add;              //stores the address of block
	int no_of_block;             //stores the block number (since their will be two blocks of same size)
	int row;                     //stores row in which it is stores in the data structure
}block;

typedef struct free_memory_manager {
	int size;
	void *curr_add;
	int no_of_block;
	int row;
}fblock;

typedef struct data_manager {
	block s[5000][5000]; //stores the malloced blocks
	fblock fs[5000][5000]; //stores the free blocks 
	int r, c[5000]; //r stores the total rows of both blocks, c[r] stores total colums in rth row of the freed block
	int col_s[5000]; //stores the total colums of malloced blocks
	int mem_allocated[5000]; // it stores total memory called
}manager;


void shiftright(manager *m, int row, int column);
int split_blocks(manager *m, int row_info, int col_info, size_t size, size_t tsize, void *r, int shift_enabler);
void *initialize(manager *m, size_t size);
int *block_avail(manager *m, size_t size, int *arr);
void manage_manager(manager *m, void *p, size_t tsize, size_t size);
void *set_manager(manager *m, size_t size);
block fremove(manager *m, block *b, int row, int column);
void insert(manager *m, block *b);
void *assign(manager *m, size_t size);
block *remove_allocated(manager *m, block *b, void *p);
void merge_block(manager *m, int row_info);
void finsert(manager *m, block *b);
int free_block_identifier(manager *m);

