// Rhea runtime library, if you can call it that.
// Note about mangling:
//  Special or backend function = name
// 	Rhea function in C = '$' + name
//  If we end up using C instead of C++ (Which at this point is likely), method = '__' + class_name + '_' + method_name

#include <stdio.h>
#include <stdint.h>

// Types
typedef double 		Float;
typedef int64_t 	Int;

void Int$_System$xprint(Int i){
	printf("%ld\n", i);
}

void Float$_System$xprint(Float i){
	printf("%g\n", i);
}

Float Float$_Float$i$d(Float joe, Float other){
	return joe / other;
}

Float Float$_Float$i$m(Float joe, Float other){
	return joe * other;
}

Float Float$_Float$i$a(Float joe, Float other){
	return joe + other;
}

Float Float$_Float$i$s(Float joe, Float other){
	return joe - other;
}

Float Int$_Float$i$d(Float joe, Int other){
	return joe / other;
}

Float Int$_Float$i$m(Float joe, Int other){
	return joe * other;
}

Float Int$_Float$i$a(Float joe, Int other){
	return joe + other;
}

Float Int$_Float$i$s(Float joe, Int other){
	return joe - other;
}

Int Int$_Int$i$d(Int self, Int other){
	return self / other;
}

Int Int$_Int$i$m(Int self, Int other){
	return self * other;
}

Int Int$_Int$i$a(Int self, Int other){
	return self + other;
}

Int Int$_Int$i$s(Int self, Int other){
	return self - other;
}

Int Float$_Int$i$d(Int self, Float other){
	return self / other;
}

Int Float$_Int$i$m(Int self, Float other){
	return self * other;
}

Int Float$_Int$i$a(Int self, Float other){
	return self + other;
}

Int Float$_Int$i$s(Int self, Float other){
	return self - other;
}
