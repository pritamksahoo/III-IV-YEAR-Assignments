#include <iostream>
#include <bitset>
#include <string>

using namespace std;

#define MAX 1000

string DecToBinary(int num[], int start, int end);
void KeyGen(bitset<56> key, bitset<48> round_key, int round);
void encrypt(bitset<64> bs_plain, bitset<56> key);

template<size_t N>
int BinaryToDec(bitset<N> bs)
{
	int ret = 0, base = 1;
	for (int i = 0; i < N; ++i)
	{
		ret += bs[i]*base;
		base *= 2;
	}
	return ret;
}

template<size_t N>
void ShiftLeft(bitset<N> bs, int byRotate)
{
	bitset<N> temp_bs;
	for (int i=byRotate; i<=N-1; i++)
	{
		temp_bs[i] = bs[i - byRotate];
	}
	int index = N - byRotate;
	for (int i=0; i<byRotate; i++)
	{
		temp_bs[i] = bs[index++];
	}

	for (int i=0; i<N; i++)
	{
		bs[i] = temp_bs[i];
	}
}

template<size_t N1, size_t N2>
void permutation(bitset<N1> bs1, bitset<N2> bs2, int p_box[])
{
	int index = N2-1;
	for (int i=0; i<N2; i++)
	{
		bs2[index--] = bs1[N1-1-i];
	}
}

template<size_t N1, size_t N2>
void substitution(bitset<N1> bs1, bitset<N2> bs2, int s_box[][16])
{
	for (int i=0; i<8; i++)
	{
		int start = 6*i, end = 6*(i+1)-1;
		bitset<2> bs_row;
		bitset<4> bs_col;

		bs_row[0] = bs1[end], bs_row[1] = bs1[start];
		col_index = 0;
		for (j=start+1; j<=end-1; j++)
		{
			bs_col[col_index++] = bs1[j];
		}

		int row = BinaryToDec(bs_row);
		int col = BinaryToDec(bs_col);

		int dec[] = {s_box[row][col]};
		string binary = DecToBinary(dec, 0, 0);

		start = 4*i, end = 4*(i+1)-1;
		int index = binary.length()-1;
		for (j=start; j<=end; j++)
		{
			bs2[j] = (int)(binary[index--]) - (int)('0');
		}
	}
}

int main()
{
	string P, K;
	int plain[MAX], key[8];
	cin >> P;
	cin >> K;

	int len = P.length(), index = 0;
	for (int i=0; i<len; i++)
	{
		if (P[i] != ' ')
		{
			plain[index++] = (int)(P[i]);
		}
	}

	index = 0, len = K.size();
	for (int i=0; i<len; i++)
	{
		if (K[i] != ' ')
		{
			key[index++] = (int)(K[i]);
		}
		if (index == 8)
		{
			break;
		}
	}


}

string DecToBinary(int num[], int start, int end)
{
	string ret ("0000000000000000000000000000000000000000000000000000000000000000");
	ret.resize((end-start+1)*8);
	int index = 0;

	for (int i=start; i<=end; i++)
	{
		int n = num[i], j=0;
		while (n != 0)
		{
			rem = n%2;
			n /= 2;
			ret[index + (j++)] = rem;
		}
		index += 8;
	}
	
	return ret;
}

void KeyGen(bitset<56> key, bitset<48> round_key, int round)
{
	bitset<28> bs1, bs2;
	int i = 0;
	for (i=0; i<29; i++)
	{
		bs1[i] = key[i];
	}
	for(int j=0; j<29; j++)
	{
		bs2[j] = key[i++];
	}

	int rotate = 2;
	if (round == 1 || round == 2 || round == 9 || round == 16)
	{
		rotate = 1;
	}
	ShiftLeft(bs1, rotate);
	ShiftLeft(bs2, rotate);
	i = 0;
	for (int j=0; j<29; j++)
	{
		key[i++] = bs1[j];
	}
	for (int j=0; j<29; j++)
	{
		key[i++] = bs2[j];
	}

	int cp[] = {};

	permutation(key, round_key, cp);

}

void encrypt(bitset<64> bs_plain, bitset<56> key)
{
	
}