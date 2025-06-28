import numpy as np
from task4_1 import Perceptron
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


class NeuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes):
        self.hidden_layer = Perceptron(inputnodes, hiddennodes)
        self.output_layer = Perceptron(hiddennodes, outputnodes)

    def think(self, inputs):
        inputs = inputs.reshape(1, -1)  #2d
        hidden_output = self.hidden_layer.think(inputs)
        final_output = self.output_layer.think(hidden_output)
        return final_output

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, inputs, targets, iterations=100, lr=0.3):
        for _ in range(iterations):
            # Forward pass
            hidden_output = self.hidden_layer.think(inputs) #784->200 (1,200)
            final_output = self.output_layer.think(hidden_output)#200->10 (1,10)
            # Error at output
            output_error = targets - final_output #(1,10)
            output_gradient = output_error * self.sigmoid_derivative(final_output)
            output_delta = np.dot(hidden_output.T, output_gradient)

            #print(hidden_output.shape, final_output.shape, output_delta.shape, output_error.shape, output_gradient.shape)

            # Error at hidden
            hidden_error = np.dot(output_gradient, self.output_layer.synaptic_weights.T)
            hidden_gradient = hidden_error * self.sigmoid_derivative(hidden_output)
            hidden_delta = np.dot(inputs.T, hidden_gradient)
            #print(hidden_error.shape, hidden_gradient.shape, hidden_delta.shape)

            # Update weights
            self.output_layer.synaptic_weights += output_delta*lr
            self.hidden_layer.synaptic_weights += hidden_delta*lr

        #save weights
        np.save("hidden_weights.npy", self.hidden_layer.synaptic_weights)
        np.save("output_weights.npy", self.output_layer.synaptic_weights)


if __name__ == "__main__":
    NN = NeuralNetwork(784, 200, 10)

    with open("C:/Users/rabab/Desktop/SS25/mnist_train_100.csv", "r") as f:
        training_data_list = f.readlines()

    with open("C:/Users/rabab/Desktop/SS25/mnist_test_10.csv", "r") as f:
        test_data_list = f.readlines()

#nputdata (grayscale values) : [0:254] => [0.01:0.99]
#targets (label): If the input is labeled with label i, the i-th position in the target data array is set to 0.99,#
#all other values of the array to 0.01. E.g.: label == 7 => targets[7] = 0.99, all other 0.01

    for data in training_data_list:
        values = data.strip().split(',')
        inputs = ((np.asarray(values[1:], dtype=np.float32) / 255.0) * 0.99) + 0.01
        inputs = np.array([inputs])  # shape (1, 784)

        targets = np.full((1, 10), 0.01)
        targets[0][int(values[0])] = 0.99

        NN.train(inputs, targets)

    # Evaluate performance
    scorecard = []

    # for data_point in test_data_list:
    #     values = data_point.strip().split(',')
    #     correct_label = int(values[0])
    #     inputs = (np.asarray(values[1:], dtype=np.float32) / 255.0 * 0.99) + 0.01
    #
    #     outputs = NN.think(inputs)
    #     label = np.argmax(outputs)
    #
    #     scorecard.append(1 if label == correct_label else 0)
    #
    # print("Performance: {:.2f}%".format(100 * np.mean(scorecard)))

    # Test NN
    fig, axes = plt.subplots(2, 5, figsize=(10, 10))  # 5x5 grid
    fig.suptitle("Predictions vs Targets", fontsize=16)

    for i, data_point in enumerate(test_data_list[:10]):
        raw_values = data_point.strip().split(',')
        correct_label = int(raw_values[0])

        image_array = np.asarray(raw_values[1:], dtype=np.float32).reshape((28, 28))
        inputs = (np.asarray(raw_values[1:], dtype=np.float32) / 255.0 * 0.99) + 0.01

        #predictions
        outputs = NN.think(inputs)
        predicted_label = np.argmax(outputs)
        scorecard.append(1 if predicted_label == correct_label else 0)

        # Plotting
        ax = axes[i // 5, i % 5]
        ax.imshow(image_array, cmap='Greys', interpolation='none')
        ax.set_title(f"T:{correct_label} P:{predicted_label}", fontsize=10)
        ax.axis('off')

    print("Performance: {:.2f}%".format(100 * np.mean(scorecard)))
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()
