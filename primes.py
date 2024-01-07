import os, subprocess, sys, re

# Args checking

if len(sys.argv) < 2 :
	print("Nombre d'arguments invalide. Veuillez spécifier la taille des clés générées.")

# Consts

keySize = sys.argv[1]

root = f"./keys-{keySize}"
primesFnp = "./primes.txt"
finalPrimesFnd = f"./final-primes-{keySize}-2.txt"

primesList = []

# KEY_LIMIT = 1000

# Detect

def getPrimes (entry) :
	prime1 = re.compile(r'prime1:\s\d+')
	prime2 = re.compile(r'prime2:\s\d+')

	m1 = prime1.search(entry)
	m2 = prime2.search(entry)

	pr1 = ""
	pr2 = ""

	if m1:
		p1Value = m1.group()
		p1 = p1Value[8:]
		pr1 = p1

	if m2:
		p2Value = m2.group()
		p2 = p2Value[8:]
		pr2 = p2

	return (pr1, pr2)

# List

def list_files_in_folder(fp):	
	files = os.listdir(fp)

	nCommonPDup = 0
	nCommonQDup = 0
	nCommonPQDup = 0

	ordered_files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(fp, f)))
	# ordered_files = ordered_files[0 : KEY_LIMIT]

	with open(primesFnp, 'w') as fprimes :		
		for fn in ordered_files:
			print(f"Clé {fn} ...")

			fnp = os.path.join(fp, fn)
			with open(fnp) as f:
				content = f.read()
				mapedP = list(map(lambda x : x['p'], primesList))
				mapedQ = list(map(lambda x : x['q'], primesList))

				# Executing BASH command

				cmd = f"openssl rsa -noout -text -in {fnp}"

				retCmd = subprocess.check_output(cmd, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

				# Getting command result

				chunks = [line.decode() for line in retCmd.splitlines()]
				ret = '\n'.join(chunks)

				prime1, prime2 = getPrimes(ret) # Getting primes from extraction using regexp

				fndP = False
				fndQ = False
				fndPQ = False

				# Checking if this prime numbers have already been found

				try :
					# P
					idxP = mapedP.index(prime1)
					primeKey = primesList[idxP]
					# fprimes.write(f"Doublon de nombre premier détecté (P : {primeKey['p']}), clé de base : {primeKey['originalKey']}, clé contenant le doublon : {primeKey['copiesP']}\n")
				
					# Q
					idxQ = mapedQ.index(prime2)
					primeKey = primesList[idxQ]

					if idxP != idxQ :
						raise ValueError("Different primes.")

					# fprimes.write(f"Doublon de nombre premier détecté (Q : {primeKey['q']}), clé de base : {primeKey['originalKey']}, clé contenant le doublon : {primeKey['copiesQ']}\n")
					
					print(f"Doublons détectés pour les deux nombres (clé : {primeKey['originalKey']}) !")
					primesList[idxQ]['copiesPQ'].append(fn) # Adding current key filename to copies found on Q prime
					fndPQ = True # Setting to true if both numbers have been found in previous keys
				except ValueError :
					pass

				try :
					idxP = mapedP.index(prime1)
					fndP = True
					primeKey = primesList[idxP]
					primesList[idxP]['copiesP'].append(fn) # Adding current key filename to copies found on P prime
					print(f"Doublon détecté pour une clé, nombre P (clé : {primeKey['originalKey']}) !")
				except ValueError :
					pass

				try :
					idxQ = mapedQ.index(prime2)
					fndQ = True
					primeKey = primesList[idxQ]
					primesList[idxQ]['copiesQ'].append(fn) # Adding current key filename to copies found on Q prime
					print(f"Doublon détecté pour une clé, nombre Q (clé : {primeKey['originalKey']}) !")
				except ValueError :
					pass

				# Saving new key to be compared later, if no same prime has been found for the current one

				if fndPQ :
					nCommonPQDup += 1
				elif fndP :
					nCommonPDup += 1
				elif fndQ :
					nCommonQDup += 1
				else :
					primesList.append({
						'copiesP' : [],
						'copiesQ' : [],
						'copiesPQ' : [],
						'originalKey' : fn,
						'p' : prime1,
						'q' : prime2
					})

		fprimes.close()

		# Log

		print("Detection réussie ! Sauvegarde ...")

		with open(finalPrimesFnd, "w") as f :
			for prime in primesList :
				pqCopies = prime['copiesPQ']
				pCopies = prime['copiesP']
				qCopies = prime['copiesQ']

				if len(pqCopies) > 0 :
					f.write(f"Doublons de nombres premiers détectés pour P et Q (clé de base : {prime['originalKey']}, clés : {pqCopies})\n")
				elif len(pCopies) > 0 :
					f.write(f"Doublons de nombre premier détecté (clé de base : {prime['originalKey']}, clés contenant le même nombre premier P : {pCopies})\n")
				elif len(qCopies) > 0 :
					f.write(f"Doublons de nombre premier détecté (clé de base : {prime['originalKey']}, clés contenant le même nombre premier Q : {qCopies})\n")
			f.write(f"\n\nDoublons de nombres premier :\n - P : {nCommonPDup}\n - Q : {nCommonQDup}\n - P et Q : {nCommonPQDup}")
			f.close()


list_files_in_folder(root) # List




