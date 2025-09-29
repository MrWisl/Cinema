
from datetime import datetime


class Films:
    def __init__(self, name=None, tseans=None, time=None, price=None):
        super().__init__()
        self.name = name
        self.tseans = tseans
        self.time = time
        self.price = price

    def film_info(self):
        print('Название: {}'.format(self.name),
              'Время сеанса {}'.format(self.tseans),
              'Длинна фильма {}'.format(self.time),
              'Цена: {}'.format(self.price), sep='\n')


class Hall(Films):

    def __init__(self, place=None):
        super().__init__()
        self.PLACES = place
        self.FILM = None
        self.free_place = len(self.PLACES[0]) * len(self.PLACES)
        self.busy_place = 0

    def show_place(self):
        for row in self.PLACES:
            print(row)

    def append_place(self):
        for row in self.PLACES:
            print(row)
        while True:
            try:
                row, col = map(int, input('Укажите номер ряда и номер кресла через пробел >>>').split())
            except ValueError:
                print('Введите цифрами')
                continue
            try:
                self.PLACES[row - 1][col - 1]
            except IndexError:
                print('Ряда или кресла не сущетсвует')
                continue
            if self.PLACES[row - 1][col - 1] == '':
                self.PLACES[row - 1][col - 1] = 'З'
            else:
                print('Место занято')
            break
        self.free_place -= 1
        self.busy_place += 1
        for row in self.PLACES:
            print(row)

    def create_seans(self):
        name = input('Введите название фильма >>>')
        if self.FILM is not None:
            if self.FILM.name == name:
                print('Cеанс этого фильма уже назначен')
                return None
            print('В зале уже назначен сеанc')
            solution = input('Желаете заменить? (Да/Нет) >>>').strip().lower()
            while True:
                if solution == 'нет':
                    return None
                elif solution == 'да':
                    break
                else:
                    print('такого ответа нет, повторите попытку')
                    continue

        while True:
            try:
                tseans = datetime.strptime(input('Ввведите время сеанса hh:mm >>>'), '%H:%M')
            except ValueError:
                print('Неправильный формат Даты повторите попытку')
                continue
            break
        while True:
            try:
                time = int(input('Введите длительность фильма в минутах >>>'))
            except ValueError:
                print('Ошибка: Введите цифрами')
                continue
            break
        while True:
            try:
                price = int(input('Введите цену фильма >>>'))
            except ValueError:
                print('Ошибка: Введите цифрами')
                continue
            break
        self.FILM = Films(name, tseans, time, price)
        return name


class Cinemas:
    def __init__(self):
        self.HALLS = {}

    def append_hall(self):
        while True:
            name = input('Введите название зала >>>').strip()
            if name in self.HALLS.keys():
                print('Зал с таким именем уже существует измените его')
                continue
            break
        while True:
            try:
                count_row, count_col = list(map(int,
                                                input('Введите кол-во рядов и кресел в зале через пробел >>>').split()))
            except ValueError:
                print('введите числами')
                continue
            break
        place = [['' for _ in range(count_col)] for _ in range(count_row)]
        self.HALLS[name] = Hall(place)


class Programs(Cinemas):

    def __init__(self):
        super().__init__()
        self.CINEMAS = {}
        self.have_films = {}

    def __del__(self):
        print('Деятельность билетной программы завершина')

    def append_cinemas(self):
        name = input('введите название кинотеатра >>>').strip()
        if name in self.CINEMAS.keys():
            print('Такой кинотеатр уже есть')
        self.CINEMAS[name] = Cinemas()
        self.CINEMAS[name].append_hall()

    def cinemas_info(self):
        if self.CINEMAS == {}:
            print('Кинотеатров не существует')
            return
        print('Доступные кинотеатры:',
              ' ,'.join([cinema for cinema in self.CINEMAS.keys()]))
        name_cinemas = input('Введите название кинотеатра о котором нужна информация>>>')
        if name_cinemas not in self.CINEMAS.keys():
            print('Кинотеатра не сущесвует')
            return
        halls = self.CINEMAS[name_cinemas].HALLS
        print('Доступные залы:',
              ' ,'.join([hall for hall in halls.keys()]))
        name_halls = input('Введите имя зала в 1 слово >>>').strip()
        if name_halls not in halls.keys():
            print('Зала не существует')
            return
        hall = halls[name_halls]
        hall.show_place()
        print(f'В зале {hall.free_place} свободных мест')
        print(f'В зале {hall.busy_place} занятых мест')
        if hall.FILM:
            print('В данный момент назначен сеанс фильма - {}'.format(hall.FILM.name))
            print('Информация о фильме:')
            hall.FILM.film_info()

    def append_film(self):
        cinem = self.CINEMAS
        if cinem == {}:
            print('Кинотеатров не существует')
            return
        print('Доступные кинотеатры:',
              ', '.join([cinemas for cinemas in cinem.keys()]))
        name = input('Введите название кинотеатра >>>')
        if name not in cinem.keys():
            print('Такого кинотеатра нет')
            return
        if not cinem[name].HALLS:
            print('В кинотеатре не существует залов')
            return
        hall = cinem[name].HALLS
        print('Доступные залы:')
        print(', '.join([hall for hall in hall.keys()]))
        name_hall = input('Введите номер зала >>>')
        if name_hall not in hall.keys():
            print('Этого зала не существует')
            return
        film_name = hall[name_hall].create_seans()
        if not film_name:
            print('Операция была отмененна')
            return
        if name not in self.have_films.keys():
            self.have_films[name] = [(film_name, name_hall)]
            return
        self.have_films[name] = [(film_name, name_hall)
                                 if hall == name_hall
                                 else (film, hall)
                                 for film, hall in self.have_films[name]
                                 ]
        self.have_films[name].append((film_name, name_hall))

    def next_session(self):
        if self.CINEMAS == {}:
            print('Кинотеатров не существует')
            return
        best_session = None
        path = []
        film_name = input('Введите название фильма >>>')
        for name, cinemas in self.CINEMAS.items():
            for nameh, hall in cinemas.HALLS.items():
                if not hall.FILM or hall.FILM.name != film_name:
                    continue
                if best_session is None or (best_session > hall.FILM.tseans and hall.free_place != 0):
                    path = []
                    best_session = hall.FILM.tseans
                    path.extend([name, nameh, best_session])
        if path:
            print(f'Ближайший сеанс на фильм {film_name} cостоится в кинотеатре {path[0]}.',
                  f'В зале {path[1]} в {path[2]}.')
        else:
            print('Сеанса на данный фильм не существует :) Ждите премьеры.')

    def buy_billets(self):
        if self.have_films == {}:
            print('В данный моменет сеансов нет')
            return
        else:
            print('\n'.join(
                 [f'В кинотеатре {cinema} проходят сеансы:'
                  f'В зале {seans[1]} проходит фильм {seans[0]} стоимостью {self.CINEMAS[cinema].HALLS[seans[1]].price}'
                  if self.CINEMAS[cinema].HALLS[seans[1]].free_place != 0
                  else f'в кинотеатре {cinema} в зале {seans[1]} мест нет'
                  for cinema in self.have_films.keys()
                  for seans in self.have_films[cinema]]),
                end='\n')
        name = input('Введите имя кинотеатра >>>')
        if name not in self.have_films.keys():
            print('такого кинотеатра не существует или в нем не идет показ')
            return
        cinem = self.CINEMAS[name]
        hall = cinem.HALLS
        print('Залы:', ', '.join([h for h in hall.keys()]))
        nameh = input('Введите имя зала >>>')
        if nameh not in hall.keys():
            print('Такого зала не существует')
            return
        if not hall[nameh].FILM:
            print('В данном зале не проводится сеанс')
            return
        if hall[nameh].free_place == 0:
            print('В этом зале нет свободных мест')
            return
        print(f'Cтоимость фильма {hall[nameh].FILM.price} рублей')
        while True:
            sol = input('Преобрести билет? (Да\Нет) >>>').strip().lower()
            if sol == 'да':
                hall[nameh].append_place()
                print('Спасибо за покупку')
                return
            elif sol == 'нет':
                print('произошла отмена')
                return
            else:
                print('Неправильный ввод ответа повторите попытку')
                continue

    def add_hall(self):
        if self.CINEMAS == {}:
            print('Кинотеатров не существует')
            return
        print('Доступные кинотеатры:',
              ', '.join([cinemas for cinemas in self.CINEMAS.keys()]))
        cin_name = input('Введите название кинотеатра >>>')
        if cin_name not in self.CINEMAS.keys():
            print('Такого кинотеатра не существует')
            return
        self.CINEMAS[cin_name].append_hall()

    @staticmethod
    def help():
        commands = {
            'help': 'Выводит меню помощи',
            'add_cinema': 'Добавляет кинотеатр и зал в него',
            'add_hall': 'Добавляет зал в определенный кинотеатр',
            'add_film': 'Добавляет фильм в зал определнного кинотеатра',
            'n_session': 'Показывает в каком кинотеатре и вкаком зале будет ближайший показ',
            'info': 'Выводит информацию об кинотеатре и его зале',
            'buy': 'Забронировать место',
            'end': 'Завершение программы'
        }
        for comm, disc in commands.items():
            print(f'{comm}: {disc}')



pg = Programs()
print('Для получения информации о командах введите help')
while True:
    com = input('Введите комнаду >>>').strip()
    if com == 'help':
        pg.help()
    elif com == 'add_cinema':
        pg.append_cinemas()
    elif com == 'add_film':
        pg.append_film()
    elif com == 'n_session':
        pg.next_session()
    elif com == 'info':
        pg.cinemas_info()
    elif com == 'buy':
        pg.buy_billets()
    elif com == 'add_hall':
        pg.add_hall()
    elif com == 'end':
        break
