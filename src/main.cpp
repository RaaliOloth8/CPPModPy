import screen_hello;

import log;
import another_name;
import deep_dep;

int main()
{
	Log::msg("Hello from cpp");
	ScreenHello scr;
	scr.say();
	testAnotherName();
	testDeepDep();
	return 0;
}