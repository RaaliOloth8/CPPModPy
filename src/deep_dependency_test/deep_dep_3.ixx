export module deep_dep_3;

import deep_dep_5;
import deep_dep_4;
import types;

export u16 deepDep3()
{
	return deepDep4() + deepDep5();
}