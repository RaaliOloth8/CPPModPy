export module deep_dep_4;

import deep_dep_5;
import types;

export u16 deepDep4()
{
	return deepDep5();
}