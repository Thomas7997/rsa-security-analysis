import os, sys

# Args checking

if len(sys.argv) < 2 :
	print("Nombre d'arguments invalide. Veuillez spécifier la taille des clés générées.")

# Consts

root = f"./keys-{sys.argv[1]}"
copiesPath = f"./copies-{sys.argv[1]}.txt"

keysList = []
copiesList = []

nDuplicates = 0

def list_files_in_folder(fp):
	try:
		fcopies = open(copiesPath, 'w')
		files = os.listdir(fp)
		for fn in files:
			fnp = os.path.join(fp, fn)
			with open(fnp) as f:
				content = f.read()
				mapedKeysList = list(map(lambda x : x['content'], keysList))

				try :
					idx = mapedKeysList.index(content)
					originalFilename = keysList[idx]['filename']

					print(f"Doublon {fn} detecté !")
					copiesList.append({
						'originalFilename' : originalFilename,
						'copyFilename' : fn
					})
					fcopies.write(f"Clé d'origine : {originalFilename} Copie : {fn}\n")

					nDuplicates += 1

				except Exception as e :
					pass

				keysList.append({
					'filename' : fn,
					'content' : content
				})
		fcopies.close()
	except Exception as e:
		print(f"Error: {e}")

list_files_in_folder(root)

print(f"{nDuplicates} doublons détectés !")