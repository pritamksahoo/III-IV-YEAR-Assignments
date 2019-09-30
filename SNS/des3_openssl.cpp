#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/des.h>

/*
Run the code by typing in terminal the following command :
g++ des3_openssl.cpp -lssl -lcrypto
./a.out
*/

/* Print Encrypted and Decrypted data packets */
void print(const void* data, int len)
{
    const unsigned char * p = (const unsigned char*)data;
    int i = 0;
    
    for (; i<len;++i)
        printf("%02X ", *p++);
    
    printf("\n");
}

int main()
{
    // Hexadecimal input
    unsigned char input_data[] = {0xf1, 0xa2, 0x03, 0xb4, 0x05};
    // Buffers for storing cipher (After encryption) and plain text (After decryption)
    unsigned char* cipher[sizeof(input_data)];
    unsigned char* text[sizeof(input_data)];
    // Initial vector
    DES_cblock iv = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
    DES_set_odd_parity(&iv);

    // Triple DES key for Encryption and Decryption 
    DES_cblock Key1 = { 0x11, 0x22, 0x11, 0x11, 0x31, 0x11, 0x01, 0x11 };
    DES_cblock Key2 = { 0x22, 0xb2, 0x22, 0x22, 0x2d, 0x22, 0x22, 0x22 };
    DES_cblock Key3 = { 0x33, 0x13, 0x33, 0x33, 0x03, 0x33, 0x3e, 0x33 };
    DES_key_schedule SchKey1,SchKey2,SchKey3;
    
    /* Check for Weak key generation */
    if ((DES_set_key_checked(&Key1, &SchKey1) || DES_set_key_checked(&Key2, &SchKey2) || DES_set_key_checked(&Key3, &SchKey3)) == -2)
    {
        printf("Weak key ....\n");
        return 1;
    }
    else
    {
        // Triple-DES CBC Encryption 
        DES_ede3_cbc_encrypt( (unsigned char*)input_data, (unsigned char*)cipher, sizeof(input_data), &SchKey1, &SchKey2, &SchKey3,&iv, DES_ENCRYPT);
        
        // Triple-DES CBC Decryption 
        memset(iv,0,sizeof(DES_cblock));
        DES_set_odd_parity(&iv);
        DES_ede3_cbc_encrypt( (unsigned char*)cipher, (unsigned char*)text, sizeof(input_data), &SchKey1, &SchKey2, &SchKey3,&iv,DES_DECRYPT);
        
        /* Printing and Verifying */
        printf("\nOriginal plain text : \n");
        print(input_data,sizeof(input_data));
        printf("\nEncrypted cipher text : \n");
        print(cipher,sizeof(input_data));
        printf("\nDecrypted plain text : \n");
        print(text,sizeof(input_data));
        printf("\n");
        return 0;
    }
}