import screen_hello;

import log;
import another_name;
import deep_dep;
import export_import;

int main()
{
	Log::msg("Hello from cpp");
	ScreenHello scr;
	scr.say();
	testAnotherName();
	testDeepDep();
	exportImportTest();
	return 0;
}