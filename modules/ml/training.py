import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
import random



all_possible_features = ['is_married', 'absenceDays', 'salary', 'city', 'childrenCount',
       'is_fired', 'mentored', 'speciality_Ведущий инструктор',
       'speciality_Ведущий специалист', 'speciality_Ведущий экономист',
       'speciality_Главный специалист', 'speciality_Директор',
       'speciality_Специалист', 'speciality_Старший оператор',
       'speciality_Эксперт', 'speciality_аккумуляторщик',
       'speciality_аппаратчик', 'speciality_бухгалтер',
       'speciality_ведущий бухгалтер', 'speciality_ведущий инструктор',
       'speciality_ведущий специалист', 'speciality_ведущий юрисконсульт',
       'speciality_водитель автомобиля', 'speciality_главный бухгалтер',
       'speciality_главный инженер', 'speciality_главный инспектор',
       'speciality_главный специалист', 'speciality_дежурный',
       'speciality_диспетчер', 'speciality_заведующий складом',
       'speciality_заведующий хозяйством',
       'speciality_заместитель главного бухгалтера',
       'speciality_заместитель главного инженера',
       'speciality_заместитель директора',
       'speciality_заместитель начальника отдела',
       'speciality_заместитель начальника управления',
       'speciality_заместитель начальника цеха', 'speciality_заточник',
       'speciality_инженер', 'speciality_инспектор',
       'speciality_кладовщик 3 разряда', 'speciality_лаборант',
       'speciality_мастер', 'speciality_машинист', 'speciality_метролог',
       'speciality_начальник смены', 'speciality_начальник цеха',
       'speciality_оператор', 'speciality_слесарь', 'speciality_техник',
       'speciality_токарь', 'speciality_фрезеровщик 5 разряда',
       'speciality_фрезеровщик 6 разряда', 'speciality_шлифовщик 5 разряда',
       'speciality_шлифовщик 6 разряда', 'speciality_экономист',
       'speciality_эксперт', 'speciality_электрогазосварщик 4 разряда',
       'speciality_электрогазосварщик 5 разряда',
       'speciality_электрогазосварщик 6 разряда', 'speciality_электромеханик',
       'speciality_электромонтер', 'speciality_электрослесарь',
       'absenceReason_Командировка', 'absenceReason_Лист нетрудоспособности',
       'absenceReason_Отпуск', 'absenceReason_Прочие отсутствия', 'season_win', 'season_aut', 'season_spr', 'season_sum'
       'education_higher', 'education_school', 'education_college']







def season(x: int) -> str:
    if x in (1, 2, 12):
        return "win"
    elif x in (3, 4, 5):
        return "spr"
    elif x in (6, 7, 8):
        return "sum"
    else:
        return "aut"


def preprocess(df):
    dates_features = ['startDate', 'endDate', 'birthDate']
    for i in dates_features:
        df[i].fillna(pd.Timestamp('now'), inplace=True)
        df[i] = pd.to_datetime(
            df[i],
            format='%d/%m/%Y'
        )
    df['season'] = df['endDate'].dt.month.apply(lambda x: season(x))
    df['workingPeriod'] = (df['endDate'] - df['startDate']).dt.days
    df['age'] = round((pd.Timestamp('now') - df['birthDate']).dt.days / 365)  # .astype('<m8[Y]')
    # df.drop(dates_features, axis=1, inplace=True

    # impute
    df.absenceDays.fillna(0, inplace=True)
    df.absenceReason.fillna('No', inplace=True)
    features_bool = ["is_married", "mentored"]
    df[features_bool] = df[features_bool].astype(int)
    df["city"] = df.city.replace("Москва", 1)
    df.loc[df["city"] != 1, "city"] = 0
    df['gender'] = df.gender.replace('male', 0)
    df.loc[df["gender"] != 0, "gender"] = 1
    df.drop('is_fired', axis=1, inplace=True)
    df['salary'] = df['salary'] / 100

    features_hot = ['speciality', 'absenceReason', 'season', 'education']

    df_dummies = pd.get_dummies(df, columns=features_hot, prefix=features_hot, sparse=False, drop_first=True)

    to_add_columns = list(set(all_possible_features) - set(df_dummies.columns))

    to_add_df = pd.DataFrame([])
    for i in to_add_columns:
        to_add_df[i] = pd.Series([0] * df.shape[0])

    to_add_df.index = df.index

    df_to_feed = pd.concat([df, to_add_df], axis=1)

    df_to_feed.drop(features_hot, axis=1, inplace=True)

    df_to_feed.drop(dates_features, axis=1, inplace=True)

    return df_to_feed


def train(employees):

    df = pd.DataFrame([vars(employee) for employee in employees])
    df.index = df.id
    df.drop("id", axis=1, inplace=True)

    df = preprocess(df)
    print(df)

    X = df.drop("workingPeriod", axis=1)
    y = df.pop("workingPeriod")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.23, random_state=1)

    model = RandomForestRegressor(min_samples_split=6, random_state=1)
    model.fit(X_train, y_train)
    print(model.predict(X_train))

    dump(model, "model.joblib")


if __name__ == "__main__":
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
                             mentored=False

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
                              mentored=True

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
                              mentored=False

                              )





    employees = [instance, instance2, instance3]
    train(employees)