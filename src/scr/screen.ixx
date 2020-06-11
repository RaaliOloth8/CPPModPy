export module screen;

import types;

export class Screen
{
protected:
	i32 test = 10;
	
public:
    virtual void say() = 0;
};