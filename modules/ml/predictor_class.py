from joblib import load
import pandas as pd
import numpy as np
from training import preprocess

# some_data_passed



class Analitics():
    def __init__(self, employees):
        self.model = load('model.joblib')
        # self.model = model
        self.df = pd.DataFrame([vars(employee) for employee in employees])
        self.df.index = self.df.id
        self.df.drop('id', axis=1, inplace=True)

    def preprocess(self, X):
        df_preprocessed = preprocess(X)
        return df_preprocessed

    def predict(self):
        df2 = self.df.copy()
        df2 = self.preprocess(df2)
        X = df2.drop('workingPeriod', axis=1)

        start_dates = pd.to_datetime(
            pd.Series(self.df['startDate'].values, index=self.df.index),
            format="%d/%m/%Y"
        )

        predictions = self.model.predict(X)

        left_days = ((start_dates + pd.Series(np.ceil(predictions), index=start_dates.index).apply(
                         lambda x: pd.Timedelta(x, unit='D')) - pd.Timestamp('now')
                     ).dt.days
                     ).apply(lambda x: max(x, 0))

        return left_days

#df = pd.read_csv('Данные для аналитики2.txt', encoding='utf-16', sep = "\t", index_col='ID')
#cl = Analitics(X=df)
if __name__=="__main__":

    # employees = [instance, instance2, instance3]
    predictor = Analitics(employees)
    print(predictor.predict())



