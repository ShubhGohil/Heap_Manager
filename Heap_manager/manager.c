#include"manager.h"

int *array; // used to store the output of block_avail function. It tells if their is a block available. 
int store[3]; // used to store the block availiablity.

/*This function is used to shift the block in free blocks array to their right*/
void shiftright(manager *m, int row, int column) {
	int i, j, k;
	i = row;
	j = column;
	k = m->c[i];
	while(k>j) {
		m->fs[i][k] = m->fs[i][k-1];
		k--;
	}
}

/*
 *This funtion is used to split the blocks having same size,
 *into blocks of half of their sizes.
 */
int split_blocks(manager *m, int row_info, int col_info, size_t size, size_t tsize, void *r, int shift_enabler) {
	int i, j;
	i = row_info;
	j = col_info;
	while(size <= tsize/2) {
		if(shift_enabler == 1) {
			shiftright(m, i, j);
		}
		tsize /= 2;
		m->fs[i][j].curr_add = r + tsize;
		m->fs[i][j+1].curr_add = r;
		m->fs[i][j].size = tsize;
		m->fs[i][j+1].size = tsize;
		m->fs[i][j].row = i;
		m->fs[i][j+1].row = i;
		m->fs[i][j].no_of_block = 1;
		m->fs[i][j+1].no_of_block = 2;
		j++;
		m->c[i]++;
	}
	return j;
}


/*
 *This function works only once in the beginning to initialize the values of structure
 *and take first chunck of memory.
 */
void *initialize(manager *m, size_t size) {
	int a, multiple = 1;
	void *q;
	void *p = sbrk(0);
	if(p == (void *) -1) {
		return NULL;
	}
	while(multiple*MEM <= size) {
		multiple *= 2;	
	}
	p = sbrk(multiple*MEM);
	if(p == (void *) -1) {
		return NULL;
	}
	q = sbrk(0);
	if(q == (void *) -1) {
		return NULL;
	}
	for(a=0; a < 5000; a++) {
		m->fs[0][a].curr_add = NULL;
		m->fs[0][a].size = 0;
		m->fs[0][a].no_of_block = 0;
		m->fs[0][a].row = 0;
		m->s[0][a].curr_add = NULL;
		m->s[0][a].size = 0;
		m->s[0][a].no_of_block = 0;
		m->s[0][a].row = 0;
		m->c[a] = 0;
		m->col_s[a] = 0;
	}
	m->fs[0][0].curr_add = p;
	m->fs[0][0].size = multiple*MEM;
	m->fs[0][0].row = 0;
	m->fs[0][0].no_of_block = 1;
	m->c[0] = 1;
	split_blocks(m, 0, 0, size, multiple*MEM, p, 0);
	m->r = 1;
	//TMEM = multiple*MEM;
	m->mem_allocated[0] = multiple*MEM;
	return p;
}

/*
 *This funtion checks if their is a block of size,
 *which can satify the condition available.
 */
int *block_avail(manager *m, size_t size, int *arr) {
	int a = 0, i;
	int multiplier = 1;
	while(size > 2*multiplier) {
		multiplier *= 2;
	}
	while(a < m->r) {
		for(i=0; i < m->c[a]; i++) {
			if((2*multiplier) < m->fs[a][i].size) {
				;
			}
			else if((2*multiplier) == m->fs[a][i].size) {
				if(m->fs[a][i].no_of_block == 1) {
					if(m->fs[a][i].size == m->fs[a][i+1].size) {
						arr[0] = a;
						arr[1] = i+1;
						arr[2] = 1;
						return arr;
					}
					else {
						arr[0] = a;
						arr[1] = i;
						arr[2] = 1;
						return arr;
					}
				}
				else if(m->fs[a][i].no_of_block == 2) {
					arr[0] = a;
					arr[1] = i;
					arr[2] = 1;
					return arr;
				}
			}
			else {
				if((2*multiplier) > m->fs[a][0].size) {
					a++;
					if(a >= m->r) {
						break;
					}
					i = -1;
				}
				else {
					arr[0] = a;
					arr[1] = split_blocks(m, a, i-1, size, m->fs[a][i-1].size, m->fs[a][i-1].curr_add, 1);
					arr[2] = 1;
					return arr;
				}
			}
		}
		a++;
	}
	arr[0] = 0;
	arr[1] = 0;
	arr[2] = 0;
	return arr;
}


/*This function sets the initial value of the chunk in the data structure.*/
void manage_manager(manager *m, void *p, size_t tsize, size_t size) {
	m->fs[(m->r)-1][0].curr_add = p;
	m->fs[(m->r)-1][0].size = tsize;
	m->fs[(m->r)-1][0].row = (m->r)-1;
	m->fs[(m->r)-1][0].no_of_block = 1;
	m->c[(m->r)-1] = 1;
	split_blocks(m, (m->r)-1, 0, size, m->mem_allocated[(m->r)-1], p, 0);
	return;
}

/*
 *This function sets the pre conditional values of the data structure,
 *apart from the first call.
 */
void *set_manager(manager *m, size_t size) {
	void *q, *p;
	int multiple = 1, i;
	for(i=0; i<5000; i++) {
		m->fs[m->r][i].curr_add = NULL;
		m->fs[m->r][i].size = 0;
		m->fs[m->r][i].no_of_block = 0;
		m->fs[m->r][i].row = 0;
		m->s[m->r][i].curr_add = NULL;
		m->s[m->r][i].size = 0;
		m->s[m->r][i].no_of_block = 0;
		m->s[m->r][i].row = 0;

	}
	m->r++;
	while(multiple*MEM < size) {
		multiple *= 2;
	}
	p = sbrk(multiple*MEM);
	if(p == (void *) -1) {
		return NULL;
	}
	q = sbrk(0);
	if(q == (void *) -1) {
		return NULL;
	}
	//TMEM = multiple*MEM;
	m->mem_allocated[(m->r)-1] = multiple*MEM;
	manage_manager(m, p, multiple*MEM, size);
	return p;
}

/*
 *This function is used to remove the free block when allocated,
 *from the  free block's data structure.
 */
block fremove(manager *m, block *b, int row, int column) {
	int i, j;
	i = row;
	j = column;
	b->size = m->fs[row][column].size;
	b->curr_add = m->fs[row][column].curr_add;
	b->row = m->fs[row][column].row;
	b->no_of_block = m->fs[row][column].no_of_block;
	while(j!=m->c[i]) {
		m->fs[i][j].size = m->fs[i][j+1].size;
		m->fs[i][j].curr_add = m->fs[i][j+1].curr_add;
		m->fs[i][j].row = m->fs[i][j+1].row;
		m->fs[i][j].no_of_block = m->fs[i][j+1].no_of_block;
		j++;
	}
	m->c[i]--;
	return *b;
}

/*
 *This functin is used to add the block allocated to the used data structure,
 *after extracting from free block data structure.
 */
void insert(manager *m, block *b) {
	int i;
	i = b->row;
	m->s[i][m->col_s[i]].size = b->size;
	m->s[i][m->col_s[i]].curr_add = b->curr_add;
	m->s[i][m->col_s[i]].row = b->row;
	m->s[i][m->col_s[i]].no_of_block = b->no_of_block;
	m->col_s[i]++;
}


/*
 *This function is used to give the pointer address to the calling function
 *and hence allocate the memory.
 */
void *assign(manager *m, size_t size) {
	void *p;
	block b;
	array = block_avail(m, size, store);
	if(array[2] == 0) {
		p = set_manager(m, size);
			if(p == NULL) {
				return p;
			}
			else {
				array = block_avail(m, size, store);
				if(array[2] == 0) {
					return NULL;
				}
				else {
					p = m->fs[array[0]][array[1]].curr_add;
					b = fremove(m, &b, array[0], array[1]);
					insert(m, &b);
				}	
			}
	}
	else {
		p = m->fs[array[0]][array[1]].curr_add;
		b = fremove(m, &b, array[0], array[1]);
		insert(m, &b);
	}
	return p;
}

/*
 *This function is used to remove the allocate block
 *from used data structure when ever free is called.
 */
block *remove_allocated(manager *m, block *b, void *p) {
	int i = 0, j = 0 ,flag = 0;
	int k;
	while(i < m->r) {
		//printf("i = %d\n", i);
		while(j < m->col_s[i]) {
			//printf("j = %d\n", j);
			if(m->s[i][j].curr_add == p) {
				//printf("got it\n");
				b->curr_add = m->s[i][j].curr_add;
				b->size = m->s[i][j].size;
				b->row = m->s[i][j].row;
				b->no_of_block = m->s[i][j].no_of_block;
				k = j;
				while(k < m->col_s[i]) {
					m->s[i][k].curr_add = m->s[i][k+1].curr_add;
					m->s[i][k].size = m->s[i][k+1].size;
					m->s[i][k].row = m->s[i][k+1].row;
					m->s[i][k].no_of_block = m->s[i][k+1].no_of_block;
					k++;
					//printf("k = %d\n", k);
				}
				m->col_s[i]--;
				flag = 1;
				break;		
			}
			else {
				j++;
			}
		}
		if(flag == 1) {
			break;
		}
		i++;
		j = 0;
	}
	if(i == m->r) {
		b->curr_add = NULL;
		b->size = 0;
		b->row = 0;
		b->no_of_block = 0;
		return b;
	}
	return b;
}

/*
 *This fuction is used to join the blocks having same size and corresponig address,
 *to form a block which can store larger values.
 */
void merge_block(manager *m, int row_info) {
	int i = row_info, j, k = 0, flag = 0;
	while(k < m->c[i]) {
	//for(k=0; k < m->c[i]; k++)  {
		if(m->fs[i][k].size == m->fs[i][k+1].size) {
			if(m->fs[i][k].curr_add == ((m->fs[i][k+1].curr_add)+(m->fs[i][k].size))) {
				m->fs[i][k].curr_add = m->fs[i][k+1].curr_add;
				m->fs[i][k].size *= 2;
				m->fs[i][k].no_of_block = 2;
				m->c[i]--;
				j = k+1;
				flag = 1;
				while(j < m->c[i]+1) {
					m->fs[i][j].curr_add = m->fs[i][j+1].curr_add;
					m->fs[i][j].size = m->fs[i][j+1].size;
					m->fs[i][j].no_of_block = m->fs[i][j+1].no_of_block;
					j++;
				}
			}
			if(flag == 1) {
				k = k - 2;
				flag = 0;
			}
		}
		k++;
	}
	if(m->fs[i][0].size == m->mem_allocated[i]) {
		m->fs[i][0].no_of_block = 1;
		return;
	}
	else {
		return;
	}
}


/*This function is used to insert a block in free block data structure when freed.*/
void finsert(manager *m, block *b) {
	int i, j = 0, flag = 0;
	i = b->row;
	while(b->size < m->fs[i][j].size) {
		j++;
	}
	if(m->fs[i][j].size == b->size) {
		if(b->no_of_block < m->fs[i][j].no_of_block) {
			if(b->curr_add == (m->fs[i][j].curr_add + b->size)) {
				shiftright(m, i, j);
				flag = 1;
			}
			else {
				shiftright(m, i, j);
			}
		}
		else {
			if((b->curr_add + b->size) == m->fs[i][j].curr_add) {
				shiftright(m, i, j+1);
				flag = 1;
			}
			else {
				shiftright(m, i, j+1);
			}
			j++;
		}
	}
	else {
		shiftright(m, i, j);
	}
	m->fs[i][j].curr_add = b->curr_add;
	m->fs[i][j].size = b->size;
	m->fs[i][j].row = b->row;
	m->fs[i][j].no_of_block = b->no_of_block;
	m->c[i]++;
	if(flag == 1) {
		merge_block(m, i);
		return;
	}
	return;
}

/*This function keeps a track if every malloced memory is freed or not.*/
int free_block_identifier(manager *m) {
	int i = 0;
	while(i < m->r) {
		if(m->fs[i][0].size == m->mem_allocated[i]) {
			i++;
		}
		else {
			return 0;
		}
	}
	if(i == m->r) {
		return 1;
	}
	else {
		return 0;
	}
}

