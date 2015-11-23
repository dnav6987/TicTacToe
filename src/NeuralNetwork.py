import math
from random import random

# Feed forward, back propagation neural network. Highly influenced by a Ron Cemer
# blog post (http://roncemer.com/software-development/tic-tac-toe-an-experiment-in-machine-learning/).
# 
# Every neuron is connected to every neuron in the adjacent layers.
# The weights determine how highly to weight each connections.
# The thresholds determines if a neuron can 'fire'.
# Every time we change the weights we also add a component that is the product of the previous
# weight change and the momentum so that we do not get stuck in any local maxima.
# The learning rate determines how much we change the weights by on each iteration.
# Error gradients are used as an optimization to minimize the loss function.

class NeuralNetwork:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.num_layers = len(num_neurons)

        self.momentum = 0.8
        self.learning_rate = 0.2

        # initalize the lists of data

        self.neurons = [[] for i in range(self.num_layers)]
        self.thresholds = [[] for i in range(self.num_layers)]
        self.weights = [[] for i in range(self.num_layers - 1)]
        self.last_weight_changes = [[] for i in range(self.num_layers - 1)]
        self.error_gradients = [[] for i in range(self.num_layers)]     

        for layer in range(self.num_layers):
            self.neurons[layer] = [0. for i in range(self.num_neurons[layer])]
            self.error_gradients[layer] = [0. for i in range(self.num_neurons[layer])]
            self.thresholds[layer] = [self.rand() for i in range(self.num_neurons[layer])] # randomize thresholds

            if layer > 0:
                self.weights[layer-1] = [[] for i in range(self.num_neurons[layer-1])]
                self.last_weight_changes[layer-1] = [[] for i in range(self.num_neurons[layer-1])]

                for prev_neuron in range(len(self.weights[layer-1])):
                    self.weights[layer-1][prev_neuron] = [self.rand() for i in range(self.num_neurons[layer])] # randomize weights
                    self.last_weight_changes[layer-1][prev_neuron] = [0. for i in range(self.num_neurons[layer])]

    # return a random number in range [-0.5, 0.5)
    def rand(self):
        return (random() - 0.5)/2.0

    def set_input(self, inputs):
        if len(inputs) == len(self.neurons[0]):
            self.neurons[0] = inputs
        else:
            raise RuntimeError('must set inputs with the same number of input neurons')

    def set_learning_rate(self, rate):
        self.learning_rate = rate

    def set_momentum(self, momentum):
        self.momentum = momentum

    def get_input(self):
        return self.neurons[0]

    def get_output(self):
        return self.neurons[self.num_layers-1]

    # propagate the input through the network
    def forward_propagate(self):
        for layer in range (1, self.num_layers):    # start at layer just above inputs
            # for each neuron, calculate the weighted sum of all the neurons connected to it in the previous layer
            # and put it in the activation function
            for neuron in range(self.num_neurons[layer]):
                weighted_sum = 0

                for prev_neuron in range(self.num_neurons[layer-1]): # each neuron in the previous layer
                    weighted_sum += self.neurons[layer-1][prev_neuron] * self.weights[layer-1][prev_neuron][neuron]

                # non-linear transformation from the weighted sum to calculate this nuerons value.
                # if greater than threshold, will be possitive, else negative
                self.neurons[layer][neuron] = self.activation_func(weighted_sum-self.thresholds[layer][neuron])

    # given the expected outputs, calculate the errors and change the weights
    def back_propagate(self, expected):
        if len(expected) != len(self.get_output()):
            raise RuntimeError('expected output must be of same size as output layer')

        for layer in range (self.num_layers-1, 0, -1):  # starting at output layer, working down to input layer
            for neuron in range(self.num_neurons[layer]): # each neuron
                if layer == self.num_layers-1: # output layer
                        error = expected[neuron] - self.neurons[layer][neuron] # how far off the output was from the correct output
                        self.error_gradients[layer][neuron] = self.inverse_activation_func(self.neurons[layer][neuron]) * error # calculate the gradient

                else:   # not the output layer
                    weighted_error_grad = 0

                    for next_neuron in range(self.num_neurons[layer+1]): # calculate the weighted error gradient propagated down from layer above
                        weighted_error_grad += self.error_gradients[layer+1][next_neuron] * self.weights[layer][neuron][next_neuron]

                    self.error_gradients[layer][neuron] = self.inverse_activation_func(self.neurons[layer][neuron]) * weighted_error_grad # calculate this gradient

                # update the weights changes between this neuron and the neurons on the layer below
                for prev_neuron in range(self.num_neurons[layer-1]):
                    # component of weight change from this iteration
                    weight_change = self.learning_rate * self.neurons[layer-1][prev_neuron] * self.error_gradients[layer][neuron]
                    # add component from previous iteration using momentum
                    self.weights[layer-1][prev_neuron][neuron] += weight_change + self.last_weight_changes[layer-1][prev_neuron][neuron] * self.momentum

                    self.last_weight_changes[layer-1][prev_neuron][neuron] = weight_change

                # set the threshold
                self.thresholds[layer][neuron] -= self.learning_rate * self.error_gradients[layer][neuron]

    # activation function is hyperbolic tan
    def activation_func(self, val):
        return math.tanh(val)

    # inverse activation function. sech^2(x): sech^2(x) + tanh^2(x) = 1
    def inverse_activation_func(self, val):
        temp = math.tanh(val)
        return (1 - (temp**2))

    # test the neural network by learning some binary logical operators
    @staticmethod
    def test(num_iterations):
        print '\n\nTesting Neural Net on Truth Table\n\n'

        NN = NeuralNetwork([2,2,1])

        TRUE = {
                        (0,1) : 1,
                        (1,1) : 1,
                        (1,0) : 1,
                        (0,0) : 1
                }

        FALSE = {
                        (0,1) : 0,
                        (1,1) : 0,
                        (1,0) : 0,
                        (0,0) : 0
                }

        AND = {
                        (0,1) : 0,
                        (1,1) : 1,
                        (1,0) : 0,
                        (0,0) : 0
                }

        NAND = {
                        (0,1) : 1,
                        (1,1) : 0,
                        (1,0) : 1,
                        (0,0) : 1
                }

        OR = {
                        (0,1) : 1,
                        (1,1) : 1,
                        (1,0) : 1,
                        (0,0) : 0
                }


        XOR = {
                        (0,1) : 1,
                        (1,1) : 0,
                        (1,0) : 1,
                        (0,0) : 0
                }

        NOR = {
                        (0,1) : 0,
                        (1,1) : 0,
                        (1,0) : 0,
                        (0,0) : 1
                }

        binary_operators = {
                                'TRUE' : TRUE,
                                'FALSE' : FALSE,
                                'AND' : AND,
                                'NAND' : NAND,
                                'OR' : OR,
                                'XOR' : XOR,
                                'NOR' : NOR
                            }

        for operator, truth_table in binary_operators.iteritems():
            print 'Learning binary operator:', operator

            for this_pass in range(num_iterations):
                # should_print = not this_pass or not ((this_pass)%1000)
                # if should_print: print 'Pass:', (this_pass)

                for inputs in truth_table:
                    expected = [truth_table[inputs]]
                    NN.set_input(list(inputs))
                    NN.forward_propagate()
                    NN.back_propagate(expected)

                    # if should_print:
                    #     print 'in: ', inputs, 'out: ', NN.get_output(), 'expected:', expected

            for inputs in truth_table:
                expected = truth_table[inputs]
                NN.set_input(inputs)
                NN.forward_propagate()

                print 'in: ', inputs, 'out: ', NN.get_output(), 'expected:', expected, '\n'