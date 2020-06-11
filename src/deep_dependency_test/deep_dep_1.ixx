#include <cassert>

export module deep_dep_1;

import deep_dep_2;
import deep_dep_3;

import types;
import log;

export void deepDep1()
{
	u16 test = 0;
	test += deepDep2();
	test += deepDep3();
	// should be 20
	assert(test == 20);
	Log::msg("it's 20");
}