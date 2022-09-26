from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> None:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длина шага при хотьбе или беге
    M_IN_KM: float = 1000  # переводной коэффициент из метр в км
    H_IN_MIN = 60  # переводной коэффициент часы в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (ккал)."""
        raise NotImplementedError('Smth wrong with get_spent_calories() metod')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CAL_1: float = 18
    COEFF_CAL_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (ккал) при беге."""

        return ((self.COEFF_CAL_1 * self.get_mean_speed()
                - self.COEFF_CAL_2) * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (ккал) при спорт. ходьбе."""

        return ((self.COEFF_CAL_1 * self.weight + (self.get_mean_speed()**2
                // self.height) * self.COEFF_CAL_2 * self.weight)
                * (self.duration * self.H_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Длина гребка
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании в км/ч."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (ккал) при плавании."""

        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_dictionary: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in train_dictionary:
        return train_dictionary[workout_type](*data)
    else:
        raise NotImplementedError('Unknown training')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
