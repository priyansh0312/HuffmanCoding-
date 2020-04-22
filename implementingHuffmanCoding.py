# compresses a file from text to binary and reduces file size.
# decompresses a file from binary to text 
import heapq
import os


class TreeNode:
	def __init__(self,value,frequency):
		self.value = value 
		self.frequency = frequency
		self.left = None 
		self.right = None 
	# for comparing two binary tree nodes (overloaded functions)	
	def __lessthan__(self,other): 
		return self.frequency < other.frequency

	def __equalto__(self,other):
		return self.frequency == other.frequency


class HuffmanCoding:

	def __init__(self,path):
		self.path = path 
		self.__heap=[]
		self.__codes={}
		self.__reverseCodes={}

	
	def __make_frequency_Dict(self,text):
		freq_d = {}
		for i in text:
			if i not in freq_d:
				freq_d[i] = freq_d.get(i,0) + 1
		return freq_d 


	def __createHeap(self,freq_d):		
		# 1. every node of the heap should be a binary tree node : create TreenNode class
		# 2. binary tree node must have a left,right,value,frequency
		for key in freq_d:
			freq = freq_d[key]
			newNode = TreeNode(key,freq)
			heapq.heappush(self.__heap,newNode)
	

	
	def __createBinaryTree(self,heap):
		# 1. find two min freq nodes from the heap
		# 2. create a newnode that has value None and freq = sum of frequencies of two min nodes
		# 3. assign right and left of the newNode created 
		# 4. push newNode into the heap
		# 5. repeat this process for the newNode and the next minimum Node freq for all the elements in the heap
		
		while len(self.__heap)>1:
			min1 = heapq.heappop(self.__heap)
			min2 = heapq.heappop(self.__heap)
			total_freq = min1.frequency + min2.frequency
			newNode = TreeNode(None,total_freq)
			newNode.right = min1
			newNode.left = min2 
			heapq.heappush(self.__heap,newNode)
		return 

	def __buildCodesHelper(self,root,curr_bits):

		if root is None: # we need to return for no left or no right nodes
			return 

		if root.value is not None : # for leafNodes we need to map values with curr bits added so far 
			self.__codes[root.value] = curr_bits
			self.__reverseCodes[curr_bits] = root.value

		self.__buildCodesHelper(root.left,curr_bits + "1") # 1 for left node 
		self.__buildCodesHelper(root.right,curr_bits + "0") # 0 for right node

	def __buildCodes(self):
		root = heapq.heappop(self.__heap)
		self.__buildCodesHelper(root,'')

	def __getEncodedtext(self,text):
		encodedtext = ""
		for char in text:
			encodedtext+=self.__codes[char]
		return encodedtext

	def __getPaddedEncodedtext(self,encodedtext):
		# 1. get number of paddings to be done at end 
		# 2. add 0s corresponding to the number of paddings
		# 3. add the binary of the padding amount infront of the encoded textin 8 bits

		padding_amount = 8 - (len(encodedtext)%8) 

		for i in range(padding_amount):
			encodedtext+="0" 

		padded_info = "{0:08b}".format(padding_amount) # 0:08b converts 0th element in format to 8 bit binary
		padded_encodedtext = padded_info + encodedtext
		return padded_encodedtext

	def __convertToBytes(self,padded_encodedtext):
		li =[] 
		for i in range(0,len(padded_encodedtext),8):
			byte = padded_encodedtext[i:i+8] # one byte is 8 bits in the padded encoded text 
			li.append(int(byte,2)) # converts the text into binary integer 
		return li

	def __removePadding(self,text):
		padded_info = text[:8]
		extra_padding = int(padded_info,2)

		text = text[8:]
		actual_text = text[:-1*extra_padding]
		return actual_text


	def __decodeText(self,text):
		decoded_text = ""
		current_bits = ""

		for bit in text:
			current_bits+=bit
			if current_bits in self.__reverseCodes:
				char = self.__reverseCodes[current_bits]
				decoded_text+=char
				current_bits = ""
		return decoded_text


	def compress(self):
		# get file from the path

		# os library is used with splitext to split path provided on the basis of dot(.) and stores filename as 
		# untitled and file_extension as .txt
		file_name,file_extension = os.path.splitext(self.path) 
		output_path = file_name + '.bin' # saving output file in .bin format by simply adding string to filename

		# opening file 

		# syntax for opening a file in r+ format and opening another output file in wb(write in binary) format 
		with open(self.path,"r+") as file, open(output_path,"wb") as output:
			# read text from file
			text = file.read()
			text = text.rstrip() # removing extra spaces and indentation from the file from the right side
			# make frequency dictionary
			freq_dict = self.__make_frequency_Dict(text)
		
			# construct heap from the frequency dictionary 
			self.__createHeap(freq_dict)

			# construct binary tree from the heap
			self.__createBinaryTree(self.__heap)

			# construct the codes from tree 
			self.__buildCodes()

			# create encoded text using the codes
			encodedtext = self.__getEncodedtext(text)

			# put these encoded texts into the file binary file 
			# padding of the encodeing text for 8 bit system
			padded_encodedtext = self.__getPaddedEncodedtext(encodedtext)

			# converting to bytes 
			bytes_array = self.__convertToBytes(padded_encodedtext)
			final_bytes = bytes(bytes_array) # converts the given integer into bytes
		
			# return the binary file as output
			output.write(final_bytes)

		print("compressed")
		return output_path

	def decompress(self,input_path):
		file_name, file_extension = os.path.splitext(self.path)
		output_path = file_name + "_decompressed" + ".txt"
		with open(input_path,"rb") as file, open(output_path,'w') as output:
			bitString = ""
			byte = file.read(1) # reading each character 
			while byte :
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8,'0')
				bitString+=bits
				byte = file.read(1)
			actual_text = self.__removePadding(bitString)
			decompressed_text = self.__decodeText(actual_text)
			output.write(decompressed_text)
		return 


#Main
path = '/Users/priyanshsoni/Desktop/mycodes/Sample.txt'
h = HuffmanCoding(path) # making an object for the path 
output_path = h.compress() # calling compress function for the file 
h.decompress(output_path)

