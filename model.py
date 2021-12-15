import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as Function

import os


class linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.linear_layer1 = nn.Linear(input_size, hidden_size)
        self.linear_layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = Function.relu(self.linear_layer1(x))
        x = self.linear_layer2(x)

        return x

    def save(self, file_name="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class Q_Trainer:
    def __init__(self, model, learning_rate, gamma):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def train_step(self, state_current, action, reward, state_next, done):
        state_current = torch.tensor(state_current, dtype=torch.float)
        state_next = torch.tensor(state_next, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state_current.shape) == 1:
            state_current = torch.unsqueeze(state_current, 0)
            state_next = torch.unsqueeze(state_next, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current status
        prediction = self.model(state_current)

        target = prediction.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(state_next[idx])
                )

            target[idx][torch.argmax(action).item()] = Q_new

        # 2: r + y * max(next prediction Q value)
        self.optimizer.zero_grad()

        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()
