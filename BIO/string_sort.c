#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_NO 100
#define MAX_LEN 100

struct ArrayOfString
{
	char string[MAX_LEN];
	struct ArrayOfString* next;
};

int ascii(char ch);
struct ArrayOfString* NewNode(char str[]);
void string_sort(char store[][MAX_LEN], int no_string, int max_str_len);
void push_back(struct ArrayOfString** as, char str[]);
void printArrayOfString(struct ArrayOfString *as[]);

int main()
{
	char store[MAX_NO][MAX_LEN];
	int no_string, i, max_act_len = 0;

	// printf("Enter no. of strings : ");
	scanf("%d", &no_string);

	for (i=0; i<no_string; i++)
	{
		scanf("%s", store[i]);
		if (max_act_len < strlen(store[i]))
		{
			max_act_len = strlen(store[i]);
		}
	}

	// for (i=0; i<no_string; i++)
	// {
	// 	printf("%s ", store[i]);
	// }

	string_sort(store, no_string, max_act_len);
}

int ascii(char ch)
{
	return ((int)(tolower(ch))-(int)('a')+1);
}

void printArrayOfString(struct ArrayOfString *as[])
{
	int i;
	struct ArrayOfString *temp;
	for(i=0; i<27; i++)
	{
		temp = as[i];
		printf("%d : ", i);
		while(temp != NULL)
		{
			printf("%s ", temp->string);
			temp = temp->next;
		}
		printf("\n");
	}
	printf("\n");
}

struct ArrayOfString* NewNode(char str[])
{
	struct ArrayOfString* as = (struct ArrayOfString*)malloc(sizeof(struct ArrayOfString));
	strcpy(as->string, str);
	as->next = NULL;
	return as;
}

void push_back(struct ArrayOfString** as, char str[])
{
	struct ArrayOfString *head, *new_node;

	if (*as == NULL)
	{
		*as = NewNode(str);
	}
	else
	{
		head = *as;
		while (head->next != NULL)
		{
			head = head->next;
		}
		new_node = NewNode(str);
		head->next = new_node;
	}
}

void string_sort(char store[][MAX_LEN], int no_string, int max_str_len)
{
	struct ArrayOfString* as1[27];
	struct ArrayOfString* as2[27];
	struct ArrayOfString* temp_node;
	int i, j, temp_len;
	char temp_str_empty[MAX_LEN], temp_str[MAX_LEN];
	temp_str_empty[0] = '\0';

	for (i = 0; i < 27; ++i)
	{
		as1[i] = NULL;
	}

	for (j=0; j<no_string; j++)
	{
		temp_len = strlen(store[j]);
		if (temp_len == max_str_len)
		{
			push_back(&as1[ascii(store[j][temp_len-1])], store[j]);
		}
		else
		{
			push_back(&as1[0], store[j]);
		}
	}
	// printArrayOfString(as1);
	for (i=1; i<max_str_len; i++)
	{
		for (j = 0; j < 27; ++j)
		{
			as2[j] = NULL;
		}

		for (j=0; j<27; j++)
		{
			temp_node = as1[j];
			while (temp_node != NULL)
			{
				strcpy(temp_str, temp_node->string);
				temp_len = strlen(temp_str);
				if (temp_len >= max_str_len-i)
				{
					push_back(&as2[ascii(temp_str[max_str_len-i-1])], temp_str);
				}
				else
				{
					push_back(&as2[0], temp_str);
				}
				temp_node = temp_node->next;
			}
		}

		for (j = 0; j < 27; ++j)
		{
			as1[j] = as2[j];
		}

	}

	for (i=0; i<27; i++)
	{
		temp_node = as1[i];
		while (temp_node != NULL)
		{
			printf("%s\n", temp_node->string);
			temp_node = temp_node->next;
		}
	}
}