"""Small deterministic GLMs and output helpers for offline exploratory analysis."""
from pathlib import Path
import csv
import json
import os
import tempfile
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, xlogy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/cpu'
OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='hf-mpl-'))


def save_json(name, value):
    def cast(v):
        if isinstance(v, np.generic): return v.item()
        if isinstance(v, np.ndarray): return v.tolist()
        raise TypeError(type(v))
    (OUT / name).write_text(json.dumps(value, indent=2, default=cast, allow_nan=False)+'\n')


def save_csv(name, rows):
    if not rows: return
    with (OUT / name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def glm_predict(train_x, train_y, test_x, kind, penalty=1.0):
    """L2 penalty on standardized slopes; unpenalized intercept; training-only scaling."""
    mean=train_x.mean(axis=0); scale=train_x.std(axis=0);scale[scale<1e-8]=1
    x=np.column_stack([np.ones(len(train_x)),(train_x-mean)/scale])
    xt=np.column_stack([np.ones(len(test_x)),(test_x-mean)/scale])
    initial=np.zeros(x.shape[1]); avg=np.mean(train_y)
    initial[0]=np.log((avg+1e-4)/(1-avg+1e-4)) if kind=='logistic' else np.log(avg+1e-4)
    def objective(b):
        z=x@b
        if kind=='logistic':
            value=np.sum(np.logaddexp(0,z)-train_y*z);grad=x.T@(expit(z)-train_y)
        else:
            # Bounds below keep coefficients finite; overflow is rejected by line search.
            with np.errstate(over='ignore'):
                mu=np.exp(z);value=np.sum(mu-train_y*z);grad=x.T@(mu-train_y)
        return value+penalty*np.sum(b[1:]**2)/2, grad+penalty*np.r_[0,b[1:]]
    fit=minimize(objective,initial,jac=True,method='L-BFGS-B',bounds=[(-25,25)]*len(initial),options={'maxiter':1000,'ftol':1e-10})
    if not fit.success: raise RuntimeError(f'GLM failed: {fit.message}')
    z=xt@fit.x
    pred=expit(z) if kind=='logistic' else np.exp(np.clip(z,-25,25))
    return pred, {'converged':bool(fit.success),'iterations':int(fit.nit),'max_abs_coefficient':float(np.max(np.abs(fit.x)))}


def binary_scores(y,p):
    brier=float(np.mean((y-p)**2))
    p=np.clip(p,1e-8,1-1e-8)
    return {'brier':brier,'log_loss':float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))}


def count_scores(y,p):
    mae=float(np.mean(np.abs(y-p)))
    p=np.clip(p,1e-8,None)
    return {'mae':mae,'poisson_deviance':float(2*np.mean(xlogy(y,y/p)-(y-p)))}
