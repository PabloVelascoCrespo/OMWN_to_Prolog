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

def eliminarFuente(cadena):
    try:
        return cadena[4:]
    except:
        return "NO TIENE NI GLOSA NI EJEMPLOS"
def fusionarGlosaExe(df):
    grouped = df.groupby(df.iloc[:, 0])
    result_df = pd.DataFrame(columns=df.columns)

    for group_name, group_data in grouped:
        concatenated_values = '; '.join(map(str, group_data.iloc[:, 2]))
        result_df = pd.concat([result_df, pd.DataFrame({df.columns[0]: [group_name], df.columns[2]: [concatenated_values]})], ignore_index=True)
    result_df = result_df.drop(columns=['Tipo'])
    return result_df

for csv in list_of_csv[18:]:
    inicio = time.time()
    print(csv)
    df = pd.read_csv(csv, index_col=[0])
    df['Synset'] = df['Synset'].apply(crearSynsetID)
    df['Info'] = df['Info'].apply(eliminarFuente)
    Synset_list = df['Synset'].to_list()
    Glosa_list =  []

    df = df.drop(df[df['Tipo'].str.contains('NO TIENE NI GLOSA NI EJEMPLOS')].index)
    df = df.drop(df[df['Tipo'].str.contains('lemma')].index)
    df = fusionarGlosaExe(df)

    df['Info'] = df['Info'].apply(reemplazarComillas)
    if not df.empty:
        print(df)
    new_path = csv.replace('wnsDF','wnsProlog').replace('.csv','\\wn_g.pl')
    if not os.path.exists(os.path.dirname(new_path)):
        os.makedirs(os.path.dirname(new_path))

    fichero_escritura = open(new_path, encoding='utf-8',mode='w')
    for i in df.index:
       fichero_escritura.write("g(" + str(df["Synset"][i]) + ",\'" + str(df["Info"][i]) + "\').\n")
       
    fichero_escritura.close()
    final = time.time()
    print('Proceso en ruta: ' + csv + ' finalizado. Ha tardado ' + str(final-inicio) + '.\n')
    print("----------------------------------------------------")