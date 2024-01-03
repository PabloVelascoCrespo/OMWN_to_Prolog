import glob
import pandas as pd

list_of_tab = glob.glob('omw-data-main\\wns\\**\\*.tab', recursive=True)

for tab in list_of_tab:
    print(tab)
    fichero = open(tab,encoding="utf-8")
    fichero_lineas = fichero.readlines()
    Synset = []
    Tipo = []
    Info = []
    for linea in fichero_lineas:
        linea_dividida = linea.split('\t')
        
        cadena= ""
        if len(linea_dividida)  == 3:
            Synset.append(linea_dividida[0])
            Tipo.append(linea_dividida[1])
            Info.append(linea_dividida[2][:-1])
        elif len(linea_dividida)  > 3:
            Synset.append(linea_dividida[0])
            Tipo.append(linea_dividida[1])
            for info in linea_dividida[1:]:
                cadena+=info[:-1]
            Info.append(cadena)
        else:
            print(linea)

    csv = pd.DataFrame({'Synset': Synset, 'Tipo': Tipo, 'Info':Info})
    csv = csv.drop(0)
    csv = csv.reset_index(drop=True)
    new_path = tab[14:].replace('wns','wnsDF').replace('tab','csv')
    csv.to_csv(new_path)
    fichero.close()
    print('----------------------------------------------------------------------')