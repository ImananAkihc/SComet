#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <emmintrin.h>

#define SIZE 1024 * 1024 * 10

char array[SIZE];
int loop = 1;

void nontemporal_sse_write_loop(void *array, size_t size, size_t interval)
{
  for (int l = 0; l < loop; l++)
  {
    __m128i *varray = (__m128i *)array;

    __m128i vals = _mm_set1_epi32(1);

    size_t i;
    for (i = 0; i < size / sizeof(__m128i); i++)
    {
      _mm_stream_si128(&varray[i], vals);
      vals = _mm_add_epi16(vals, vals);
      for (size_t j = 0; j < interval; j++)
        asm("nop");
    }
  }
}

int main(int argc, char **argv)
{
  int interval = 0;
  if (argc >= 2)
  {
    sscanf(argv[1], "%d", &interval);
  }
  if (argc >= 3)
  {
    sscanf(argv[2], "%d", &loop);
  }
  memset(array, 0xFF, SIZE);
  *((uint64_t *)&array[SIZE]) = 0;

  nontemporal_sse_write_loop(array, SIZE, interval);

  return 0;
}
