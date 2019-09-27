#include <iostream>
#include <bitset>
#include <string>

using namespace std;

#define MAX 1000

string DecToBinary(int num[], int start, int end);
void KeyGen(bitset<56>& key, bitset<48>& round_key, int round);
void encrypt(bitset<64>& bs_plain, bitset<64>& key);
void mixer(bitset<32>& input, bitset<48>& round_key, bitset<32>& output);

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
void ShiftLeft(bitset<N>& bs, int byRotate)
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
void permutation(bitset<N1>& bs1, bitset<N2>& bs2, int p_box[])
{
	int index = N2-1;
	for (int i=0; i<N2; i++)
	{
		bs2[index--] = bs1[N1-1-p_box[i]];
	}
	// cout << bs2 << endl;
}

template<size_t N1, size_t N2>
void substitution(bitset<N1>& bs1, bitset<N2>& bs2, int s_box[8][4][16])
{
	for (int i=0; i<8; i++)
	{
		int start = 6*i, end = 6*(i+1)-1;
		bitset<2> bs_row;
		bitset<4> bs_col;

		bs_row[0] = bs1[start], bs_row[1] = bs1[end];
		int col_index = 0;
		for (int j=start+1; j<=end-1; j++)
		{
			bs_col[col_index++] = bs1[j];
		}

		int row = BinaryToDec(bs_row);
		int col = BinaryToDec(bs_col);

		int dec[] = {s_box[7-i][row][col]};
		string binary = DecToBinary(dec, 0, 0);

		start = 4*i, end = 4*(i+1)-1;
		int index = binary.length()-1;
		for (int j=start; j<=end; j++)
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

	int len = P.length(), index = 0, key_index = 0;
	for (int i=0; i<len; i++)
	{
		if (P[i] != ' ')
		{
			plain[index++] = (int)(P[i]);
		}
	}

	len = K.size();
	for (int i=0; i<len; i++)
	{
		if (K[i] != ' ')
		{
			key[key_index++] = (int)(K[i]);
		}
		if (key_index == 8)
		{
			break;
		}
	}

	bitset<64> key_org (DecToBinary(key, 0, 7));

	for (int i=0; i<index; i=i+8)
	{
		bitset<64> plain_org (DecToBinary(plain, 8*i, 8*(i+1)-1));
		encrypt(plain_org, key_org);
		cout << plain_org;
	}
	cout << '\n' << DecToBinary(plain,0,index-1);
	// bitset<64> plain (string("0000000100100011010001010110011110001001101010111100110111101111"));
	// bitset<64> key (string("0001001100110100010101110111100110011011101111001101111111110001"));
	// encrypt(plain, key);
	// cout << plain << endl;

}

string DecToBinary(int num[], int start, int end)
{
	string ret ("0000000000000000000000000000000000000000000000000000000000000000");
	ret.resize((end-start+1)*8);
	int index = 0;

	for (int i=start; i<=end; i++)
	{
		int n = num[i], j=7;
		while (n != 0)
		{
			int rem = n%2;
			n /= 2;
			ret[index + (j--)] = (char)(rem + (int)('0'));
		}
		index += 8;
	}
	// cout << ret << endl;
	return ret;
}

void KeyGen(bitset<56>& key, bitset<48>& round_key, int round)
{
	bitset<28> bs1;
	bitset<28> bs2;
	// cout << "key : " << key << endl;
	int i = 0;
	for (i=0; i<28; i++)
	{
		bs2[i] = key[i];
	}
	for(int j=0; j<28; j++)
	{
		bs1[j] = key[i++];
	}

	int rotate = 2;
	if (round == 1 || round == 2 || round == 9 || round == 16)
	{
		rotate = 1;
	}
	// cout << "c #" << round << "(before) : " << bs1 << endl;
	ShiftLeft(bs1, rotate);
	// cout << "c #" << round << "(after) : " << bs1 << endl;
	// cout << "d #" << round << "(before) : " << bs2 << endl;
	ShiftLeft(bs2, rotate);
	// cout << "d #" << round << "(after) : " << bs2 << endl;

	i = 0;
	for (int j=0; j<28; j++)
	{
		key[i++] = bs2[j];
	}
	for (int j=0; j<28; j++)
	{
		key[i++] = bs1[j];
	}

	int CP[] = {
		13, 16, 10, 23, 0, 4,
        2, 27, 14, 5, 20,  9,
      	22, 18, 11, 3, 25, 7,
       	15, 6, 26, 19, 12, 1,
       	40, 51, 30, 36, 46, 54,
       	29, 39, 50, 44, 32, 47,
       	43, 48, 38, 55, 33, 52,
       	45, 41, 49, 35, 28, 31
	};

	permutation(key, round_key, CP);
	// cout << "Round Key #" << round << " : " << round_key << endl;

}

void mixer(bitset<32>& input, bitset<48>& round_key, bitset<32>& output)
{
	bitset<48> temp_input;
	bitset<32> temp_output;
	int ED[] = {
		31,  0,  1,  2,  3,  4,
        3,  4,  5,  6,  7,  8,
        7,  8,  9, 10, 11, 12,
       	11, 12, 13, 14, 15, 16,
       	15, 16, 17, 18, 19, 20,
       	19, 20, 21, 22, 23, 24,
       	23, 24, 25, 26, 27, 28,
       	27, 28, 29, 30, 31,  0
	};
	
	permutation(input, temp_input, ED);
	// cout << "E(R) : " << temp_input << endl;

	temp_input ^= round_key;
	// cout << "K + E(R) : " << temp_input << endl;

	int S[8][4][16] = {
		{
			{14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7},
			{0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8},
			{4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0},
			{15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13}
		},
		{
			{15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10},
	 		{3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5},
	 		{0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15},
			{13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9}
		},
		{
			{10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8},
			{13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1},
			{13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7},
	 		{1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12}
		},
		{
			{7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15},
			{13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9},
			{10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4},
			{3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14}
		},
		{
			{2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9},
			{14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6},
	 		{4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14},
			{11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3}
		},
		{
			{12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11},
			{10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8},
	 		{9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6},
	 		{4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13}
		},
		{
			{4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1},
			{13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6},
	 		{1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2},
	 		{6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12}
		},
		{
			{13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7},
	 		{1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2},
	 		{7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8},
	 		{2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11}
		}
	};

	substitution(temp_input, temp_output, S);
	// cout << "S-Box : " << temp_output << endl;

	int P[] = {
		15,  6, 19, 20,
       	28, 11, 27, 16,
        0, 14, 22, 25,
        4, 17, 30,  9,
        1,  7, 23, 13,
       	31, 26,  2,  8,
       	18, 12, 29,  5,
       	21, 10,  3, 24
	};

	permutation(temp_output, output, P);
	// cout << "Final-P-Box : " << output << endl;
}

void encrypt(bitset<64>& bs_plain, bitset<64>& key_org)
{
	bitset<56> key;
	int CP[] = {
		56, 48, 40, 32, 24, 16,  8,
        0, 57, 49, 41, 33, 25, 17,
        9,  1, 58, 50, 42, 34, 26,
       	18, 10,  2, 59, 51, 43, 35,
       	62, 54, 46, 38, 30, 22, 14,
        6, 61, 53, 45, 37, 29, 21,
       	13,  5, 60, 52, 44, 36, 28,
       	20, 12,  4, 27, 19, 11,  3
	};

	// Parity Drop
	// cout << "org key : " << key_org << endl;
	permutation(key_org, key, CP);
	// cout << "parity key : " << key << endl;

	int IP[] = {
		57, 49, 41, 33, 25, 17,  9,  1,
       	59, 51, 43, 35, 27, 19, 11,  3,
       	61, 53, 45, 37, 29, 21, 13,  5,
       	63, 55, 47, 39, 31, 23, 15,  7,
       	56, 48, 40, 32, 24, 16,  8,  0,
       	58, 50, 42, 34, 26, 18, 10,  2,
       	60, 52, 44, 36, 28, 20, 12,  4,
       	62, 54, 46, 38, 30, 22, 14,  6
	};
	int FP[] = {
		39,  7, 47, 15, 55, 23, 63, 31,
       	38,  6, 46, 14, 54, 22, 62, 30,
       	37,  5, 45, 13, 53, 21, 61, 29,
       	36,  4, 44, 12, 52, 20, 60, 28,
       	35,  3, 43, 11, 51, 19, 59, 27,
       	34,  2, 42, 10, 50, 18, 58, 26,
       	33,  1, 41,  9, 49, 17, 57, 25,
       	32,  0, 40,  8, 48, 16, 56, 24
	};
	bitset<64> bs_int;
	bitset<48> round_key;
	permutation(bs_plain, bs_int, IP);
	// cout << "After initial permutation : " << bs_int << endl;

	for (int i=1; i<=16; i++)
	{
		// Round Key
		KeyGen(key, round_key, i);
		// cout << "Round #" << i << " : " << endl;
		bitset<32> feistel, l, r;
		
		int j = 0;
		for (j=0; j<32; j++)
		{
			r[j] = bs_int[j];
		}
		for(int k=0; k<32; k++)
		{
			l[k] = bs_int[j++];
		}		

		// cout << "l(old) : " << l << endl;
		// cout << "r(old) : " << r << endl;
		// Mixer
		mixer(r, round_key, feistel);
		// cout << "feistel key : " << feistel << endl;
		l ^= feistel;
		// cout << "New l : " << l << endl;

		// Swapper
		j = 0;
		for (int k=0; k<32; k++)
		{
			bs_int[j++] = l[k];
		}
		for (int k=0; k<32; k++)
		{
			bs_int[j++] = r[k];
		}
		// cout << "Finally : " << bs_int << endl;
	}

	ShiftLeft(bs_int, 32);

	permutation(bs_int, bs_plain, FP);
}