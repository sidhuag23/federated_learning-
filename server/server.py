import flwr as fl
import time


class SlowFedAvg(fl.server.strategy.FedAvg):

    def aggregate_fit(self, server_round, results, failures):

        print("\n--- Aggregating round", server_round, "---")

        aggregated = super().aggregate_fit(server_round, results, failures)

        print("Waiting before next round...\n")
        time.sleep(5)   # wait 5 seconds

        return aggregated


strategy = SlowFedAvg()

fl.server.start_server(
    server_address="0.0.0.0:8080",
    config=fl.server.ServerConfig(num_rounds=10),
    strategy=strategy,
)
