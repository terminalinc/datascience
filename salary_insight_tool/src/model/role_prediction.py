def predict_role(df, index, skills_list):
    import joblib
    import pandas as pd
    import numpy as np
    role_classification_model = joblib.load("src/model/role_classification_model.sav")
    model_skill_df = pd.read_csv("data/reference/model_skill_df.csv")
    
    common_skill_list = list(model_skill_df['skill'])
    
    # remove all na from skill list
    df_ss = df[~df[skills_list].isna()]
    
    for s in common_skill_list:
        df_ss.loc[:, s] = 0
        df_ss.loc[df_ss[skills_list].str.lower().str.contains(s), s] = 1
        
    # Exclude all roles without matching skills
    df_ss['skill_count'] = df_ss[common_skill_list].sum(axis=1)
    df_ss = df_ss[df_ss['skill_count'] > 0].reset_index(drop=True)    
    
    df_x = df_ss.loc[:, common_skill_list]
    
    if len(df_x) > 0:
    
        quantify_prediction = pd.DataFrame(role_classification_model.predict_proba(df_x))
        quantify_prediction.columns = list(role_classification_model.classes_)
        quantify_prediction['confidence'] = quantify_prediction[list(role_classification_model.classes_)].max(axis=1)
        quantify_prediction['predicted_role'] = role_classification_model.predict(df_x)
        
        df_x['predicted_role'] = np.where(quantify_prediction['confidence'] > 0.35, quantify_prediction['predicted_role'], '')
        
        results = pd.concat([df_ss[index], 
                   df_x[['predicted_role']]], axis = 1)
        
        output = pd.merge(df, results, 
                                    on = index, 
                                    how = 'left')
    else:
        output = df.copy()
        output['predicted_role'] = ''
    
    return output

#output.to_csv('temp.csv')

# job_ft = pd.read_csv("/Sync/3_Professional/Terminal_Sync/data/job/job_ft.csv")
# df = job_ft[['job_id', 'created_at', 'required_skills']][0:500]

# index = ['job_id']
# skills_list = 'required_skills'

# predict_role(df, index, skills_list)
