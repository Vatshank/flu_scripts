#include<iostream>
using namespace std;

void reverse(char *begin, char *end)
{
	char temp;
	while(begin < end)
	{
		temp = *begin;
		*begin++ = *end;
		*end-- = temp;
	}
}

void reverseWords(char *s, int n)
{
	char *word_begin, *word_end;
	reverse(s, s+n-2);

	word_begin = s;
	word_end = s;
	while(*word_end)
	{
		word_end++;
		if(*word_end == ' ')
		{
			reverse(word_begin, word_end-1);
			word_begin = word_end + 1;
		}

		else if(*word_end == '\0')
		{
			reverse(word_begin, word_end-1);
		}
	}

}



int main()
{
	char s[] = "Padh le chutiye!";
	int n = sizeof(s)/sizeof(char);
	reverseWords(s, n);
	for (int i = 0; i<n; i++)
        cout << s[i];
    cout << endl;

	return 0;
}





