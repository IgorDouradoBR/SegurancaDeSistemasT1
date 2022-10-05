import collections
import math
import os
import string

LETRASP = {'a':0.1463,'b':0.0104,'c':0.0388,'d':0.0499,'e':0.1257,'f':0.0102,'g':0.013,'h':0.0078,'i':0.0618,'j':0.0039,'k':0.0001,'l':0.0277,'m':0.0473,'n':0.0444,'o':0.0973,'p':0.0252,'q':0.012,'r':0.0653,'s':0.068,'t':0.0433,'u':0.0363,'v':0.0157,'w':0.0003,'x':0.0025,'y':0.00006,'z':0.0047}
LETRASI = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253, 'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094, 'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025, 'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056, 'u':0.02758, 'v':0.0978, 'w':0.2360,'x':0.00150, 'y':0.01974, 'z':0.0074}

class __decifra__:

  def __init__(self, tudocifrado, letras, comum):
      self.tudocifrado = tudocifrado
      self.letras = letras
      self.tamanhol = len(letras)
      self.comum = comum
      self.dicioalfabeto = {}
      self.construtor()

  def construtor(self):  
      for tamanhoC in range(0, self.tamanhol):
          for k in range(0, tamanhoC): 
              _cifrado_ = str(self.tudocifrado[k::tamanhoC])
              if len(_cifrado_) >= 2:
                  indices = self.tabelaI(_cifrado_)
                  if indices > 0.0:
                      if tamanhoC in self.dicioalfabeto:
                          self.dicioalfabeto[tamanhoC].append(indices)
                      else:
                          self.dicioalfabeto[tamanhoC] = [indices]
          if tamanhoC in self.dicioalfabeto:
              self.dicioalfabeto[tamanhoC] = float(sum(self.dicioalfabeto[tamanhoC]) / len(self.dicioalfabeto[tamanhoC]))

  def distribui(ctxt):
    used_lang_ioc = LETRASI if ctxt == 'en' else LETRASP  
    keylen = 0  
    closest = 0  
    avg_ioc = [] 

    for i in range(5):
        avg_ioc.append(((ctxt, i)))
    for i in range(5):
        if sum(avg_ioc[i], closest, used_lang_ioc)>= 11:
            closest = avg_ioc[i]
            keylen = i + 1
    return keylen
  
  def tabelaI(self, _cifrado_):
      repeticao_acumulo = 0.0
      for char_repeticao in collections.Counter(_cifrado_).values():
          repeticao_acumulo = repeticao_acumulo + char_repeticao * (char_repeticao - 1)
      totalCarac = len(_cifrado_)
      return repeticao_acumulo / (totalCarac * (totalCarac - 1))

  

  def getRepeticaoAcumulo(self, frequencies, total_length):
      acumulo = 0.0
      for f in frequencies:
          frequencies[f] *= (1.0 / total_length)
          acumulo += ((frequencies[f] - math.pow(self.letras[f], 2)) / self.letras[f])
      return acumulo

  def indiceFs(self, _cifrado_, position):
      fluctuations = []
      for letter in _cifrado_:
          fluc = chr(ord(self.comum) + ((ord(letter) - ord(self.comum) - position) % self.tamanhol))
          fluctuations.append(fluc)
      return fluctuations

  def chance(self, _cifrado_):
      indicessoma = {}
      self.comum = 'a'
      for i in range(self.tamanhol):
          fluctuations = self.indiceFs(_cifrado_, i)
          frequencies = collections.Counter(fluctuations)
          indicessoma[i] = self.getRepeticaoAcumulo(frequencies, len(_cifrado_))          
      return chr(min(indicessoma, key = indicessoma.get) + ord(self.comum))
  
  def getdicionario(self):
      return self.dicioalfabeto

  def captura(self):
      return self.tudocifrado



class __pegachave__:
    def __init__(self, repeticao, letras, alfab):
        self.repeticao = repeticao
        self.tamanhol = len(letras)
        self.alfab = alfab
        self.dicioalfabeto = repeticao.getdicionario()

    def testeR(text): 
        freq_each_char = sum(text)  
        ioc = 0
        for index in list(LETRASP):  
            ioc += (freq_each_char[index] * (freq_each_char[index] - 1))
        return ioc / (len(text) * (len(text) - 1)) 

    def tamanhoChave(self):
        coincide = lambda k : abs(float('%.3f' % k[1]) - self.alfab)
        chave,_ = min(self.dicioalfabeto.items(), key = coincide)
        return chave


    def getChave(self):
        tamanhoC = self.tamanhoChave()
        cifrado = self.repeticao.captura()
        return ''.join(self.repeticao.chance(cifrado[k::tamanhoC]) for k in range(tamanhoC))

    def textoClaro(self):
        chave = self.getChave()
        cifrado = self.repeticao.captura()
        return ''.join(string.ascii_lowercase[(ord(char) - ord(chave[pos % len(chave)])) % self.tamanhol] for pos, char in enumerate(cifrado))



def leTexto():  
  with open(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + nome, 'r') as file:
    return file.read()


nome = input("Digite o nome do arquivo e sua extensão (exemplo: plaintext.txt): ")

if __name__ == "__main__":
  linguagem = int(input("Digite 1 para texto em português e 2 para texto em inglês: "))
  if (linguagem == 1):
    print(f'\n==========================================\n')
    tudocifrado = leTexto()
    print('Cifra achada!')

    tabelafqc = __decifra__(tudocifrado, LETRASP, 'a')
    print('Frequências encontrada!')

    chaveLocalizada = __pegachave__(tabelafqc, LETRASP, 0.07461).getChave()
    print('Chave localizada!')
    
    with open(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + 'saida.txt', "w+") as file:
      file.write(__pegachave__(tabelafqc, LETRASP, 0.07461).textoClaro())

    print(f'\nArquivo já sobrescrito... Chave da cifra: {chaveLocalizada}')
    print(f'\n==========================================\n')

  elif (linguagem == 2):
    print(f'\n==========================================\n')

    print('Found cipher!')
    tudocifrado = leTexto()
    print('Found frequency!')
    tabelafqc = __decifra__(tudocifrado, LETRASI, 'e')
    chaveLocalizada = __pegachave__(tabelafqc, LETRASI, 0.06551).getChave()
    print('Found key!')
    with open(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + 'saida.txt', "w+") as file:
      file.write(__pegachave__(tabelafqc, LETRASI, 0.06551).textoClaro())

    print(f'\nFile already overwritten... Your key is: {chaveLocalizada}')
    print(f'\n==========================================\n')
  
