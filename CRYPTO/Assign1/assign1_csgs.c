/*
	PRITAM KUMAR SAHOO
	BT16CSE068

	Que - Implementation of core construction of CSGS Algorithm
	CODE with PROPER COMMENTS and DECORATION and DESCRIPTION
*/

/*
	IMPORT REQUIRED LIBRARIES
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <gmp.h>
#include <pbc/pbc.h>
#include <time.h>
#include <assert.h>

/*
	Structure to store SETUP variables (bilinear-pairing) of CSGS Algo, which includes
	order, identity, generator, alpha, omega (random exponents), Public Parameters (PP), 
	Master Enrollment Key (MK), Tracing Key (TK), etc.
*/
typedef struct setup_output {
	element_t mk0;
	mpz_t mk1;
	mpz_t tk;
	mpz_t n;
	element_t G;
	pairing_t pairing;

	// e = element_pairing() function
	element_t gen_subgroup_q;
	element_t* generators;
	element_t B_Omega;
	element_t A_val;
	mpz_t alpha;

	// identity of G
	element_t identity;

	pbc_param_t p;
	mpz_t omega;
	mpz_t pval, qval;
	mpz_t mval;

} setup_result;


setup_result ret_setup;


void random_prime_bits(mpz_t result, mpz_t n) {

	/*
		PURPOSE : Generating random prime of given bit-size

		INPUT : Bit Size (n)

		OUTPUT : Random Prime

		ALGORITHM : Given step by step INSIDE code itself

	*/

	mpz_t random;
	mpz_init(random);

	// Random state
	gmp_randstate_t state;
	gmp_randinit_default(state);

	mpz_init(random);
	gmp_randseed_ui(state, (rand()+1)*(rand()+1));

	if (mpz_cmp_ui(n,1) <= 0) {
		// No prime of bit-size less than or equal to 1 exists
		printf("NO PRIME EXISTS\n");
	} else {

		// Bit-Size is valid, i.e. > 1
		mpz_t lower_limit;
		mpz_init(lower_limit);

		// Setting a lower limit for the prime, which is 2^(n-1)
		mpz_ui_pow_ui(lower_limit, 2, mpz_get_ui(n)-1);

		// Generating random prime

		/*
		Keeping two things in mind - 
			1) Prime should be greater than lower limit
			2) It should pass probable prime testing method
		*/
		while (1) {
			mpz_urandomb(random, state ,mpz_get_ui(n));

			if (mpz_cmp(random, lower_limit) > 0 && mpz_probab_prime_p(random,mpz_get_ui(n))) {
				mpz_set(result,random);
				break;
			}
		}
	}

	/*
		END of GENERATING PRIME of BITSIZE n
		Prime is stored in result
	*/
}


void setup(setup_result* retval, mpz_t security_parameter) {

	/*

	Setup (1^lambda) : 

		PURPOSE : To setup the system and define key parameters to establish a group signature scheme.
				  We are assuming to support upto 2^k signatures in the group, and sign messages in {0,1}^m.
				  Here; k, m = O(lambda)

		INPUT : A security parameter (1^lambda), in unary.

		ALGORITHM : COMMENTED STEP BY STEP INSIDE THE CODE ITSELF

		OUTPUT : 
			1) Public Parameters (PP)
			2) Master Enrollment Key (MK)
			3) Group Manager's tracing Key (TK)

	*/

	mpz_t k,m;
	mpz_init(k);
	mpz_init(m);

	// Initializing 'k' and 'm' as lambda (security parameter provided in the input), as described in the PURPOSE section
	mpz_set(k, security_parameter);
	mpz_set(m, security_parameter);

	mpz_init(retval->mval);
	mpz_set(retval->mval, m);

	mpz_t p_bits, q_bits;
	mpz_init(p_bits);
	mpz_init(q_bits);

	// Setting 'bit sizes' of primes p and q
	mpz_add_ui(p_bits, k, 2);
	mpz_add_ui(q_bits, k, 3);

	mpz_t p,q;
	mpz_init(p);
	mpz_init(q);
	mpz_init(retval->pval);
	mpz_init(retval->qval);

	// Initializing random prime 'p' of bit size p_bits (defined earlier)
	random_prime_bits(p, p_bits);

	// Initializing random prime 'q' of bit size q_bits (defined earlier)
	// The fact that p and q should not be same, is taken care of via following do-while loop
	do {
		random_prime_bits(q, q_bits);
	} while(mpz_cmp(p,q) == 0);

	mpz_t n;
	mpz_init(n);

	// Define 'n' as 'p X q'
	mpz_mul(n, p, q);
	mpz_init(retval->n);
	mpz_set(retval->n, n);
	gmp_printf("N = %Zd\n", n);
	gmp_printf("P = %Zd\n", p);
	gmp_printf("Q = %Zd\n", q);
	mpz_set(retval->pval, p);
	mpz_set(retval->qval, q);

	pairing_t pairing;
	pbc_param_t par;
	
	// Create a 'pairing' of order 'n'
	pbc_param_init_a1_gen(par, n);
	pbc_param_init_a1_gen(retval->p, n);
	pairing_init_pbc_param(pairing, par);

	element_t g1, gt1, identity, h, add, temp, mk0;

	// Setting up / defining elements (identity, generators, etc.) of 'pairing', an algebraic structure
	// Using pre-defined functions starting with 'element_init_**'
	pairing_init_pbc_param(retval->pairing, par);

	// Symmetric pairing (G1 = G2 = g1)
	// g1 here is a generator of 'pairing'
	element_init_G1(g1, pairing);
	element_init_G2(g1, pairing);
	element_init_GT(gt1, pairing);

	element_init_G1(add, pairing);
	element_init_G1(temp, pairing);
	element_init_G1(h, pairing);
	element_init_G1(identity, pairing);
	element_init_G1(retval->G, pairing);
	element_init_GT(retval->A_val, pairing);

	// Master Enrollment Key
	element_init_G2(mk0, pairing);

	element_set0(identity);
	element_init_G1(retval->identity, pairing);
	element_set0(retval->identity);
	element_set(retval->G, g1);

	// Defining a generator h of subgroup Gq of G
	do {
		element_random(g1);
		element_pow_mpz(h, g1, p);
	} while(element_cmp(h, identity) == 0);

	// Defining the Sub-group Gq
	element_init_G1(retval->gen_subgroup_q, pairing);
	element_set(retval->gen_subgroup_q, h);

	mpz_t required, gen;
	mpz_init(required);
	mpz_init(gen);

	// m+3 generators required
	mpz_add_ui(required, m, 3);

	// Drawing m+2 random generators of 'pairing' (one is already created, 'g1')
	element_t* generators = (element_t*)malloc(sizeof(element_t)*(3+mpz_get_ui(m)));

	for (unsigned long int i = 0; i < (3+mpz_get_ui(m)); i++) {
		element_init_G1(generators[i], pairing);
	}

	unsigned long long int index = 0;

	// Defining all the generators
	do {
		element_random(g1);
		element_pow_mpz(temp, g1, n);

		if (element_cmp(temp, identity) == 0) {
			element_pow_mpz(temp, g1, p);

			if (element_cmp(temp, identity)) {
				element_pow_mpz(temp, g1, q);

				if (element_cmp(temp, identity)) {
					mpz_add_ui(gen, gen, 1);
					element_set(generators[index], g1);
					index++;
				}
			}
		}

	} while(mpz_cmp(gen, required));

	retval->generators = generators;

	// Next, pick two random exponents ('alpha', 'omega'), belongs to Zn
	mpz_t alpha, omega;
	mpz_init(alpha);
	mpz_init(omega);
	gmp_randstate_t state;
	gmp_randinit_default(state);
	gmp_randseed_ui(state, (rand()+1)*(rand()+1));
	mpz_t gcd_alpha_p, gcd_alpha_q;
	mpz_init(gcd_alpha_p);
	mpz_init(gcd_alpha_q);

	// Generating 'alpha'
	// Making sure 'alpha' is co-prime to both 'p' and 'q'
	do{
		mpz_urandomm(alpha, state, n);
		mpz_gcd(gcd_alpha_p, alpha, p);
		mpz_gcd(gcd_alpha_q, alpha, q);

	} while(mpz_cmp_ui(gcd_alpha_p, 1) != 0 || mpz_cmp_ui(gcd_alpha_q, 1) != 0);

	// Generating 'omega'
	mpz_urandomm(omega, state, n);
	mpz_init(retval->omega);
	mpz_set(retval->omega, omega);

	gmp_printf("Alpha = %Zd\nOmega = %Zd\n", alpha, omega);
	mpz_init(retval->alpha);
	mpz_set(retval->alpha, alpha);

	// 1) Set, PP = (g1, h, all m+2 generators, g1^omega)
	element_pow_mpz(g1, generators[0], omega);
	element_init_G1(retval->B_Omega, pairing);
	element_set(retval->B_Omega, g1);

	// 2) Set, MK = (g1^alpha, omega)
	element_pow_mpz(mk0, generators[0], alpha);
	element_init_G1(retval->mk0, pairing);
	element_set(retval->mk0, mk0);
	mpz_init(retval->mk1);
	mpz_set(retval->mk1, omega);

	// 3) Set, TK = q
	mpz_init(retval->tk);
	mpz_set(retval->tk, q);

	// Now, all the required outputs (PP, MK, TK) are set.

	/*
	END of SETUP phase
	*/ 
}


static int num_user;
int add_user_val;


void enroll(mpz_t final_sid, mpz_t userID, element_t k1, element_t k2, element_t k3) {

	/*
		PURPOSE : Create a Signing Key of User ID defined by 'userID'

		INPUT : 
			1) User ID (0 <= ID < 2^k < p)
			2) Signing Key Pair - 
				i) k1 (to be determined)
				ii) k2 (to be determined)
				iii) k3 (to be determined)

		OUTPUT : (k1, k2, k3)

		ALGORITHM : Given step by step INSIDE code itself
	*/

	mpz_t gcd, sid;
	mpz_init(gcd);
	mpz_init(sid);
	mpz_gcd(gcd, userID, ret_setup.n);
	assert(mpz_cmp_ui(gcd,1) == 0);

	mpz_t val;
	mpz_init(val);
	mpz_set(val, ret_setup.pval);

	// Setting 'val' to max(p, q)
	if (mpz_cmp(ret_setup.pval,ret_setup.qval) > 0) {
		mpz_set(val, ret_setup.qval);
	}

	// Choose a valid SID

	/*
	Things to keep in mind - 
		1) (omega + sid) lies in multiplicative group modulo 'n'
	*/
	while (1) {
		mpz_add(sid, userID, ret_setup.omega);
		mpz_mod(sid, sid, ret_setup.n);
		mpz_gcd(gcd, sid, ret_setup.n);

		num_user += 1;

		// If condition is satisfied, then 'sid' is found
		if (mpz_cmp_ui(gcd, 1) == 0) {
			break;
		}

		// Else, update userID
		mpz_add_ui(userID, val, num_user);
	}

	mpz_t inverse;
	mpz_init(inverse);

	// Calculating 'inverse' = (sid)^(-1) mod n
	assert(mpz_invert(inverse, sid, ret_setup.n));

	gmp_printf("sid (not to be disclosed to user): %Zd\n", userID);

	mpz_init(final_sid);
	mpz_set(final_sid, userID);
	element_init_G1(k1, ret_setup.pairing);
	element_init_G1(k2, ret_setup.pairing);
	element_init_G1(k3, ret_setup.pairing);

	// Set, k1 = (g^alpha)^inverse
	element_pow_mpz(k1, ret_setup.generators[0], ret_setup.alpha);
	element_pow_mpz(k1, k1, inverse);

	// Set, k2 = g^userID, g = first generator of 'pairing'
	element_pow_mpz(k2, ret_setup.generators[0], userID);

	// Set, k3 = u^userID, u = second generator of 'pairing'
	element_pow_mpz(k3, ret_setup.generators[1], userID);

	/*
		END of ENROLL
		All, k1, k2, and k3 (Signing Key Triples) have been set
	*/
}


void sign(element_t pi1, element_t pi2, element_t sigma1, element_t sigma2, element_t sigma3, element_t sigma4, element_t k1, element_t k2, element_t k3, char* message) {
	
	/*
		PURPOSE : To Sign a Message 'message' with a Signing Key Kid ('k1', 'k2', 'k3')

		INPUT : 
			1) Final Signature Components
				a) pi1 
				b) pi2
				c) sigma1
				d) sigma2
				e) sigma3
				f) sigma4

			2) Signing Key
				a) k1
				b) k2
				c) k3

			3) Message
				- 'message' (m-bit message)

		OUTPUT : 
			Final Signature tuples (pi1, pi2, sigma1, sigma2, sigma3, sigma4)

		ALGORITHM : Given step by step INSIDE the code itself
	*/

	mpz_t s, t1, t2, t3, t4, t_temp;
	mpz_init(s);
	mpz_init(t1);
	mpz_init(t2);
	mpz_init(t3);
	mpz_init(t4);
	mpz_init(t_temp);
	gmp_randstate_t state;
	gmp_randinit_default(state);
	gmp_randseed_ui(state, (rand()+1)*(rand()+1));
	mpz_urandomm(s, state, ret_setup.n);

	/*
		Setting up two-level hybrid, unblinded signature quadriples 
		(theta1, theta2, theta3, theta4)
	*/
	element_t theta3, val1;


	element_init_G1(theta3, ret_setup.pairing);
	element_init_G1(val1, ret_setup.pairing);

	// Set, theta3 = v'; where v' is the third generator, initially 
	element_set(theta3, ret_setup.generators[2]);
	element_t temp_pw;
	element_init_G1(temp_pw, ret_setup.pairing);
	mpz_t msg_val;
	mpz_init(msg_val);

	// Compute, theta3 as; theta3 *= ( product of all m generaotrs starting
	// from 4th raised individually to the power of corresponding message bits (starting from zero) )
	for (int i = 3; i < (3+mpz_get_ui(ret_setup.mval)); i++) {

		if (message[i-3] == '1') {
			mpz_set_ui(msg_val,1);
		} else {
			mpz_set_ui(msg_val, 0);
		}

		element_pow_mpz(temp_pw, ret_setup.generators[i], msg_val);
		element_mul(theta3, theta3, temp_pw);
	}

	element_set(val1, theta3);

	// Set, theta3 *= s; where, s = random belongs to Zn
	element_pow_mpz(theta3, theta3, s);

	/*
		 ----------------------------------
		| Set final 'theta3' = theta3 * K3 |
		 ----------------------------------
	*/
	element_mul(theta3, theta3, k3);

	element_t theta4;
	element_init_G1(theta4, ret_setup.pairing);

	// Set, theta4 = g^(-s); where, g = first generator, and s is previously defined random
	element_set(theta4, ret_setup.generators[0]);
	element_pow_mpz(theta4, theta4, s);
	element_invert(theta4, theta4);
	element_t ver1, ver2, ver3;

	// Verifications of theta3 and theta4, whether they are well formed
	element_init_GT(ver1, ret_setup.pairing);
	element_init_GT(ver2, ret_setup.pairing);
	element_init_GT(ver3, ret_setup.pairing);
	element_pairing(ver1, theta3, ret_setup.generators[0]);
	element_pairing(ver2, theta4, val1);
	element_mul(ver1, ver1, ver2);
	element_pairing(ver3, k2, ret_setup.generators[1]);

	if (element_cmp(ver1, ver3) == 0) {
		printf("-----------------Verification of initial signature successful------------------\n");
	} else {
		printf("Verification of initial signature UNSUCCESSFUL\n");
	}

	//End of verification of theta3 and theta4

	// Generating 4 random expinents, t1, t2, t3, t4; all belongs to Zn 
	mpz_urandomm(t1, state, ret_setup.n);
	mpz_urandomm(t2, state, ret_setup.n);
	mpz_urandomm(t3, state, ret_setup.n);
	mpz_urandomm(t4, state, ret_setup.n);

	element_t h, temp;

	/*
		Now, all thetas are to be turned into a blinded signature that 
		is both verificable and traceable, but remains anonymous to anyone
		who lacks the tracing Key
	*/
	element_init_G1(sigma1, ret_setup.pairing);
	element_init_G1(sigma2, ret_setup.pairing);
	element_init_G1(sigma3, ret_setup.pairing);
	element_init_G1(sigma4, ret_setup.pairing);
	element_init_G1(h, ret_setup.pairing);
	element_init_G1(temp, ret_setup.pairing);
	element_set(h, ret_setup.gen_subgroup_q);
	element_set(sigma1, k1);
	element_set(sigma2, k2);
	element_set(sigma3, theta3);
	element_set(sigma4, theta4);
	element_pow_mpz(temp, h, t1);

	// Setting, 'sigma1' = K1 * (h ^ (t1)); h = generator of Gq //
	element_mul(sigma1, temp, sigma1);
	element_pow_mpz(temp, h, t2);

	// Setting, 'sigma2' = K2 * (h ^ (t2)); h = generator of Gq //
	element_mul(sigma2, temp, sigma2);
	element_pow_mpz(temp, h, t3);

	// Setting, 'sigma3' = theta3 * (h ^ (t3)); h = generator of Gq //
	element_mul(sigma3, temp, sigma3);
	element_pow_mpz(temp, h, t4);

	// Setting, 'sigma4' = theta4 * (h ^ (t4)); h = generator of Gq //
	element_mul(sigma4, temp, sigma4);

	element_t theta1, theta2, u;
	element_init_G1(pi1, ret_setup.pairing);
	element_init_G1(pi2, ret_setup.pairing);
	element_init_G1(theta1, ret_setup.pairing);
	element_init_G1(theta2, ret_setup.pairing);
	element_init_G1(u, ret_setup.pairing);

	// Setting up, theta1 = K1 and theta2 = K2
	element_set(theta1, k1);
	element_set(theta2, k2);
	// u = Second generator of G
	element_set(u, ret_setup.generators[1]);
	mpz_mul(t_temp, t1, t2);
	element_pow_mpz(h, h, t_temp);
	element_pow_mpz(theta1, theta1,t2);
	element_mul(theta2, theta2, ret_setup.B_Omega);
	element_pow_mpz(theta2, theta2, t1);
	element_mul(pi1, theta1, h);

	// SET, pi1 = h^(t1*t2) * (theta1)^t2 * (theta2*omega)^t1 //
	element_mul(pi1, pi1, theta2);
	element_pow_mpz(pi2, u, t2);
	element_pow_mpz(u, ret_setup.generators[0], t3);
	element_invert(u, u);

	// SET, pi2 = u^t2 * g^(-t3) * val1^(t4);
	// where, val1 = ( product of all m generaotrs starting
	// from 4th raised individually to the power of corresponding message bits (starting from zero) )
	element_mul(pi2, pi2, u);
	element_pow_mpz(val1, val1, t4);
	element_invert(val1, val1);
	element_mul(pi2, pi2, val1);

	/*
		END of MESSAGE SIGNING
		(pi1, pi2, sigma1, sigma2, sigma3, sigma4) is created
	*/
}


void verify(element_t Aval, element_t sigma1, element_t sigma2, element_t sigma3, element_t sigma4, element_t pi1, element_t pi2, char* message) {
	
	/*
		PURPOSE : To validate a group signature sigma on a message

		INPUT : 
			1) Group Signature
				a) sigma1
				b) sigma2
				c) sigma3
				d) sigma4
				e) pi1
				f) pi2

			2) Message
				- 'message' ('m' bits)

		OUTPUT : NONE (prints "VALID" (or) "INVALID")

		ALGORITHM : Given step by step INSIDE the code itself
	*/

	element_t Acopy, val1, val2, pairing_result1, pairing_result2, T1, T2;

	/*
		Calculate T1 and T2
	*/
	element_init_G1(val2, ret_setup.pairing);
	element_init_G1(val1, ret_setup.pairing);
	element_init_GT(Acopy, ret_setup.pairing);
	element_init_GT(pairing_result1, ret_setup.pairing);
	element_init_GT(pairing_result2, ret_setup.pairing);
	element_init_GT(T1, ret_setup.pairing);
	element_init_GT(T2, ret_setup.pairing);
	element_set(Acopy, Aval);

	// A = A^(-1)
	element_invert(Acopy, Acopy);

	// val1 = sigma2*omega
	element_mul(val1, sigma2, ret_setup.B_Omega);

	// T1 = e(sigma1, val1)
	element_pairing(T1, sigma1, val1);

	/*
		 ------------------------------------------------
		| Finally, T1 = A^(-1) * e(sigma1, sigma2*omega) |
		 ------------------------------------------------
	*/
	element_mul(T1, T1, Acopy);

	element_set(val2, ret_setup.generators[2]);
	element_t temp_pw;
	element_init_G1(temp_pw, ret_setup.pairing);
	mpz_t msg_val;
	mpz_init(msg_val);

	// Setting, val2 = 2nd generator * (product of all m generaotrs starting
	// from 4th raised individually to the power of corresponding message bits (starting from zero))
	for (int i = 3; i < (3+mpz_get_ui(ret_setup.mval)); i++) {
		if (message[i-3] == '1') {
			mpz_set_ui(msg_val,1);
		} else {
			mpz_set_ui(msg_val, 0);
		}

		element_pow_mpz(temp_pw, ret_setup.generators[i], msg_val);
		element_mul(val2, val2, temp_pw);
	}

	// T2 = e(sigma2, u); where, u = 2nd generator
	element_pairing(T2, ret_setup.generators[1],sigma2);

	// pairing_result2 = e(sigma3, g); where, g = first generator
	element_pairing(pairing_result2, ret_setup.generators[0], sigma3);
	// pairing_result2 = pairing_result2^(-1)
	element_invert(pairing_result2, pairing_result2);

	// T2 = T2 * pairing_result2
	element_mul(T2, T2, pairing_result2);

	// pairing_result2 = e(sigma4, val2)
	element_pairing(pairing_result2, sigma4, val2);

	/*
		 ---------------------------------------------------------------------
		| Finally set up T2 = e(sigma2,u) * e(sigma3,g)^(-1) * e(sigma4*val2) |
		 ---------------------------------------------------------------------
	*/
	element_mul(T2, T2, pairing_result2);
	element_t T1_verify, T2_verify;
	element_init_GT(T1_verify, ret_setup.pairing);
	element_pairing(T1_verify, ret_setup.gen_subgroup_q, pi1);
	element_init_GT(T2_verify, ret_setup.pairing);
	element_pairing(T2_verify, ret_setup.gen_subgroup_q, pi2);


	/*
	Verifying two conditions - 
		1) T1 == e(h, pi1)
		2) T2 == e(h, pi2)
	*/
	if (element_cmp(T1, T1_verify) == 0 && element_cmp(T2, T2_verify) == 0) {
		printf("---------------------VERIFICATION VALID-------------------------\n");
	} else {
		printf("VERIFICATION INVALID\n");
	}

	/*
		END of VERIFICATION
	*/
}


void trace(element_t sigma2, mpz_t* sids, unsigned long num_of_users) {

	/*
		PURPOSE : Tracing authority recovers the identity of the Signer

		INPUT : 
			1) Signature (sigma2)
			2) Array of SIDs
			3) Number of users (length of SID array)

		OUTPUT : NONE (print "successful" or "unsuccessful")

		ALGORITHM : Given step by step INSIDE the code itself
	*/

	element_t sigma2_copy, val;
	element_init_G1(sigma2_copy, ret_setup.pairing);
	element_init_G1(val, ret_setup.pairing);
	element_set(sigma2_copy, sigma2);
	element_pow_mpz(sigma2_copy, sigma2_copy, ret_setup.tk);

	// For each user
	for (unsigned long i = 0; i < (num_of_users); i++) {

		/*
			Condition of successful tracing - 
				1) sigma2^(q) == (g ^ (SID[i])) ^ q;
				where, q = order of Gq, SID[i] = SID of ith user
		*/

		element_pow_mpz(val, ret_setup.generators[0], sids[i]);
		element_pow_mpz(val, val, ret_setup.tk);

		if (element_cmp(val, sigma2_copy) == 0) {
			gmp_printf("----------------------------SID %Zd traced successfully--------------------------\n", sids[i]);
		} else {
			gmp_printf("----------------------------SID %Zd unsuccessful in passing trace test--------------------------\n", sids[i]);
		}
	}

	/*
		END of TRACING SIGNER
	*/
}


int main (int argc, char **argv) {
	/*
		MAIN FUNCTION
	*/

	num_user = 0;
	srand(time(NULL));
	mpz_t security_parameter;
	mpz_init(security_parameter);

	// Initializing security parameter
	mpz_set_ui(security_parameter, 6);

	// Setting up PP, MK, and TK, calling user-defined setup function
	// All output parameters stored in 'ret_setup'
	setup(&ret_setup, security_parameter);

	/*
		Retreiving and printing all setup parameters above
	*/

	printf("PUBLIC INFORMATION:\n");
	gmp_printf("N: %Zd\n", ret_setup.n);
	printf("G: ");

	element_t grp, add;
	element_init_G1(grp, ret_setup.pairing);
	element_init_G1(add, ret_setup.pairing);
	element_set(grp, ret_setup.generators[0]);
	element_set(add, grp);

	printf("FOR e and GT, the pairing parameters are as follows:\n");
	pbc_param_out_str(stdout, ret_setup.p);

	element_t Aval;
	element_init_GT(Aval, ret_setup.pairing);
	element_pairing(Aval, ret_setup.generators[0], ret_setup.generators[0]);
	element_pow_mpz(Aval, Aval, ret_setup.alpha);
	// A
	printf("A: ");
	element_printf("%B\n", Aval);
	// OMEGA
	printf("OMEGA: ");
	element_printf("%B\n", ret_setup.B_Omega);
	// MK
	printf("MASTER KEY: ");
	element_printf("%B, ",ret_setup.mk0);
	gmp_printf("%Zd\n", ret_setup.mk1);
	// TK
	printf("TRACING KEY: ");
	gmp_printf("%Zd\n", ret_setup.qval);

	add_user_val = rand()%6+1;

	mpz_t random, userID;
	mpz_init(random);
	mpz_init(userID);
	gmp_randstate_t state;
	gmp_randinit_default(state);
	gmp_randseed_ui(state, (rand()+1)*(rand()+1));

	mpz_t count, limit;
	mpz_init(count);
	mpz_init(limit);
	mpz_set_ui(limit, 1);

	while(mpz_cmp(count, security_parameter)) {
		mpz_mul_ui(limit, limit, 2);
		mpz_add_ui(count, count, 1);
	}

	unsigned long num_of_users = 10;
	// Initializing SID's for defined 'num_of_users
	mpz_t* sids = (mpz_t*)malloc(sizeof(mpz_t)*num_of_users);

	// Enrollment of all users
	for (unsigned long i = 0; i < num_of_users;i++) {

		// Signing Key (k1, k2, k3)
		element_t k1, k2, k3;
		mpz_init(sids[i]);

		// Generating random user ID
		// User ID should not be 0, p, (or) q
		do {
			mpz_urandomm(userID, state, limit);
		} while(mpz_cmp_ui(userID, 0) == 0 || mpz_cmp(userID, ret_setup.pval) == 0 || mpz_cmp(userID, ret_setup.qval) == 0);

		// Function Call for Enrollment
		enroll(sids[i], userID, k1, k2, k3);
	}

	element_t k1, k2, k3;

	/*
		 ----------------------------------------------------------------
		| Demonstration of SIGNING and TRACING / VERIFYING algorithms for|
		| a particular User ID 											 |
		 ----------------------------------------------------------------
	*/
	gmp_printf("------------------Demonstrating for USERID - %Zd-----------------\n", userID);
	mpz_t sid;
	mpz_init(sid);

	/*
		 ---------------------
		| Step 1 - Enrollment |
		 ---------------------
	*/
	enroll(sid, userID, k1, k2, k3);
	// Printing k1, k2, and k3
	element_printf("K1: %B\nK2: %B\nK3: %B\n", k1, k2, k3);
	element_t val1, val2, val3, val4;

	// Setting up all the parameters required
	element_init_G1(val4, ret_setup.pairing);
	element_init_GT(val1, ret_setup.pairing);
	element_init_GT(val2, ret_setup.pairing);
	element_init_GT(val3, ret_setup.pairing);
	element_pairing(val1, k2, ret_setup.generators[1]);
	element_pairing(val2, k3, ret_setup.generators[0]);
	element_mul(val4, k2, ret_setup.B_Omega);
	element_pairing(val3, k1, val4);

	// Checking whether new-enrolled Key is well-formed

	/*
		Conditions - 
			1) e(K1, K2*omega) == A; where, A = e(g, g)^alpha
			2) e(K2, u) == e(K3, g)
	*/
	if (element_cmp(val1, val2) == 0 && element_cmp(val3, Aval) == 0) {
		printf("--------------------Verification of key successful - key well formed by enroll()----------------------------\n");
	} else {
		printf("Verification of key UNSUCCESSFUL - key not well formed by enroll()\n");
	}

	// Setting up a message to sign for the user
	char* msg = (char*)malloc(sizeof(char)*(1+mpz_get_ui(ret_setup.mval)));
	for (unsigned int i = 0; i < mpz_get_ui(ret_setup.mval); i++) {
		int b = rand()%2;
		msg[i] = '1';
		if (b == 0) {
			msg[i] = '0';
		}
	}

	msg[mpz_get_ui(ret_setup.mval)] = '\0';
	printf("Message (m bits): %s\n", msg);

	element_t sigma1, sigma2, sigma3, sigma4, pi1, pi2;

	/*
		 ------------------
		| Step 2 - Signing |
		 ------------------
	*/
	sign(pi1, pi2, sigma1, sigma2, sigma3, sigma4, k1, k2, k3, msg);

	// Printing the signature
	element_printf("Final Signature:\nSigma1: %B\nSigma2: %B\nSigma3: %B\nSigma4: %B\nPi1: %B\nPi2: %B\n",sigma1, sigma2, sigma3, sigma4, pi1, pi2);
	
	/*
		 -----------------
		| Step 3 - Verify |
		 -----------------
	*/
	verify(Aval, sigma1, sigma2, sigma3, sigma4, pi1, pi2, msg);

	/*
		 ----------------
		| Step 4 - Trace |
		 ----------------
	*/
	trace(sigma2, sids, num_of_users);
	return 0;

	/*
		END OF MAIN
	*/
}
