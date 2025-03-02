#include <iostream>
#include <gmp.h>
#include <cstdlib>
#include <ctime>
#include <fstream>

void generateKeys(mpz_t e, mpz_t d, mpz_t n) {
    // setting state and seed
    gmp_randstate_t state;
    gmp_randinit_default(state);
    gmp_randseed_ui(state, time(0));

    // initializing required variables
    mpz_t p, q, phi, temp1, temp2, range, gcd;
    mpz_inits(p, q, phi, temp1, temp2, range, gcd, NULL);

    // generating two distinct prime numbers p and q
    bool isDistinctPrime = false;
    while (!isDistinctPrime) {
        mpz_urandomb(p, state, 512);
        mpz_nextprime(p, p);
        
        mpz_urandomb(q, state, 512);
        mpz_nextprime(q, q);

        isDistinctPrime = mpz_cmp(p, q) != 0;
    }

    // calculating n = p x q
    mpz_mul(n, p, q);

    // calculating phi(n) = (p - 1)(q - 1)
    mpz_sub_ui(temp1, p, 1);
    mpz_sub_ui(temp2, q, 1);
    mpz_mul(phi, temp1, temp2);

    // selecting integer e such that 1 < e < phi(n) and gcd(phi(n), e) = 1
    mpz_sub_ui(range, phi, 2);
    do {
        mpz_urandomm(e, state, range);
        mpz_add_ui(e, e, 2);
        mpz_gcd(gcd, phi, e);
    } while (mpz_cmp_ui(gcd, 1) != 0);

    // calculating d such that d x e (mod phi(n)) = 1 or d = e^(-1) (mod phi(n))
    mpz_invert(d, e, phi);

    // storing public key KU = (e, n)
    std::ofstream publicKeyFile("1302850_Srijan_Publickey");
    char* eStr = mpz_get_str(NULL, 10, e);
    char* nStr = mpz_get_str(NULL, 10, n);
    publicKeyFile << "(" << eStr << ", " << nStr << ")";

    // storing private key KR = (d, n)
    std::ofstream privateKeyFile("1302850_Srijan_Privatekey");
    char* dStr = mpz_get_str(NULL, 10, d);
    privateKeyFile << "(" << dStr << ", " << nStr << ")";

    // outputting keys
    std::cout << "Generated public and private keys and saved to 1302850_Srijan_Publickey and 1302850_Srijan_Privatekey" << "\n\n";

    std::cout << "Public key (e, n):" << "\n";
    std::cout << "(";
    mpz_out_str(stdout, 10, e);
    std::cout << ", ";
    mpz_out_str(stdout, 10, n);
    std::cout << ")";

    std::cout << "\n\n";

    std::cout << "Private key (d, n):" << "\n";
    std::cout << "(";
    mpz_out_str(stdout, 10, d);
    std::cout << ", ";
    mpz_out_str(stdout, 10, n);
    std::cout << ")";

    std::cout << "\n\n";
}

void encrypt(mpz_t C, mpz_t M, mpz_t e, mpz_t n) {
    // calculates ciphertext C such that C = M^e (mod n)
    mpz_powm(C, M, e, n);

    // outputting ciphertext after encryption
    std::cout << "Ciphertext after encryption: " << "\n";
    mpz_out_str(stdout, 10, C);
    std::cout << "\n\n";
}

void decrypt(mpz_t M, mpz_t C, mpz_t d, mpz_t n) {
    // calculates plaintext M such that M = C^e (mod n)
    mpz_powm(M, C, d, n);

    // converting mpz to plaintext
    size_t count;
    size_t size = mpz_sizeinbase(M, 2) / 8 + 1;
    char* buffer = new char[size];
    mpz_export(buffer, &count, 1, 1, 0, 0, M);
    std::string result(buffer, count);

    // outputting plaintext after decryption
    std::cout << "Plaintext after decryption: " << "\n";
    std::cout << result;
    std::cout << "\n\n";
}

int main() {
    // initializing required variables
    mpz_t e, d, n, C, M;
    mpz_inits(e, d, n, C, M, NULL);

    // generating keys
    generateKeys(e, d, n);

    // getting plaintext from the user
    std::string input;
    std::cout << "Enter the plaintext (without spaces): ";
    std::cin >> input;
    std::cout << "\n\n";

    // converting plaintext to mpz
    mpz_import(M, input.length(), 1, 1, 0, 0, input.c_str());

    // encrypting plaintext
    encrypt(C, M, e, n);

    // decrypting ciphertext
    decrypt(M, C, d, n);
    
    return 0;
}