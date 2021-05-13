import screen;
import screen_hello;

import log;
import another_name;
import deep_dep;
import export_import;

import part_test;

int main()
{
	Log::msg("Hello from cpp");
	
	Screen* scr = new ScreenHello();
	scr->say();
	delete scr;
	
	testAnotherName();
	testDeepDep();
	exportImportTest();
	
	part_test_part1();
	part_test_part2();
	return 0;
}