import numpy as np


#
# Write a python class “perceptron” by implementing the following member functions:
#
# def __init__(self): initializes the member variable self.synaptic_weights with random values
#
# def sigmoid(self,x) : sigmoid function
#
# def sigmoid_derivative(self,x) : derivative of sigmoid function
#
# def think(self, inputs): one “thought-step” of the perceptron for the given inputs. Returns outputs.
#
# def train(self, inputs, targets, iterations) : the training loop.
# Shall be exectuted “iterations”-times to train the network. Does contain backpropagation and weight adjustments.

#
# if __name__ == “__main__”: the main function.
# creates one instance of class perceptron, trains it with the training data
# and asks the user to enter values for the signals I1, I2 and I3. Prints out perceptron’s belief afterwards
class Perceptron():
    #def __init__(self, n_inputs, n_outputs):
    def __init__(self, n):
        self.synaptic_weights = np.random.random((n, 1)) - 1
        #self.synaptic_weights = np.random.normal(0.0, pow(n_inputs, -0.5), (n_inputs, n_outputs))
        print("Initial synaptic weights:", self.synaptic_weights)

    # sigmoid function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # derivative of sigmoid function
    def sigmoid_derivative(self, x):
       # return self.sigmoid(x) * (1 - self.sigmoid(x))
        return x * (1 - x)

    # training loop
    def train(self, inputs, targets, iterations):
        for i in range(iterations):
            outputs=self.think(inputs)
            #print('out',outputs)
            errors = targets - outputs
            deltaW= np.dot(inputs.T, errors * self.sigmoid_derivative(outputs))
            self.synaptic_weights += deltaW

        print("Synaptic weights after training:", self.synaptic_weights)

    def think(self, inputs):
        inputs = inputs.astype(float)
        outputs = self.sigmoid(np.dot(inputs, self.synaptic_weights))
        return outputs


if __name__ == "__main__":
    p = Perceptron(3)
    training_data= np.array([
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 1]])

    # Target outputs
    training_outputs = np.array([[0, 1, 1, 0]]).T

    # Train the Perceptron
    p.train(training_data, training_outputs, 100)

    user_input = input("Enter 3 binary inputs: ").strip()

    user_input_values = [float(c) for c in user_input]
    user_input_array = np.array([user_input_values])
    output = p.think(user_input_array)
    print("Perceptron prediction:", output[0][0])
    print("Predicted output:", round(output[0][0]))