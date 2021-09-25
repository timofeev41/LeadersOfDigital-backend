from joblib import load
import pandas as pd
import numpy as np
from training import preprocess


class EmployeeEntry():
    def __init__(self,
                 id,
                 speciality,
                 birthDate,
                 education,
                 gender,
                 is_married,
                 startDate,
                 endDate,
                 absenceReason,
                 absenceDays,
                 salary,
                 city,
                 childrenCount,
                 is_fired,
                 mentors,
                 ):
        self.id = id
        self.speciality = speciality
        self.birthDate = birthDate
        self.education = education
        self.gender = gender
        self.is_married = is_married
        self.startDate = startDate
        self.endDate = endDate
        self.absenceReason = absenceReason
        self.absenceDays = absenceDays
        self.salary = salary
        self.city = city
        self.childrenCount = childrenCount
        self.is_fired = is_fired
        self.mentors = mentors


class Analitics:
    def __init__(self, employees):
        self.model = load("model.joblib")
        # self.model = model
        self.df = pd.DataFrame([vars(employee) for employee in employees])
        self.df.index = self.df.id
        self.df.drop("id", axis=1, inplace=True)

    def preprocess(self, X):
        df_preprocessed = preprocess(X)
        return df_preprocessed

    def predict(self):
        df2 = self.df.copy()
        df2 = self.preprocess(df2)
        X = df2.drop("workingPeriod", axis=1)

        start_dates = pd.to_datetime(pd.Series(self.df["startDate"].values, index=self.df.index), format="%d/%m/%Y")

        predictions = self.model.predict(X)

        left_days = (
            (
                start_dates
                + pd.Series(np.ceil(predictions), index=start_dates.index).apply(lambda x: pd.Timedelta(x, unit="D"))
                - pd.Timestamp("now")
            ).dt.days
        ).apply(lambda x: max(x, 0))

        return left_days


# df = pd.read_csv('Данные для аналитики2.txt', encoding='utf-16', sep = "\t", index_col='ID')
# cl = Analitics(X=df)
if __name__ == "__main__":
    instance = EmployeeEntry(id=108,
                             speciality='Ведущий инженер',
                             birthDate='02/07/2002',
                             education='school',
                             gender="male",
                             is_married=True,
                             startDate='10/10/2021',
                             endDate='15/10/2024',
                             absenceReason=None,
                             absenceDays=None,
                             salary=38900,
                             city='Москва',
                             childrenCount=2,
                             is_fired=True,
                             mentors=False

                             )
    instance2 = EmployeeEntry(id=101,
                              speciality='Уборщик',
                              birthDate='02/07/2002',
                              education='higher',
                              gender="female",
                              is_married=True,
                              startDate='10/10/2021',
                              endDate='10/10/2022',
                              absenceReason='Ilness',
                              absenceDays=2,
                              salary=3900,
                              city='Москва',
                              childrenCount=2,
                              is_fired=True,
                              mentors=True

                              )

    instance3 = EmployeeEntry(id=102,
                              speciality='Уборщик',
                              birthDate='02/07/2002',
                              education='college',
                              gender="female",
                              is_married=False,
                              startDate='10/10/2021',
                              endDate='10/10/2023',
                              absenceReason='Holiday',
                              absenceDays=5,
                              salary=18000,
                              city='Припять',
                              childrenCount=10,
                              is_fired=True,
                              mentors=False

                              )





    employees = [instance, instance2, instance3]
    predictor = Analitics(employees)


    print(predictor.predict())
