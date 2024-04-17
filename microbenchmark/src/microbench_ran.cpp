#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <emmintrin.h>

//#define SIZE (1024*1024*10/16)
#define random(x) (rand() % x)
int SIZE = 1024 * 1024 * 10 / 16;
int m = 37777357;
__m128i array[1024 * 1024 * 10 / 16];
int loop = 1;
size_t i = 714809;
void nontemporal_sse_write_loop(__m128i *array, size_t size, size_t interval)
{
	__m128i vals = _mm_set1_epi32(1);
	for (int l = 0; l < loop; l++)
	{
		for (int n = 0; n < 50000; n++)
		{
			i = (1153 + i * 131111111) % m;

			_mm_stream_si128(&array[(i % SIZE)], vals);
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

	nontemporal_sse_write_loop(array, SIZE, interval);

	return 0;
}
