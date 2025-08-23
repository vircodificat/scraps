#include <unistd.h>

int main(void) {
	for (;;) {
		write(1, "Hello, world!\n", 15);
	}
}
