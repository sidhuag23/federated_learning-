import flwr as fl
import numpy as np
import csv

DATA_FILE = "spam1.csv"   # change to spam2.csv for device_2

X = []
y = []

with open(DATA_FILE) as f:
    reader = csv.DictReader(f)

    for row in reader:
        X.append([
            float(row["links"]),
            float(row["suspicious_words"])
        ])

        y.append(int(row["label"]))

X = np.array(X, dtype=float)
y = np.array(y)

class PerceptronClient(fl.client.NumPyClient):

    def __init__(self):
        self.w = np.zeros(2, dtype=float)
        self.b = 0.0
        self.lr = 0.1

    def get_parameters(self, config):
        return [self.w, np.array([self.b])]

    def set_parameters(self, parameters):
        self.w = parameters[0]
        self.b = parameters[1][0]

    def fit(self, parameters, config):

        self.set_parameters(parameters)

        for x, label in zip(X, y):

            z = np.dot(self.w, x) + self.b
            pred = 1 if z > 0 else 0

            error = label - pred

            self.w += self.lr * error * x
            self.b += self.lr * error

        return [self.w, np.array([self.b])], len(X), {}

    def evaluate(self, parameters, config):

        self.set_parameters(parameters)

        correct = 0

        for x, label in zip(X, y):

            z = np.dot(self.w, x) + self.b
            pred = 1 if z > 0 else 0

            if pred == label:
                correct += 1

        acc = correct / len(X)

        return 0.0, len(X), {"accuracy": acc}


fl.client.start_numpy_client(
    #server_address="localhost:8080",
    server_address="fl_server:8080",
    client=PerceptronClient()
)
### fl-serve for docker only 
