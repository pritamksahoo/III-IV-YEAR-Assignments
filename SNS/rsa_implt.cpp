// g++ rsa_implt.cpp -lgmp

#include <gmp.h>
#include <iostream>
#include <string>

using namespace std;

#define MAX 100

void rsa_encrypt(mpz_t cipher, const mpz_t n, const mpz_t enc_key, const mpz_t message);
void rsa_decrypt(mpz_t plain, const mpz_t n, const mpz_t dec_key, const mpz_t cipher);
int key_init(const mpz_t p, const mpz_t q, mpz_t n, const mpz_t enc_key, mpz_t dec_key);

int main()
{
	mpz_t message, n, p, q, enc_key, dec_key, cipher, plain;
	char msg_str[MAX], p_str[MAX], q_str[MAX], enc_key_str[MAX];
	int base;

	/* Inputs */
	cout << "\nEnter the value of p : ";
	cin >> p_str;

	cout << "\nEnter the value of q : ";
	cin >> q_str;

	cout << "\nEnter the value of e (encryption key) : ";
	cin >> enc_key_str;

	cout << "\nEnter the message : ";
	cin >> msg_str;

	cout << "\nEnter base of the inputs (binary - 2, decimal - 10, etc.) : ";
	cin >> base;

	/* Initialization */
	mpz_init_set_str(message, msg_str, base);
	mpz_init_set_str(p, p_str, base);
	mpz_init_set_str(q, q_str, base);
	mpz_init_set_str(enc_key, enc_key_str, base);

	/* Computing n, decryption key and some validation */
	int valid = key_init(p, q, n, enc_key, dec_key);

	if (valid)
	{
		/* Encryption */
		rsa_encrypt(cipher, n, enc_key, message);
		cout << "\n\n# Encrypted message : " << mpz_get_str(NULL, 0, cipher);

		/* Decryption */
		rsa_decrypt(plain, n, dec_key, cipher);
		cout << "\n\n# Decrypted cipher : " << mpz_get_str(NULL, 0, plain);
	}

	mpz_clears(message, p, q, enc_key, NULL);

	cout << "\n" << endl;
}

int key_init(const mpz_t p, const mpz_t q, mpz_t n, const mpz_t enc_key, mpz_t dec_key)
{
	mpz_t gcd, temp_p, temp_q, phi;

	mpz_inits(gcd, temp_p, temp_q, phi, NULL);

	/* Checking primality of p and q */
	int isPrimeP = mpz_probab_prime_p(p, 5);
	int isPrimeQ = mpz_probab_prime_p(q, 5);

	if (isPrimeP == 0)
	{
		cout << "\n\nERROR : P should be prime!\n\n---Program terminated---" << endl;
		return 0;
	}

	if (isPrimeQ == 0)
	{
		cout << "\n\nERROR : Q should be prime!\n\n---Program terminated---" << endl;
		return 0;
	}

	/* Compute value of n */
	mpz_mul(n, p, q);

	mpz_sub_ui(temp_p, p, 1);
	mpz_sub_ui(temp_q, q, 1);

	/* Computing euler-phi value of n */
	mpz_mul(phi, temp_p, temp_q);

	/* Validation */
	if (mpz_cmp_ui(enc_key, 1) <= 0 || mpz_cmp(enc_key, n) >= 0)
	{
		mpz_clears(gcd, temp_p, temp_q, phi, NULL);
		cout << "\n\nERROR : Invalid encryption key (value of 'e' should be between 1 and pq)!\n\n---Program terminated---" << endl;
		return 0;
	}

	/* Validation - gcd between encryption key and n (should be 1) */
	mpz_gcd(gcd, enc_key, phi);
	if (mpz_cmp_ui(gcd, 1) != 0)
	{
		mpz_clears(gcd, temp_p, temp_q, phi, NULL);
		cout << "\n\nERROR : Invalid encryption key ('e' should be co-prime with pq)!\n\n---Program terminated---" << endl;
		return 0;
	}

	/* Calculating dec_key (d) : mul-inverse of 'e' w.r.t 'phi(n)' */
	mpz_invert(dec_key, enc_key, phi);

	/* All valid */
	mpz_clears(gcd, temp_p, temp_q, phi, NULL);
	return 1;
}

void rsa_encrypt(mpz_t cipher, const mpz_t n, const mpz_t enc_key, const mpz_t message)
{
	mpz_powm(cipher, message, enc_key, n);
}

void rsa_decrypt(mpz_t plain, const mpz_t n, const mpz_t dec_key, const mpz_t cipher)
{
	mpz_powm(plain, cipher, dec_key, n);
}