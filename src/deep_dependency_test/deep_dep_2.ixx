export module deep_dep_2;

import deep_dep_4;
import deep_dep_5;
import types;

export u16 deepDep2()
{
	return deepDep4() + deepDep5();
}