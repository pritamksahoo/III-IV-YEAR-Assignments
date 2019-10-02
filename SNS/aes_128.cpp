#include <iostream>
#include <bitset>
#include <string>

using namespace std;

bitset<8> modulus(string("00011011"));
bitset<8> global_round_key[11][4][4];

template<size_t N>
void ShiftBytetLeft(bitset<N> bs[4], int byRotate)
{
	bitset<N> temp_bs[4];
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

void ShiftBytetLeftWithWrapping(bitset<8> bs[4][4])
{
	for (int i=1; i<4; i++)
	{
		ShiftBytetLeft(bs[i], i);
	}
}

template<size_t N>
void ShiftBitLeftWOWrapping(bitset<N>& bs, int byRotate)
{
	for (int i=byRotate; i<=N-1; i++)
	{
		bs[i] = bs[i - byRotate];
	}
	for (int i=0; i<byRotate; i++)
	{
		bs[i] = 0;
	}
}

template<size_t N>
void multiply(bitset<N> bs1, bitset<N> bs2, bitset<N>& output)
{
	bitset<8> mult[8];
	mult[0] = bs1[0];

	for (int i=1; i<8; i++)
	{
		mult[i] = mult[i-1];

		if (mult[i][7] == 0)
		{
			ShiftBitLeftWOWrapping(mult[i], 1);
		}
		else
		{
			ShiftBitLeftWOWrapping(mult[i], 1);
			mult[i] ^= modulus;
		}
	}

	for (int i=0; i<8; i++)
	{
		if (bs2[i] == 1)
		{
			output ^= mult[i];
		}
	}
}

template<size_t N>
void DecToBinary(bitset<N>& output, int num)
{
	int index = 0;
	while (num > 0)
	{
		if (num%2)
		{
			output[index++] = 1;
		}
		else
		{
			output[index++] = 0;
		}
		num /= 2;
	}
}

template<size_t N>
void inverse(bitset<N> bs, bitset<N>& output)
{
	bitset<8> only_one (string("00000001"));
	bitset<8> zeros_like (string("00000000"));

	if (bs == zeros_like)
	{
		output = bs;
	}
	else
	{
		int found = 0;
		for (int i=0; i<16 && found == 0; i++)
		{
			for(int j=0; j<16 && found == 0; j++)
			{
				bitset<8> temp_bs(0);
				bitset<4> l(0);
				bitset<4> r(0);

				DecToBinary(l, i);
				DecToBinary(r, j);

				for (int k=0; k<4; k++)
				{
					temp_bs[k] = r[k];
					temp_bs[k+4] = l[k];
				}

				bitset<8> mult_temp(0);
				multiply(bs, temp_bs, mult_temp);

				if (mult_temp == only_one)
				{
					output = temp_bs;
					found = 1;
				}
			}
		}
	}
}

void SubByte(bitset<8> bs[][4])
{
	bitset<8> constant (string("11000110"));
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bitset<8> inverse_byte(0);
			inverse(bs[i][j], inverse_byte);

			bitset<8> temp_byte(0);
			for (int k=0; k<8; k++)
			{
				temp_byte[7-i] = inverse_byte[7-i] ^ inverse_byte[7-(i+4)%8] ^ inverse_byte[7-(i+5)%8] ^ inverse_byte[7-(i+6)%8] ^ inverse_byte[7-(i+7)%8];
				temp_byte[7-i] ^= constant;
			}
			bs[i][j] = temp_byte;
		}
	}
}



int main()
{

}