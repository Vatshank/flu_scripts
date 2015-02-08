#include<iostream>
using namespace std;

#define FALSE 0
#define TRUE 1

int countWords(char *str)
{
	bool flag=TRUE;
	int count=0;

	while(*str)
	{
		if((*str == ' ') || (*str == '\t') || (*str == '\n'))
		{
			flag = TRUE;
		}

		else if(flag==TRUE)
		{
			flag = FALSE;
			count++;
		}

		str++;
	}

	return count;
}

int main()
{
	char str[] = "Padh lo, naukri lagwalo";
	cout << countWords(str) <<endl;
	return 0;

}