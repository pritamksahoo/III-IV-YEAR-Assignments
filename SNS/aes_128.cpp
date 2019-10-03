#include <iostream>
#include <bitset>
#include <string>
#include <map>

using namespace std;

#define MAX 1000

bitset<8> modulo(string("00011011"));
bitset<8> global_round_key[11][4][4];

map< string, string > inv_sbox;
map< string, string >::iterator it;

bitset<32> round_key_constant[10];

string hexaToBinary(char ch)
{
    switch(toupper(ch))
    {
        case '0': return "0000";
        case '1': return "0001";
        case '2': return "0010";
        case '3': return "0011";
        case '4': return "0100";
        case '5': return "0101";
        case '6': return "0110";
        case '7': return "0111";
        case '8': return "1000";
        case '9': return "1001";
        case 'A': return "1010";
        case 'B': return "1011";
        case 'C': return "1100";
        case 'D': return "1101";
        case 'E': return "1110";
        case 'F': return "1111";
    }
}


template<size_t N>
int BinaryToDec(bitset<N> s)
{
    int ret=0, ex=1;
    for (int i=0; i<N; i++)
    {
        if (s[i] == 1)
        {
            ret += ex;
        }
        ex *= 2;
    }
    return ret;
}

string BinaryToHexa(bitset<8> bs)
{
	string ret ("00");

	int ret_index = 0;
	
	for (int i=7; i>0; i=i-4)
	{
		bitset<4> bt;
		int index = 3;
		for (int j=i; j>i-4; j--)
		{
			bt[index--] = bs[j];
		}
		// cout << "\nBit : " << bt << endl;
		int dec = BinaryToDec(bt);
		// cout << "Dec : " << dec << endl;
	    switch(dec)
	    {
	        case 0: ret[ret_index] = '0'; break;
	        case 1: ret[ret_index] = '1'; break;
	        case 2: ret[ret_index] = '2'; break;
	        case 3: ret[ret_index] = '3'; break;
	        case 4: ret[ret_index] = '4'; break;
	        case 5: ret[ret_index] = '5'; break;
	        case 6: ret[ret_index] = '6'; break;
	        case 7: ret[ret_index] = '7'; break;
	        case 8: ret[ret_index] = '8'; break;
	        case 9: ret[ret_index] = '9'; break;
	        case 10: ret[ret_index] = 'a'; break;
	        case 11: ret[ret_index] = 'b'; break;
	        case 12: ret[ret_index] = 'c'; break;
	        case 13: ret[ret_index] = 'd'; break;
	        case 14: ret[ret_index] = 'e'; break;
	        case 15: ret[ret_index] = 'f'; break;
	    }
	    ret_index++;
	}
	return ret;
}

void ShiftBytetLeft(bitset<8> bs[4], int byRotate)
{
	bitset<8> temp_bs[4];
	for (int i=0; i<4-byRotate; i++)
	{
		temp_bs[i] = bs[i + byRotate];
	}
	int index = 0;
	for (int i=4-byRotate; i<4; i++)
	{
		temp_bs[i] = bs[index++];
	}

	for (int i=0; i<4; i++)
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

void ShiftBytetRight(bitset<8> bs[4], int byRotate)
{
	bitset<8> temp_bs[4];
	for (int i=byRotate; i<4; i++)
	{
		temp_bs[i] = bs[i - byRotate];
	}
	int index = 4-byRotate;
	for (int i=0; i<byRotate; i++)
	{
		temp_bs[i] = bs[index++];
	}

	for (int i=0; i<4; i++)
	{
		bs[i] = temp_bs[i];
	}
}

void ShiftBytetRightWithWrapping(bitset<8> bs[4][4])
{
	for (int i=1; i<4; i++)
	{
		ShiftBytetRight(bs[i], i);
	}
}

template<size_t N>
void ShiftBitLeftWOWrapping(bitset<N>& bs, int byRotate)
{
	for (int i=N-1; i>=byRotate; i--)
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
	mult[0] = bs1;
	// cout << "Mult : " << mult[0] << endl;
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
			mult[i] ^= modulo;
		}
		// cout << "Mult " << i << " : " << mult[i] << endl;
	}

	for (int i=0; i<8; i++)
	{
		if (bs2[i] == 1)
		{
			output ^= mult[i];
			// cout << "Output : " << output << endl;
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
	bitset<8> constant (string("01100011"));
	for (int i=31; i>0; i=i-8)
	{
		bitset<8> temp_word (0);
		int index = 7;
		for (int j=i; j>i-8; j--)
		{
			temp_word[index--] = word[j];
		}

		bitset<8> inverse_byte (0);
		inverse(temp_word, inverse_byte);
		// cout << "Act. byte : " << temp_word << endl;
 	// 	cout << "Inverse Byte : " << inverse_byte << endl;

		bitset<8> temp_byte (0);
		for (int k=0; k<8; k++)
		{
			temp_byte[k] = inverse_byte[k] ^ inverse_byte[(k+4)%8] ^ inverse_byte[(k+5)%8] ^ inverse_byte[(k+6)%8] ^ inverse_byte[(k+7)%8];
		}
		// cout << "After Multiplication : " << temp_byte << endl;
		temp_byte ^= constant;
		// cout << "After Subword : " << temp_byte << endl;
		index = 7;
		for (int j=i; j>i-8; j--)
		{
			word[j] = temp_byte[index--];
		}
	}
}

void Inv_S_Box()
{
	bitset<8> constant (string("01100011"));
	for (int i = 0; i < 16; ++i)
	{
		for (int j = 0; j < 16; ++j)
		{
			bitset<4> l (i);
			bitset<4> r (j);
			bitset<8> temp_bs;

			for (int k=0; k<4; k++)
			{
				temp_bs[k] = r[k];
				temp_bs[k+4] = l[k];
			}

			bitset<8> inverse_byte(0);
			inverse(temp_bs, inverse_byte);

			bitset<8> temp_byte(0);
			for (int k=0; k<8; k++)
			{
				temp_byte[k] = inverse_byte[k] ^ inverse_byte[(k+4)%8] ^ inverse_byte[(k+5)%8] ^ inverse_byte[(k+6)%8] ^ inverse_byte[(k+7)%8];
			}
			temp_byte ^= constant;

			inv_sbox[temp_byte.to_string()] = temp_bs.to_string();
		}
	}
}

void SubByte(bitset<8> bs[][4])
{
	bitset<8> constant (string("01100011"));
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bitset<8> inverse_byte(0);
			inverse(bs[i][j], inverse_byte);

			bitset<8> temp_byte(0);
			for (int k=0; k<8; k++)
			{
				temp_byte[k] = inverse_byte[k] ^ inverse_byte[(k+4)%8] ^ inverse_byte[(k+5)%8] ^ inverse_byte[(k+6)%8] ^ inverse_byte[(k+7)%8];
			}
			temp_byte ^= constant;

			// inv_sbox[temp_byte.to_string()] = bs[i][j].to_string();

			bs[i][j] = temp_byte;
		}
	}
}

void InvSubByte(bitset<8> bs[4][4])
{
	bitset<8> constant (string("01100011"));
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			it = inv_sbox.find(bs[i][j].to_string());
			bitset<8> tt (it->second);
			bs[i][j] = tt;
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

void InvMixColumn(bitset<8> bs[][4])
{
	bitset<8> temp_bs[4][4];
	bitset<8> only_zero (string("00000000"));
	string nine = "00001001";
	string bee = "00001011";
	string dee = "00001101";
	string ee = "00001110";

	string MixMult[4][4] = {ee, bee, dee, nine, nine, ee, bee, dee, dee, nine, ee, bee, bee, dee, nine, ee};
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
		// cout << "Word " << i << " : " << word[i] << endl;
	}

	for (int i=4; i<44; i++)
	{
		// cout << "Word " << i << " : " << endl;
		if (i%4 != 0)
		{
			word[i] = word[i-1] ^ word[i-4];
		}
		else
		{
			bitset<32> temp_word;
			temp_word = word[i-1];

			ShiftBitLeftWithWrapping(temp_word, 8);
			// cout << "After RotWord : " << temp_word << endl;
			SubWord(temp_word);
			// cout << "After SubWord : " << temp_word << endl;
			temp_word ^= round_key_constant[i/4 - 1];
			// cout << "After XOR with RCon : " << temp_word << endl;
			word[i] = temp_word ^ word[i-4];
			// cout << "After RotWord : " << temp_word << endl;
		}
		// cout << "Finally : " << word[i] << endl;
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

void encrypt(bitset<128> plain, char cipher[], int* cipher_index)
{
	bitset<8> plain_word[4][4];

	int index = 127;
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bitset<8> tt;
			for (int k=7; k>=0; k--)
			{
				tt[k] = plain[index--];
			}
			plain_word[j][i] = tt;
		}
	}

	AddRoundKey(plain_word, global_round_key[0]);

	for (int i=1; i<10; i++)
	{
		// cout << "Round " << i << " : " << endl;
		SubByte(plain_word);

		ShiftBytetLeftWithWrapping(plain_word);

		MixColumn(plain_word);

		AddRoundKey(plain_word, global_round_key[i]);

	}

	SubByte(plain_word);
	ShiftBytetLeftWithWrapping(plain_word);
	AddRoundKey(plain_word, global_round_key[10]);

	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			// cout << plain_word[j][i] << endl;
			string hex = BinaryToHexa(plain_word[j][i]);
			cipher[(*cipher_index)++] = hex[0];
			cipher[(*cipher_index)++] = hex[1];

			// cout << hex;
		}
	}
}

void decipher(bitset<128>cipher_bs, char decrypted[], int* decrypted_index)
{
	bitset<8> cipher_word[4][4];

	int index = 127;
	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			bitset<8> tt;
			for (int k=7; k>=0; k--)
			{
				tt[k] = cipher_bs[index--];
			}
			cipher_word[j][i] = tt;
		}
	}

	AddRoundKey(cipher_word, global_round_key[10]);
	ShiftBytetRightWithWrapping(cipher_word);
	InvSubByte(cipher_word);

	for (int i=9; i>=1; i--)
	{
		// cout << "Round " << i << " : " << endl;
		AddRoundKey(cipher_word, global_round_key[i]);
		InvMixColumn(cipher_word);
		ShiftBytetRightWithWrapping(cipher_word);
		InvSubByte(cipher_word);
	}
	AddRoundKey(cipher_word, global_round_key[0]);

	for (int i=0; i<4; i++)
	{
		for (int j=0; j<4; j++)
		{
			// cout << plain_word[j][i] << endl;
			string hex = BinaryToHexa(cipher_word[j][i]);
			decrypted[(*decrypted_index)++] = hex[0];
			decrypted[(*decrypted_index)++] = hex[1];

			// cout << hex;
		}
	}

}

int main()
{
	string plain;
	string key;

	cin >> plain;
	cin >> key;

	int plain_len = plain.length();

	bitset<128> plain_bs;
	bitset<128> key_bs;
	bitset<128> cipher_bs;

	char cipher[MAX];
	int cipher_index = 0;
	char decrypted[MAX];
	int decrypted_index = 0;

	int index = 127;
	for (int i=0; i<32; i++)
	{
		bitset<4> tt (hexaToBinary(key[i]));
		for (int j=3; j>=0; j--)
		{
			key_bs[index--] = tt[j];
		}
	}

	KeyGen(key_bs);

	int i=0;
	index = 127;
	for (i=0; i<plain_len; i++)
	{
		bitset<4> tt (hexaToBinary(plain[i]));
		for (int j=3; j>=0; j--)
		{
			plain_bs[index--] = tt[j];
		}
		if ((i+1)%32 == 0)
		{
			encrypt(plain_bs, cipher, &cipher_index);
			index = 127;
		}
	}

	if (i%32 != 0)
	{
		int k = i;
		while (k%32 != 0)
		{
			bitset<4> tt (hexaToBinary('0'));
			for (int j=3; j>=0; j--)
			{
				plain_bs[index--] = tt[j];
			}
			k++;
		}
		encrypt(plain_bs, cipher, &cipher_index);
	}
	
	cipher[cipher_index] = '\0';
	cout << cipher << endl;

	Inv_S_Box();

	index = 127;
	for (i=0; i<cipher_index; i++)
	{
		bitset<4> tt (hexaToBinary(cipher[i]));
		for (int j=3; j>=0; j--)
		{
			cipher_bs[index--] = tt[j];
		}
		if ((i+1)%32 == 0)
		{
			decipher(cipher_bs, decrypted, &decrypted_index);
			index = 127;
		}
	}

	decrypted[decrypted_index] = '\0';
	cout << decrypted;

	// bitset<8> b1(string("11001111"));
	// bitset<8> b2(string("11100110"));
	// bitset<8> b3;

	// multiply(b1, b2, b3);
	// cout << "Multiply : " << b3 << endl;

	// cout << plain;
	// if (plain_len % 32 != 0)
	// {
	// 	int extra = 32 - plain_len%32;
	// 	for (i=0; i<extra; i++)
	// 	{
	// 		cout << '0';
	// 	}
	// }
}