#include <iostream>
#include <bitset>
#include <string>

using namespace std;

bitset<8> modulus(string("00011011"));
bitset<8> global_round_key[11][4][4];

bitset<32> round_key_constant[10];

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
void ShiftBitLeftWithWrapping(bitset<N>& bs, int byRotate)
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

void SubWord(bitset<32>& word)
{
	bitset<8> constant (string("11000110"));
	for (int i=31; i>0; i=i-8)
	{
		bitset<8> temp_word;
		int index = 7;
		for (int j=i; j>i-8; j--)
		{
			temp_word[index--] = word[j];
		}

		bitset<8> inverse_byte(0);
		inverse(temp_word, inverse_byte);

		bitset<8> temp_byte(0);
		for (int k=0; k<8; k++)
		{
			temp_byte[7-i] = inverse_byte[7-i] ^ inverse_byte[7-(i+4)%8] ^ inverse_byte[7-(i+5)%8] ^ inverse_byte[7-(i+6)%8] ^ inverse_byte[7-(i+7)%8];
			temp_byte[7-i] ^= constant;
		}
		
		index = 7;
		for (int j=i; j>i-8; j--)
		{
			word[j] = temp_byte[index--];
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

void MixColumn(bitset<8> bs[][4])
{
	bitset<8> temp_bs[4][4];
	bitset<8> only_zero (string("00000000"));
	string one = "00000001";
	string two = "00000010";
	string three = "00000011";

	string MixMult[4][4] = {two, three, one, one, one, two, three, one, one, one, two, three, three, one, one, two};
	bitset<8> multBy[4][4];
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bitset<8> bt(MixMult[i][j]);
			multBy[i][j] = bt;
		}
	}

	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			temp_bs[i][j] = only_zero;
			for (int k=0; k<4; k++)
			{
				bitset<8> ans;
				ans = only_zero;
				multiply(multBy[i][k], bs[k][j], ans);

				temp_bs[i][j] ^= ans;
			}
		}
	}

	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bs[i][j] = temp_bs[i][j];
		}
	}
}

void AddRoundKey(bitset<8> bs[4][4], bitset<8> RoundKey[4][4])
{
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bs[i][j] ^= RoundKey[i][j];
		}
	}
}

void KeyGen(bitset<128> key)
{
	int turn = 0;
	int index = 127;
	bitset<32> word[44];

	string round_constant[10] = {
		"00000001000000000000000000000000",
		"00000010000000000000000000000000",
		"00000100000000000000000000000000",
		"00001000000000000000000000000000",
		"00010000000000000000000000000000",
		"00100000000000000000000000000000",
		"01000000000000000000000000000000",
		"10000000000000000000000000000000",
		"00011011000000000000000000000000",
		"00110110000000000000000000000000",
	};

	for (int i=0; i<10; i++)
	{
		bitset<32> rt (round_constant[i]);
		round_key_constant[i] = rt;
	}

	for (int i=0; i<4; i++)
	{
		int t_index = 31;
		for (int j=index; j>index-32; j--)
		{
			word[i][t_index--] = key[j];
		}
		index -= 32;
	}

	for (int i=4; i<44; i++)
	{
		if (i%4 != 0)
		{
			word[i] = word[i-1] ^ word[i-4];
		}
		else
		{
			bitset<32> temp_word;
			temp_word = word[i-1];

			ShiftBitLeftWithWrapping(temp_word, 8);
			SubWord(temp_word);

			temp_word ^= round_key_constant[i/4 - 1];

			word[i] = temp_word;
		}
	}

	int word_index = 0;
	for (int i=0; i<11; i++)
	{
		for (int j=0; j<4; j++)
		{
			int bit_index = 31;
			for (int k=0; k<4; k++)
			{
				for (int l=7; l>=0; l--)
				{
					global_round_key[i][k][j][l] = word[word_index][bit_index--];
				}
			}
			word_index++;
		}
	}

}

void encrypt(bitset<128> plain)
{
	
}

int main()
{

}