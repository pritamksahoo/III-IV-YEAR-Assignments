#include <iostream>
#include <cmath>

#define ll long long

using namespace std;

ll calc_inverse(ll num, ll mod);
ll fast_exponent(ll num, ll exp, ll mod);
ll calc_phi(ll num);

int main()
{
	ll N, e, d, M, C[2];
	cin >> C[0];
	cin >> e;
	cin >> N;
	cin >> C[1];
	d = calc_inverse(e, calc_phi(N));
// 	N = 77, e = 13, d = 37;

    for (int i=0; i<2; i++)
    {
    	ll modfd_C = (C[2-i-1]*fast_exponent(2,e,N))%N;
    	ll pt = fast_exponent(modfd_C, d, N);
    
    	ll inv = calc_inverse(2, N);
    
    	ll answer = (pt*inv)%N;
    
    	cout << answer << endl;
    }

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

	if (t1 < 0)
	{
		t1 += mod;
	}

	return t1;
}

ll fast_exponent(ll num, ll exp, ll mod)
{
	ll ret = 1, base = num;

	while (exp != 0)
	{
		int rem = exp%2;
		if (rem == 1)
		{
			ret = (ret*base)%mod;
		}
		base = (base*base)%mod;
		exp /= 2;
	}

	return ret;
}

ll calc_phi(ll num)
{
	ll n1, n2, root = sqrt(num);
	for (ll i=2; i<root; i++)
	{
		if (num%i == 0)
		{
			n1 = i, n2 = num/n1;
			break;
		}
	}

	return (n1-1)*(n2-1);
}