export module screen_hello;

import screen;
import log;

export class ScreenHello : public Screen
{
public:

    void say() override
	{
		if(test == 10)
			Log::msg("Hello from ScreenHello");
	}
};