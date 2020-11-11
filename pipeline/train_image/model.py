import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os
import argparse
import json
from storage import Storage
import logging


def prepare_data(file):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    import imblearn
    from imblearn.over_sampling import SMOTE
    
    def preprocess(data, is_train=False):
        
        data['day'] = pd.DatetimeIndex(data['date']).day
        data['month'] = pd.DatetimeIndex(data['date']).month
        data['year'] = pd.DatetimeIndex(data['date']).year
        
        cat_cols = ['armed','city','state','manner_of_death','gender','race','signs_of_mental_illness',
             'year','threat_level','flee','body_camera','arms_category']
        encoder = LabelEncoder()

        # Apply label encoder to each column
        encoded = data[cat_cols].apply(encoder.fit_transform)
        
        # join some important data features with the encoded variables
        df = data[['name','date','age','label']].join(encoded)
     
        df_copy = df.copy()
        df_copy = shuffle(df_copy)
        features = df_copy.drop(columns=['name','date','label'])
        target = df_copy['label']

#         test_features = test.drop(columns=['name','date','label'])
#         test_target = test['label']
        # Oversampling the undersampled labels
        if is_train:
            smote = SMOTE(random_state=0)
            X, y = smote.fit_sample(features, target)
        else:
            X, y = features, target
        
        # converting ndarray to dataframe
        X = pd.DataFrame(X, columns=features.columns)
        y = pd.Series(y, name=target.name)

        return X, y
    
    def f(row):
        
        '''
          Function that will be used to create the target column of two classes 1 and 0.
          Where 1 represents the unjustified cases and 0 represents the just ones. 
          '''
        if ((row['threat_level']=='undetermined' or row['threat_level']=='other') and (row['flee']=='Not fleeing')):
            val = 1

        else:
            val = 0
        return val

 
    file = 'shootings.csv'
    path = 'data'
    bucket = 'police-shootings'
    
    Storage.download(file, path, bucket)
    
    data = pd.read_csv(file)
    data['label'] = data.apply(f, axis=1)
    train, test = train_test_split(dataframe, test_size=0.2, random_state=100)
    
    trainset = preprocess(train, train=True)
    testset = preprocess(test)
    #     train, val = train_test_split(train, test_size=0.2, random_state=100)
        logging.info(f"Training data count: {trainset[0].shape}")
#     logging.info(f"Validation data count: {val.shape[0]}")
    logging.info(f"Testing data count: {testset[0].shape}")
    return trainset, testset

def build_model(
    n_estimators=200,
    max_features='auto',
    max_depth=10,
    min_samples_split=2,
    min_samples_leaf=1,
    bootstrap=True
):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_features=max_features,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        bootstrap=bootstrap
    )
    
    return model

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_estimators',
                        type=int,
                        default=200,
                        help="Number of estimators for random forest classifier")
    
    parser.add_argument('--max_features',
                    type=str,
                    default='auto',
                    help="maximum features")
    
    parser.add_argument('--max_depth',
                    type=int,
                    default=10,
                    help="Number of estimators for random forest classifier")
    
    parser.add_argument('--min_samples_split',
                    type=int,
                    default=200,
                    help="Minimum number of samples split for random forest classifier")
        
    parser.add_argument('--min_samples_leaf',
                type=int,
                default=200,
                help="Minimum number of leaves for random forest classifier")
            
    parser.add_argument('--bootstrap',
            type=bool,
            default=True,
            help="Bootstrap value for random forest classifier")
    
    parser.add_argument('--export-dir',
                    type=str,
                    default='/tmp/export',
                    help="GCS Path to export model")
    
    args = parser.parse_known_args()[0]
    return args


def main():
    import joblib
    import pickle
    from sklearn.metrics import roc_auc_score
    args = parse_arguments()
    
    train, test = prepare_data(data)
    model = build_model(
        n_estimators=int(args.n_estimators),
        max_features=str(args.max_features),
        max_depth=int(args.max_depth),
        min_samples_split=int(args.min_samples_split),
        min_samples_leaf=int(args.min_samples_leaf),
        bootstrap=bool(args.bootstrap)
    )
    
    logging.info("Training started...")
    
    X = train[0]
    y = train[1]
    rfc = model.fit(X, y)
    
    logging.info("Training completed")
    
    pickle.dump(rfc, 'rfc.pkl')
    logging.info("Model Saved")
    
    classifier = pickle.load('rfc.pkl')
    
    rfc_test_pred = classifier.predict_proba(test[0])
    auc_score = roc_auc_score(test_target, rfc_test_pred[:,1])
    logging.info(f"ROC-AUC Score: {auc_score}")
    
    joblib.dumb(classifier, 'tmp/export')
    Storage.upload('/tmp/export', args.export_dir)
    
    print("Process Complete.")
    
    exit(0)
    
    
if __name__ == "__main__":
    main()
    
    
    
    
                 
    
