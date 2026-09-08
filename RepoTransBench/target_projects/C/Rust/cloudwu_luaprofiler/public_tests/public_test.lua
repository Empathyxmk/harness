local p = require "profiler"

-- Use different recursive function and different data for public test.

-- Fibonacci function instead of factorial
local function fib(n)
	if n <= 2 then
		return 1
	else
		return fib(n-1) + fib(n-2)
	end
end

local function bar(n)
	local s = 0
	for i=1,n do
		s = s + fib(i)
	end
	return s
end

-- Change arguments to profiler.start to different numbers
p.start(500, 5)

-- Use a different traversal value for bar
bar(12)

local info, n = p.info()

p.stop()

for filename, line_t in pairs(info) do
	for line, count in pairs(line_t) do
		print(filename, line, count)
	end
end

print("total=", n)