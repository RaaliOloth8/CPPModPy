export module log;

import std.core;

export namespace Log
{
    void msg(std::string_view message)
    {
        std::cout << message << "\n";
    }
}