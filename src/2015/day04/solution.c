// Day 4 solution, this time in C!

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include <openssl/evp.h>

/**
* Calculates the MD5 hash of the given string
*
* @param str_in The input string to be hashed. Not modified.
* @parm digest The output hash, in raw unprocessed binary. Will be modified.
* @parm digest_len Length of the output hash. Will be set to the length of the digest.
**/
void get_md5(char* str_in, unsigned char* digest, unsigned int* digest_len){
    // Set up for the hash calculation
    EVP_MD_CTX* md5_context = EVP_MD_CTX_new();

    // OpenSSL Magic to get the MD5
    EVP_DigestInit_ex(md5_context, EVP_md5(), NULL);
    EVP_DigestUpdate(md5_context, str_in, strlen(str_in));
    EVP_DigestFinal_ex(md5_context, digest, digest_len);
}

/**
* Checks whether the hash starts with a certain number of zeros
* @param digest Binary hash to check. Not modified.
* @param num_zeros How many zeros we care about here.
* @return True if the hash starts with at least num_zeros 0's, otherwise it's false.
**/
bool check_hash(unsigned char* digest, int num_zeros) {
    char hex[10];
    /** Convert the first part to hex (we only care about the first num_zeros digits anyway)
    And, we know that the problem at most cares about 6 zeros, so we don't have to
    over-complicate stuff here. **/
    for (int i=0; i<4; i++) {
        sprintf(&hex[i*2], "%02x", digest[i]);
    }
    // Check that the hash is good
    for (int i=0; i<num_zeros; i++) {
        if (hex[i] != '0') {
            return false;
        }
    }

    return true;
}

/**
* Tries a bunch of hashes until we get one satisfying the problem constraint of # zeros
*
* @param num_zeros The minimum number of zeros to accept a solution
* @param suffix The suffix that will be appended to the input string (a number). Modified in place.
* @param str_out The output hash in hex, modified in place.
**/
void find_hash(int num_zeros, int* suffix, char* str_out) {
    unsigned char digest[EVP_MAX_MD_SIZE];
    unsigned int digest_len;
    *suffix = 0;
    char str_in[64];

    // Try hashes until we get a good one
    do {
        (*suffix)++;
        sprintf(str_in, "iwrupvqb%d", *suffix);
        get_md5(str_in, digest, &digest_len);
    } while (!check_hash(digest, num_zeros));

    // Then convert the hash to hex
    for (int i=0; i<digest_len; i++) {
        sprintf(&str_out[i*2], "%02x", digest[i]);
    }
}

int main() {
    int suffix;
    char str_out[64];

    // Part 1
    find_hash(5, &suffix, str_out);
    printf("Part 1: %i --> %s\n", suffix, str_out);

    //Part 2
    find_hash(6, &suffix, str_out);
    printf("Part 2: %i --> %s\n", suffix, str_out);


    return 0;
}

