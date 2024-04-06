import cv2
import string
import math

OnionFolderPath = "OnionText/"
NormalFolderPath = "NormalText/"
InputTextFilePath = "input.txt"
OnionOutputFilePath = "Onion_output.png"
NormalOutputFilePath = "Normal_output.png"




# reads letter files into cv2 images list
def FontSetUp(path):
	fontFileNames = list(string.ascii_lowercase) # get list of lowercase alphabet
	fontFileNames.append("space") # add the space letter
	
	images = [] # empty list to hold images

	for name in fontFileNames:
		# add exact path to current letter image e.g. "a.png"
		letterImageFilePath = path + name + ".png"
		# add image to list, preserve transparency
		images.append(cv2.imread(letterImageFilePath,cv2.IMREAD_UNCHANGED)) 

	return images

# takes rows of a list and stacks them on top of each other to make an image
def CreateImageFromMatrix(list_2d):
	horizontalLines = []
	for list_h in list_2d:
		# take all the letter images and merge them into a line, then add to list
		horizontalLines.append(cv2.hconcat(list_h))

	# take the horizontal lines and stack them on top of each other
	return cv2.vconcat(horizontalLines)


# calculates the width,height of the output img based on number of input characters
def CalculateImageSize():
	totalCharacterCount = 0
	with open(InputTextFilePath, 'r') as file:
		while(True):
			currChar = file.read(1) # read the file one character at a time
			if not currChar: # if there are no more characters left end the loop
				break
			else:
				totalCharacterCount += 1 # increment the character count
	
	# ensure that (width * height) are always <= totalCharacterCount
	imgWidth = math.ceil(math.sqrt(totalCharacterCount))
	imgHeight = imgWidth
	
	# if image would be huge then quit out
	if(imgWidth > 12000): 
		print("error: text is too big to generate a reasonable image")
		exit()

	return imgWidth,imgHeight


# creates a width x height size list of character images from the input file
def CreateCharacterMatrix(images,imgWidth,imgHeight):
	letters = list(string.ascii_lowercase) # get list of lowercase alphabet
	letters.append(" ")
	
	imgMatrix = []
	
	with open(InputTextFilePath, 'r') as file:
		
		for i in range(0, imgHeight): # for each row
			imgLine = [] # start a new horizontal line
			
			for j in range(0, imgWidth): # for each character in the current row
				currChar = file.read(1).lower() # read one char at at time, forced lowercase
				
				if(currChar in letters): # if it is a-z or space
					idx = letters.index(currChar)
					imgLine.append(images[idx]) # add that character to the current image line 
				else:
					imgLine.append(images[-1]) # use space for any other character
					
			imgMatrix.append(imgLine) # add the current horizontal line

	return imgMatrix




def main():
	# determine image size
	imgWidth,imgHeight = CalculateImageSize()

	# get an image list that contains the letters/font
	letters = FontSetUp(OnionFolderPath)

	# get an image list of dimensions [width][height]
	charactersMatrix = CreateCharacterMatrix(letters,imgWidth,imgHeight)
	
	# convert the image list to a form thats ready to be saved
	outputImg = CreateImageFromMatrix(charactersMatrix)
	
	# save the image to drive
	cv2.imwrite(OnionOutputFilePath,outputImg)

	# repeat for normal font
	charactersMatrix = CreateCharacterMatrix(FontSetUp(NormalFolderPath),imgWidth,imgHeight)
	outputImg = CreateImageFromMatrix(charactersMatrix)
	cv2.imwrite(NormalOutputFilePath,outputImg)

if __name__ == "__main__":
	main()