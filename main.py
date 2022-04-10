from PIL import Image
import matplotlib.pyplot as plt

input = Image.open("input.png")
if(input.width == 256):
    input = input.crop((20, 0, 236, input.height))  #Crop out black borders on the left and right of the image. This will hopefully result in more contrast after normalization.
    print("Detected satDump ASCAT resolution. Proceeding with cropped image.")
else:
    print("Was not able to detect standard satDump width. The script will proceed without cropping.")
output = Image.new("I", (input.width, input.height))

#This creates the average of every column and plots them over the width of the image
X_values = [a for a in range(input.width)]
averages = [0 for a in range(input.width)]
for x in range(input.width):
    for y in range(input.height):
        averages[x] = averages[x] + input.getpixel((x, y)) #Sums up all pixelvalues of one column
    averages[x] = int(averages[x] / input.height) #devides by number of rows to get the average
    if(averages[x] < 0):
        averages[x] = 0
plt.plot(X_values, averages)
plt.savefig("noisepattern.png", bbox_inches = 'tight', pad_inches = 0)

#This substracts the created noise pattern from the original image to create a hopefully denoised image
lowest_val = 65535
highest_val = 0
for a in range(input.height):
    for b in range(input.width):
        pixelvalue = input.getpixel((b, a))
        corrected_pixelvalue = pixelvalue - averages[b]
        output.putpixel((b, a), corrected_pixelvalue)
        if(corrected_pixelvalue < lowest_val):
            lowest_val = corrected_pixelvalue
        if(corrected_pixelvalue > highest_val):
            highest_val = corrected_pixelvalue

#This normalizes the created image
for i in range(input.width):
    for j in range(input.height):
        value_is = output.getpixel((i,j))
        value_normalized = int(65535*((value_is - lowest_val) / (highest_val - lowest_val)))
        output.putpixel((i,j), value_normalized)
output.save("ASCAT_denoised.png")

#This uses PLT to color the images
bw_input = plt.imread("ASCAT_denoised.png")
plt.axis('off')
plt.imshow(bw_input, cmap = 'jet')
plt.savefig("colored.png", bbox_inches = 'tight', dpi = 1200, pad_inches = 0)