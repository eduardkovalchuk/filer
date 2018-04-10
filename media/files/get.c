#include <stdio.h>
#include <requests.h>

int main(int argc, const char **argv)
{
    req_t req;                        /* declare struct used to store data */
    CURL *curl = requests_init(&req); /* setup */

    requests_get(curl, &req, "http://example.com"); /* submit GET request */
    printf("Request URL: %s\n", req.url);
    printf("Response Code: %lu\n", req.code);

    requests_close(&req); /* clean up */
    return 0;
}
