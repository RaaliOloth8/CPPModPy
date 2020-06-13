import screen;
import screen_hello;

import log;
import another_name;
import deep_dep;
import export_import;

int main()
{
	Log::msg("Hello from cpp");
	
	Screen* scr = new ScreenHello();
	scr->say();
	delete scr;
	
	testAnotherName();
	testDeepDep();
	exportImportTest();
	return 0;
}