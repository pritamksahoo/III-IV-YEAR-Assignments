#include <stdio.h>
#include <ctype.h>
#include <string.h>
#define MAX 4
#define MODD 26

int calc_gcd(int a, int b)
{
    int r, r1 = a, r2 = b;
    while (r2 != 0)
    {
        r = r1%r2;
        r1 = r2;
        r2 = r;
    }
    return r1;
}


int calc_mult_inverse(int num, int modulus)
{
    int q, r, r1, r2, s1, s2, s;
    r1 = num, r2 = modulus, s1 = 1, s2 = 0;
    
    while (r2 != 0)
    {
        q = r1/r2;
        
        r = r1%r2;
        r1 = r2;
        r2 = r;
        
        s = s1 - q*s2;
        s1 = s2;
        s2 = s;
    }
    // printf("s1 = %d\n", s1);
    s1 %= modulus;
    if (s1 < 0)
    {
        s1 += modulus;
    }
    
    return s1;
}

int solve_one_part(int lhs, int rhs, int k[])
{
    int gcd, inv, i, index;
    lhs %= MODD, rhs %= MODD;
    if (lhs < 0) { lhs += MODD; }
    if (rhs < 0) { rhs += MODD; }
    // printf("lhs = %d, rhs = %d\n", lhs, rhs);
    gcd = calc_gcd(lhs, MODD);
    rhs /= gcd;
    inv = calc_mult_inverse(lhs/gcd, MODD/gcd);
    
    index = 0;
    rhs = (rhs*inv)%(MODD/gcd);
    if (rhs < 0) { rhs += (MODD/gcd); }
    for (i = 0; i < gcd; i++)
    {
        k[index++] = (rhs + i*(MODD/gcd))%MODD;
    }
    return index;
}

int solve(int mat[][3], int key[][2])
{
    int lcm, m[2][2] = {0}, lhs, rhs, mi[2], gcd, i, j, index, inv, k1[10], k2[10], no_k1, no_k2;
    // For K1
    lcm = (mat[0][1]*mat[1][1])/calc_gcd(mat[0][1], mat[1][1]);
    
    m[0][0] = mat[0][0]*(lcm/mat[0][1]), m[0][1] = mat[0][2]*(lcm/mat[0][1]);
    m[1][0] = mat[1][0]*(lcm/mat[1][1]), m[1][1] = mat[1][2]*(lcm/mat[1][1]);

    lhs = m[0][0] - m[1][0], rhs = m[0][1] - m[1][1];
    
    no_k1 = solve_one_part(lhs, rhs, k1);
    
    index = 0;
    for (i=0; i<no_k1; i++)
    {
        // For K2
        lhs = mat[1][1];
        rhs = mat[1][2] - mat[1][0]*k1[i];
        no_k2 = solve_one_part(lhs, rhs, k2);
        
        for (j=0; j<no_k2; j++)
        {
            key[index][0] = k1[i], key[index][1] = k2[j];
            index++;
        }
    }
    return index;
}


int main(){
    char C[MAX*MAX], P[MAX*MAX];
    int cipher[MAX], plain[MAX], i, mat[2][3] = {0}, found = 0, k, j, ans, index;
    int key12[10][2] = {0}, key34[10][2] = {0}, ascii, len_k1, len_k2, temp[4];
    
    fgets(P, MAX*MAX, stdin);
    
    i = 0, index = 0;
    while (P[i] != '\0')
    {
        ascii = (int)(P[i]);
        if ((ascii > 64 && ascii < 91) || (ascii > 96 && ascii < 123))
        {
            plain[index++] = (int)(toupper(P[i])) - (int)('A') + 1;
        }
        i++;
        if (index == 4) { break; }
    }
    
    fgets(C, MAX*MAX, stdin);
    
    i = 0, index = 0;
    while (C[i] != '\0')
    {
        ascii = (int)(C[i]);
        if ((ascii > 64 && ascii < 91) || (ascii > 96 && ascii < 123))
        {
            cipher[index++] = (int)(toupper(C[i])) - (int)('A') + 1;
        }
        i++;
        if (index == 4) { break; }
    }
    
    label:
    // For k1 and k2
    mat[0][0] = plain[0], mat[0][1] = plain[1], mat[0][2] = cipher[0];
    mat[1][0] = plain[2], mat[1][1] = plain[3], mat[1][2] = cipher[2];
    
    len_k1 = solve(mat, key12);
    
    // For k3 and k4
    mat[0][0] = plain[0], mat[0][1] = plain[1], mat[0][2] = cipher[1];
    mat[1][0] = plain[2], mat[1][1] = plain[3], mat[1][2] = cipher[3];
    
    len_k2 = solve(mat, key34);
    
    found = 0;
    for (i = 0; i < len_k1 && found == 0; i++)
    {
        for (j = 0; j < len_k2 && found == 0; j++)
        {
            if (calc_gcd((key12[i][0]*key34[j][1] - key12[i][1]*key34[j][0]), MODD) == 1)
            {
                // Printing Answer
                printf("%d %d %d %d", key12[i][0], key12[i][1], key34[j][0], key34[j][1]);
                found = 1;
                break;
            }
        }
    }
    if (found == 0)
    {
        for (i=0; i < 4; i++)
        {
            temp[i] = plain[i];
        }
        for (i=0; i < 4; i++)
        {
            plain[i] = cipher[i];
        }
        for (i=0; i < 4; i++)
        {
            cipher[i] = temp[i];
        }
        goto label;
    }
}