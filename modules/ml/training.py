import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
# from modules.utils.utils import normalize_date


def season(x):
  if x in (1,2,12):
    return 'win'
  elif x in (3, 4, 5):
    return 'spr'
  elif x in (6, 7, 8):
    return 'sum'
  else:
    return 'aut'

def preprocess(df):
    # даты
    df.drop('is_fired', inplace=True)
    dates_features = ['startDate', 'endDate', 'birthDates']

    for i in dates_features:
        df[i].fillna(pd.Timestamp('now'), inplace=True)
        df[i] = pd.to_datetime(
            df[i],
            format='%Y-%m-%d'
        )
    df['age'] = pd.Timestamp('now')-df['birthDates']
    df['season'] = df['endDate'].dt.month.apply(lambda x: season(x))
    df['workingPeriod'] = (df['endDate'] - df['startDate']).dt.days
    df.drop(dates_features, axis=1, inplace=True)

    df.absenceDays.fillna(0, inplace=True)
    df.absenceReason.fillna('No', inplace=True)

    features_hot = ['speciality', 'absenceReason', 'season']
    features_ord = ['education', 'gender']
    df = pd.get_dummies(df, columns=features_hot+features_ord, sparse=False, drop_first=True)
    features_bool = ['is_married', 'mentored']
    df[features_bool] = df[features_bool].astype(int)
    df['city'] = df.city.replace('Москва', 1)
    df.loc[df['city'] != 1, 'city'] = 0

    df['salary'] = df['salary'] / 100
    return df


def train(employees):

    df = pd.DataFrame([vars(employee) for employee in employees])
    df.index = df.id
    df.drop('id', axis=1, inplace=True)

    df = preprocess(df)

    X = df.drop('workingPeriod', axis=1)
    y = df.pop('workingPeriod')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=1)

    model = RandomForestRegressor(min_samples_split=6, random_state=1)
    model.fit(X_train, y_train)
    dump(model, 'model.joblib')

if __name__=='__main__':
    """
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
                     mentored,
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
            self.mentored = mentored

"""

   # employees = [instance, instance2, instance3]
    train(employees)

