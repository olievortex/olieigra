from datetime import datetime

print("____  _____")
print("Olie\\/ortex Analytics: ProductionLi.py")
print()
print(f"Create Lifted Index predictions from Deep Learning Model")
print()
print(f"Effective date: 2010 - 2025 Chanhassen")

start = datetime.now()
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import torch

from sklearn.preprocessing import MinMaxScaler

PARQUET_PATH = '/usr/datalake/silver/igra/liftedindex_lr/gph20s10k_li.parquet'
ARTIFACTS_PATH = '/usr/datalake/silver/igra/liftedindex_lr/artifacts'

print(f"Imports        : {(datetime.now()-start).total_seconds()*1000.:.2f}ms")
start = datetime.now()

def load_dataset():
    df = pd.read_parquet(PARQUET_PATH)

    # Separate the datasets
    X = df.drop(['id', 'effective_date', 'hour', 'li'], axis=1)
    Y = df['li'].values
    
    # Scale the X dataset
    ss = load_standard_scaler() 
    X = ss.transform(X)
   
    return X, Y

def load_standard_scaler()-> MinMaxScaler:
    with open(f'{ARTIFACTS_PATH}/li_std_scaler.skl', 'rb') as f:
        std_scaler = pickle.load(f)

    return std_scaler

class LiModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(127, 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 1)
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)

        return logits
model = LiModel()
model.load_state_dict(torch.load(f'{ARTIFACTS_PATH}/li_fnn.pt'))
model.eval()

X, Y = load_dataset()

logits = model.forward(torch.from_numpy(X).float())
Y_pred = logits.data.numpy()

print(f"Make Prediction: {(datetime.now()-start).total_seconds()*1000.:.2f}ms")
start = datetime.now()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

ax1.title.set_text('Interesting Region')
ax1.scatter(Y, Y_pred)
ax1.plot((-14, 50), (-14, 50), c='k')
ax1.set_xlabel('actual')
ax1.set_ylabel('prediction')
ax1.set_ylim(-14, 6)
ax1.set_xlim(-14, 6)

ax2.title.set_text('Full Region')
ax2.scatter(Y, Y_pred)
ax2.plot((-14, 50), (-14, 50), c='k')
ax2.set_xlabel('actual')
ax2.set_ylabel('prediction')

print(f"Draw Graph     : {(datetime.now()-start).total_seconds()*1000.:.2f}ms")
start = datetime.now()

plt.show()
