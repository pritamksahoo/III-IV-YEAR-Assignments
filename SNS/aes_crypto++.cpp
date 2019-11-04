// g++ aes_crypto++.cpp -lcrypto++
// AES CBC MODE

#include <iostream>
#include <iomanip>
#include <string>

#include <crypto++/modes.h>
#include <crypto++/aes.h>
#include <crypto++/filters.h>
// #include <crypto++/pch.h">
#include <crypto++/osrng.h>
#include <crypto++/cryptlib.h>
#include <crypto++/hex.h>
#include <crypto++/ccm.h>

using namespace std;
using namespace CryptoPP;

void aes_initialize(byte aes_key[], byte iv[]);
string encrypt(string P, const byte K[], const byte IV[]);
string decrypt(string C, const byte K[], const byte IV[]);
void pretty_print(string to_print);

int main()
{
	byte aes_key[CryptoPP::AES::DEFAULT_KEYLENGTH], iv[CryptoPP::AES::BLOCKSIZE];
	CryptoPP::AutoSeededRandomPool asrp;

	string plaintext, ciphertext, decrypted_plaintext;

	plaintext = "Two wrongs don't make a right";
	cout << "\nPlain Text : " << plaintext << endl;

	// Initializing key and iv
	aes_initialize(aes_key, iv);

	// Encryption
	ciphertext = encrypt(plaintext, aes_key, iv);
	cout << "\nCipher Text : ";
	pretty_print(ciphertext);

	// Decryption
	decrypted_plaintext = decrypt(ciphertext, aes_key, iv);
	cout << "\nDecrypted Plain Text : " << decrypted_plaintext;

	cout << endl;
}


void aes_initialize(byte aes_key[], byte iv[])
{
	CryptoPP::AutoSeededRandomPool asrp;

	// Generating random encryption key and Initialization vector
    asrp.GenerateBlock(aes_key, CryptoPP::AES::DEFAULT_KEYLENGTH);
    asrp.GenerateBlock(iv, CryptoPP::AES::BLOCKSIZE);
}


string encrypt(string P, const byte K[], const byte IV[])
{
	string C;

	// Creating encryption object
	CryptoPP::CBC_Mode< AES >::Encryption enc;
	enc.SetKeyWithIV(K, CryptoPP::AES::DEFAULT_KEYLENGTH, IV);

	// Encryption
	CryptoPP::StringSource ss(P, true, new CryptoPP::StreamTransformationFilter(enc, new CryptoPP::StringSink(C)));

	CryptoPP::StreamTransformationFilter st_filter(enc);
	st_filter.Put((const byte*)P.data(), P.size());
	st_filter.MessageEnd();

	const size_t ret_size = st_filter.MaxRetrievable();
	C.resize(ret_size);
	st_filter.Get((byte*)C.data(), C.size());

	return C;
}


string decrypt(string C, const byte K[], const byte IV[])
{
	string plain;

	// Creating encryption object
	CryptoPP::CBC_Mode< AES >::Decryption dec;
	dec.SetKeyWithIV(K, CryptoPP::AES::DEFAULT_KEYLENGTH, IV);

	// Decryption
	CryptoPP::StringSource ss(C, true, new CryptoPP::StreamTransformationFilter(dec, new CryptoPP::StringSink(plain)));

	StreamTransformationFilter st_filter(dec);
	st_filter.Put((const byte*)C.data(), C.size());
	st_filter.MessageEnd();

	const size_t ret_size = st_filter.MaxRetrievable();
	plain.resize(ret_size);
	st_filter.Get((byte*)plain.data(), plain.size());
	
	return plain;
}


void pretty_print(string to_print)
{
	string encoded;
	encoded.clear();

	CryptoPP::StringSource(to_print, true, new CryptoPP::HexEncoder(new CryptoPP::StringSink(encoded)));

	cout << encoded << endl;
}