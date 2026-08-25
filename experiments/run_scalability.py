from pathlib import Path
import pandas as pd, numpy as np, torch, time
from sklearn.model_selection import train_test_split
from kran.model import KRAN, KRANConfig
from kran.train import loaders, train_model, predict, set_seed
from kran.metrics import regression_metrics
rows=[]; rng=np.random.RandomState(42); n=5000
for d in [25,50,100,200,500]:
 X=rng.rand(n,d).astype(np.float32); y=(np.sin(2*np.pi*X[:,0])+X[:,1]**2+X[:,2]*X[:,3]+np.log1p(X[:,4])+rng.normal(0,.05,n)).astype(np.float32)[:,None]
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
 for G in [8,16,32]:
  set_seed(42); m=KRAN(KRANConfig(d,1,task='regression',mono_num_quad_points=G)); tr,te=loaders(Xtr,ytr,Xte,yte,256,'regression'); _,tt=train_model(m,tr,'regression',5,lr=1e-3,weight_decay=1e-4); yt,yp,it=predict(m,te,'regression'); r={'SyntheticDim':d,'G':G,**regression_metrics(yt,yp),'TrainTime_sec':tt,'InferenceTime_sec':it,'#Params':sum(p.numel() for p in m.parameters())}; rows.append(r); print(r)
Path('results').mkdir(exist_ok=True); pd.DataFrame(rows).to_csv('results/scalability.csv',index=False)
