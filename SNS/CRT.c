#include <stdio.h>

#define ll long long
#define MAX 100

ll solve_CRT(ll remainder[], ll modulus[], int no);
ll calc_inverse(ll num, ll mod);

int main()
{
	ll remainder[MAX], modulus[MAX];
	int no, i;
	ll answer;

	scanf("%d", &no);
	for (i=0; i<no; i++)
	{
		scanf("%lld %lld", &remainder[i], &modulus[i]);
	}

	answer = solve_CRT(remainder, modulus, no);
	printf("\nSolution : %lld\n\n", answer);
}

ll calc_inverse(ll num, ll mod)
{
	ll t1, t2, t, q, r, r1, r2;
	t1 = 0, t2 = 1;
	r1 = mod, r2 = num;

	while (r2 != 0)
	{
		q = r1/r2;
		r = r1%r2;

		t = t1 - q*t2;

		r1 = r2, r2 = r;
		t1 = t2, t2 = t;
	}

	return t1;
}

ll solve_CRT(ll remainder[], ll modulus[], int no)
{
	ll M[MAX], inv_M[MAX];
	ll mult = 1, ret = 0;
	int i;

	for (i=0; i<no; i++)
	{
		mult *= modulus[i];
	}

	for (i=0; i<no; i++)
	{
		if (remainder[i] != 0)
		{
			M[i] = mult/modulus[i];
			inv_M[i] = calc_inverse(M[i], modulus[i]);

			ret = (ret + remainder[i]*M[i]*inv_M[i])%mult;
		}
	}

	if (ret < 0)
	{
		ret += mult;
	}

	return ret;

}