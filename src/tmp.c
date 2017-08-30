#include "runtime.h"
int main () 
{
	Int foo = 2;
	Int$_System$xprint (foo);
	Float bar = 2.4;
	Float$_System$xprint (bar);
	Float q = Float$_Float$i$s (2.2, 1.3);
	Float$_System$xprint (q);
	Float$_System$xprint (bar);
	Float$_System$xprint (Float$_Float$i$s (3.1, 3.2));
	Float$_System$xprint (Int$_Float$i$s (2.1, 2));
	Int$_System$xprint (Float$_Int$i$m (3, 1.1));
	Int$_System$xprint (Int$_Int$i$a (4, 34));
	Float x = Float$_Float$i$m (Float$_Float$i$s (2.2, 1.3), bar);
	Float$_System$xprint (x);
}
