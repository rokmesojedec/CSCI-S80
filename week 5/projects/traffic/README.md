## Rok's Neural Net Notes
 
As part of CSCI S-80's Week 5 Project I have trained a neural network that can classify traffic sign images. 
I have based my model's code on the code example provided in the lecture. 
 
The model consists of a 2D convolutional layer that uses 32 filters with a 3x3 kernel. The input shape is 30x30x3. The activation function that works best for the convolutional layer is Sigmoid. 
 
Max-pooling layer is using 2x2 pool size. After I add a hidden layer with 128 neurons and sigmoid activation function. 0.5 dropout function is applied. 
 
Lowering the dropout rate from 0.5 to 0.1. Also, removing the dropout rate all together did not impact the accuracy or loss of the model. Increasing the dropout rate to 0.9 lowered to model accuracy to about 5%.
 
Changing activation function for the convolution and hidden networks from RuLU to sigmoid increased accuracy from ~0.05 to ~0.99. Apart from Softsign and sigmoid, other functions seem to produce low accuracy.
 
Doubling the sample image width and height made the training slower and less accurate (around 40% accuracy). Increasing the width and height by only 5px each, would drop the accuracy to 5%.  
 
Running graphically intense software in the background seems to decrease model accuracy. For example, when having a game open, the trained model would go up to 40% accuracy, as opposed to when turned off reaching about 98%. 
 
Increasing Epochs to more than 10, did not have a significant impact on accuracy. Loss did decrease slightly more.