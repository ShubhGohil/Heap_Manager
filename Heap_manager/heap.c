#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"manager.h"
#include"heap.h"

manager m; // declares a manager varialble.
int i = 0; //It is used when a function is called for the first time.


void *mmalloc(size_t size) {
	void *temp, *p;
	if(size <= 0) {
		return NULL;
	}	
	if(i == 0) {
		temp = initialize(&m, size);
		p = temp;
		i++;
	}
	p = assign(&m, size);
	return p;
}

void *ccalloc(size_t multiplier, size_t size) {
	size_t annual_size = multiplier*size;
	void *p;
	p = mmalloc(annual_size);
	memset(p, 0, annual_size);
	return p;
}

void ffree(void *p) {
	block b, *b1;
	int a, j = 0, sum = 0;
	if(p == NULL) {
		return;
	}
	b1 = remove_allocated(&m, &b, p);
	finsert(&m, b1);
	a = free_block_identifier(&m);
	p = NULL;
	if(a == 1) {
		while(j < m.r) {
			sum += m.mem_allocated[j];
			j++;
		}
		sbrk(0 - sum);
		i = 0;
	}
	return;
}


void *rrealloc(void *p, size_t size) {
	block b, *b1;
	void *temp;
	int mem_size, i = 0, j = 0;
	if(size <= 0) {
		return NULL;
	}
	if(size == 0 && p != NULL) {
		ffree(p);
		return NULL;
	}
	else {
		temp = p;
		p = mmalloc(size);
		while(i < m.r) {
			while(j < m.c[i]) {
				if(m.s[i][j].curr_add == temp) {
					mem_size = m.s[i][j].size;
					break;
				}
				else {
					j++;
				}
			}
			j = 0;
			i++;
		}
		if(p != NULL) {
			memcpy(p, temp, mem_size);
			b1 = remove_allocated(&m, &b, temp);
			finsert(&m, b1);
		}
		return p;
	}
}

