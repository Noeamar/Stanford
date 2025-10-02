from stabl.single_omic import single_omic_simple, save_single_omic_results
from stabl.EMS import generateModel,read_json,write_json,unroll_parameters
from sklearn.model_selection import LeaveOneOut,LeaveOneGroupOut, RepeatedStratifiedKFold, GroupShuffleSplit
from stabl.stabl import save_stabl_results
from stabl.sherlock import run_end
from pathlib import Path
import numpy as np
import pandas as pd
import argparse
import os 


datasetsDict = {"func" : "../data/EMIMCmdiop_functional.csv",
            "metav" : "../data/EMIMCmdiop_metavariables.csv",
            "celldensities" : "../data/EMIMCmdiop_celldensities.csv",
            "neighborhood" : "../data/EMIMCmdiop_neighborhood.csv"
            }
datasets = [pd.read_csv(datasetsDict[d],index_col=0) for d in datasetsDict.keys()]
datasetCols = {d: datasets[i].columns for i,d in enumerate(datasetsDict.keys())}
df = pd.concat(datasets,axis=1)
y =  pd.read_csv(f"../data/StageI&IIVsStageIII&IV.csv",index_col=0).Stage

df = df.loc[[ e for e in y.index if e in df.index],:]
y = y.loc[df.index]

taskType = 'binary'

groups = pd.Series([e.split("_")[3] for e in y.index],index=y.index)

orderby = "ROC AUC" if taskType == "binary" else "R2"
keepTop = 5

paramFilePath = "./params.json"
savePathRoot = "./results"
os.makedirs(savePathRoot, exist_ok=True)

def experiment(paramSet: dict,idx: int,savePath: str):
    name = str(idx)

    outerSplitter = GroupShuffleSplit(n_splits = 200, test_size=0.2, random_state=paramSet["cvSeed"])

    stim = paramSet["dataset"]
    ef = (stim == "EarlyFusion")
    if ef:
        data = df
    else:
        data = df[datasetCols[stim]]


    preprocessing,model = generateModel(paramSet)
    results = single_omic_simple(
        data,
        y,
        outerSplitter,
        model,
        paramSet["model"],
        preprocessing,
        taskType,
        ef = ef,
        outer_groups = groups
    )
    save_single_omic_results(y,results,savePath,taskType)

    if "stabl" in paramSet["model"]:
        data_std = pd.DataFrame(
            data=preprocessing.fit_transform(data),
            index=data.index,
            columns=preprocessing.get_feature_names_out()
        )
        model.fit(data_std,y)
        modelPath = Path(savePath,name,"fullModel")
        os.makedirs(modelPath,exist_ok = True)
        save_stabl_results(model,modelPath,data,y,override=True)



def postProcess(paramFilePath: str ):
    run_end(paramFilePath,df,y,taskType)

        




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=int, default=0)
    parser.add_argument("idx", type=int, default=0,nargs="?")
    parser.add_argument("intensity",type=str,default='l',nargs="?")
    args = parser.parse_args()
    if args.mode == 0:
        path = Path(savePathRoot,str(args.intensity),str(args.idx))
        experiment(read_json(Path(path,"params.json")),args.idx,path)
    elif args.mode == 1:
        postProcess(paramFilePath)
        
