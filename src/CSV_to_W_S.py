import pandas as pd
import time
import glob
import os

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4',
        's':'5'
        }
    return categorias[c]

def decodificacionCategoria(c):
    c = str(c)
    categorias = {
        '1':'n',
        '2':'v',
        '3':'a',
        '4':'r',
        '5':'s'
        }
    return categorias[c[0]]

def reemplazarComillas(palabra):
    if type(palabra) == str:
        return palabra.replace('\'', '\'\'')

def crearSynsetID(synset):
    synset = codificacionCategoria(synset[-1]) + synset[:8]
    return int(synset)

def contarSynsets(lista, e):
   contador = 0
   for i in lista:
      if i == e:
         contador += 1
   return str(contador)

def ponerEspacios(palabra):
    if type(palabra) == str:
        return "\'" + palabra[1:-1].replace('\'','\'\'').replace('_',' ') + "\'"

list_of_csv = glob.glob('wnsDF\\**\\*.csv', recursive=True)

for csv in list_of_csv[-4:]:
    inicio = time.time()
    print(csv)
    df = pd.read_csv(csv, index_col=[0])
    df['Synset'] = df['Synset'].apply(crearSynsetID)

    df = df.drop(df[df['Tipo'].str.contains('def')].index)
    df = df.drop(df[df['Tipo'].str.contains('exe')].index)
    df = df.drop(columns=['Tipo'])
    df = df.rename(columns={'Info':'Word'})
    W_Nums = []
    Synsets_list = df.Synset.value_counts()

    for index in reversed(df.index):
        fila = df.loc[index]
        W_Nums.insert(0, Synsets_list[fila['Synset']])
        Synsets_list[fila['Synset']] = Synsets_list[fila['Synset']] - 1

    df['W Num'] = W_Nums
    df["Type"] = df['Synset'].apply(decodificacionCategoria)
    df['Tag Count'] = [0] * len(df['Word'])
    df['Sense'] = [0] * len(df['Word'])
    df['Word'] = df['Word'].apply(reemplazarComillas)

    new_path = csv.replace('wnsDF','wnsProlog').replace('.csv','\\wn_s.pl')
    if not os.path.exists(os.path.dirname(new_path)):
        os.makedirs(os.path.dirname(new_path))

    fichero_escritura = open(new_path, encoding='utf-8',mode='w')
    for i in df.index:
       fichero_escritura.write("s(" + str(df["Synset"][i]) + "," + str(df["W Num"][i]) + ",\'" + str(df["Word"][i]) + "\'," + df["Type"][i] + "," + str(df["Sense"][i]) + "," + str(df["Tag Count"][i]) + ").\n")
    fichero_escritura.close()
    final = time.time()
    print('Proceso en ruta: ' + csv + ' finalizado. Ha tardado ' + str(final-inicio) + '.\n')
    print("----------------------------------------------------")