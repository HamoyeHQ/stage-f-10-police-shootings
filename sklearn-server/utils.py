def transform(instance):
    import pickle
    import numpy as np
    cat_cols = ['state', 'arms_category', 'race']
    
    encoders_dict = {}
    classes_dict = {}
    
    for index, col in enumerate(cat_cols):
        with open(f"{col}_encoder.pkl", "rb") as enc:
            encoders_dict[f"{col}_encoder"] = pickle.load(enc)
            classes_dict[f"{col}_classes"] = encoders_dict[f"{col}_encoder"].classes_
            
    instance[1] = np.where(classes_dict['race_classes'] == instance[1])[0][0]
    instance[2] = np.where(classes_dict['state_classes'] == instance[2])[0][0]
    instance[3] = np.where(classes_dict['arms_category_classes'] == instance[3])[0][0]

    instance[4] = 0 if instance[4] == "F" else 1
    instance[5] = 0 if instance[5] == "false" else 1
    instance[6] = 0 if instance[6] == "shot" else 1
    instance[7] = 0 if instance[7] == "false" else 1
    
    return instance


def predict(instances):
    import numpy as np
    import joblib
    
    try:
        inputs = np.array(instances)
    except Exception as e:
        raise Exception(f"failed to initialize numpy array from inputs {e}, {instances}")

    try:
        model = joblib.load('model.joblib')
        result = model.predict_proba(inputs).tolist()
        return result

    except Exception as e:
        raise Exception(f"Failed to predict {e}")
    
def postprocess(inputs):
    import numpy as np
    
    classes = ["justified", "unjustified"]
    predictions = np.array(inputs)
    result = [str(classes[x]) for x in list(np.argmax(predictions, axis=1))]
    return result


# def download_blob(bucket, source, destination):
#     from google.cloud import storage
    
#     client = storage.Client()
#     bucket = client.bucket(bucket)
#     blob = bucket.blob(source)
#     blob.download_to_filename(destination)
    