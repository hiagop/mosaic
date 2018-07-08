from PIL import Image
import numpy as np
import copy

class mosaic:
	def __init__(self,file):
		im = Image.open(file) # Lê a imagem de entrada
		self.width, self.height = im.size
		self.image = np.array(im, dtype="uint8") #  Converte a imagem como array numpy 

		print("Pré-processamento...")
		# Tratamento para RGB-GRAYSCALE e/ou JPEG-PNG
		output_np = np.array(np.zeros(shape=(self.height,self.width)), dtype="uint8") # Array numpy de saida
		for i in range(self.height):
			for j in range(self.width):
				aux = round(np.median(self.image[i][j])) # Tira a média dos 3 canais e arredonda o valor 
				output_np[i][j] = aux		
		self.image = output_np
		self.original = copy.deepcopy(self.image) # Backup da foto original

	def filtro_uniforme(self,L):
		window = 2*L+1
		center = L
		filtro = np.zeros((window, window))
		for i in range(window):
			for j in range(window):
				filtro[i][j] = 1/pow(window, 2)

	    # Criando a saída e o shadow
		output = np.zeros((self.height+2*center, self.width+2*center))
		output[center:self.height+center,center:self.width+center] = self.image
		altered_input = copy.deepcopy(output)

		for i in range(self.height):
			for j in range(self.width):	
				output[i+center][j+center] = np.sum(altered_input[i:i+window,j:j+window]*filtro)

		self.image = output[center:self.height+center,center:self.width+center] # Descartando o shadow e finalizando a imagem
		

	def interpolation(self, K):
		output = np.zeros((int(self.height*K), int(self.width*K)), "uint8")
		for i in range(0,K*(self.height-1),K):
			for j in range(0,K*(self.width-1),K):
				for i_add in range(K):
					for j_add in range(K):
						output[i+i_add][j+j_add] = self.image[int(i/K)][int(j/K)]
		self.image = output
		self.out = Image.fromarray(self.image, 'L') # Converte o array pra imagem, declarando que a imagem deve estar em tons de cinza
		self.width, self.height = self.out.size

	def downsampling(self, K): 
		output = np.zeros((int(self.height/K), int(self.width/K)), "uint8")
		for i in range(0,self.height, K):
			for j in range(0, self.width, K):
				output[int(i/K)][int(j/K)] = self.image[i][j]
		self.image = output
		self.out = Image.fromarray(self.image, 'L') # Converte o array pra imagem, declarando que a imagem deve estar em tons de cinza
		self.width, self.height = self.out.size

	def granulate(self, K): # Granulamento por média
		# Caso o valor de granulamento não seja multiplo do tamanho da imagem, temos esse tratamento de borda
		shadow_x = shadow_y = 0
		if(self.height % K != 0):
			shadow_x = K
		if(self.width % K != 0):
			shadow_y = K

		output = np.zeros((self.height, self.width), "uint8")
		for i in range(0,self.height-shadow_x,K):
			for j in range(0,self.width-shadow_y,K):
				aux = round(np.median(self.image[i:i+K, j:j+K]))
				for i_add in range(K):
					for j_add in range(K):
						output[i+i_add][j+j_add] = aux

		self.image = output
		self.out = Image.fromarray(self.image, 'L') # Converte o array pra imagem, declarando que a imagem deve estar em tons de cinza
		self.width, self.height = self.out.size

print("Carregando a imagem...")
obj = mosaic("gato.jpg")  
print("Aplicando filtro...")
obj.filtro_uniforme(3)
print("Aplicando granulamento...")
obj.granulate(16)
#obj.interpolation(2)
obj.out.show()		