"""
	Prime number calculation script.
	Copyright Jannik Schmied, 2021

	This script uses the "Sieve of Eratothenes" technique to 
	calculate prime numbers up to a certain range.
	Additionally, there is the possibility to save the output
	to a file instead of printing it to the screen.

	Examples:
	# Calculate all primes smaller then 1000000 and save them to file
	python3 prime.py 1000000 True
	python3 prime.py 1000000 true
	python3 prime.py 1000000 1

	# Calculate all primes smaller then 5000 but don't save them to file
	python3 prime.py 5000 False
	python3 prime.py 5000 false
	python3 prime.py 5000 0
	python3 prime.py 5000
"""


import sys
from time import time
from math import floor


# Define Sieve of Eratosthenes function
def eratothenes(n):
	# Comprehension list defining sieve
	print("[*] Preparing sieve...")
	sieve = [True for i in range(n + 1)]
	output = []
	
	# start point
	p = 2

	while p * p <= n:
		if sieve[p]:
			for i in range(p * 2, n+1, p):
				sieve[i] = False
		p += 1

	# statically set 0 and 1 to false
	sieve[0] = False
	sieve[1] = False
	print("[+] Done.\n")

	print("[*] Starting prime number calculation...")
	for p in range(n + 1):
		if sieve[p]:
			output.append(p)
			print(f"[*] Latest prime found: {p}", end='\r')

	print(f"\n[+] Done.")

	return output


# Start execution

# Check command line arguments
if len(sys.argv) not in range(2,4):
	print("[i] Usage: python3 prime.py <range:int> [<save_to_file:bool>]")
	sys.exit()

if len(sys.argv) == 3:
	# Check command line argument and handle wrong input
	save_to_file = sys.argv[2] in ["True", "False", "true", "false", "0", "1"] if (sys.argv[2] in ["True", "true", "1"] if True else False) else False

	# Dedicated output
	if save_to_file:
		print("[i] Output will be saved to a file.")
	else:
		print("[i] Output will not be saved to a file.")
else:
	save_to_file = False
	print("[i] Output will not be saved to a file.")


try:
	prime_range = int(sys.argv[1])
except:
	print("[!] Invalid Arguments.")
	print("[i] Usage: python3 prime.py <range:int> [<save_to_file:bool>]")
	sys.exit()


start = floor(time() * 1000.0)

primes = eratothenes(prime_range)

if save_to_file:
	print("[*] Saving Output to file...")
	try:
		file = open(f"primes-{prime_range}.txt", "w")
		file.write(str(primes))
		print(f"[+] Done.\n[i] Output saved to file: 'primes-{prime_range}.txt'!")
	except Exception as e:
		print(f"[!] Whoops. An error occured: {e}")

end = floor(time() * 1000.0)

delta_time = end - start

if not save_to_file:
	print(f"\n[i] Output: \n{primes}")
print(f"\n[i] Count: {len(primes)}")
print(f"[i] Execution time: {delta_time} ms ({delta_time / 1000} s / {delta_time / 60000} min)")
sys.exit()
