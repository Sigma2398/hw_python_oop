from typing import Dict, Type
from dataclasses import dataclass


# Коммент для ревьюера: Что то запутался чуть чуть, пока что исправлял.
# Скорее всего наделал новые ошибки и не исправил некоторые старые.
# Голова кругом пошла, пока что исправлял


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60
    LEN_STEP: float = 0.65
    FLIPPER_LENGTH: float = 1.38

    name: str
    action: int
    duration: float
    weight: float
    weight: float

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        # без объявления name тесты не проходят
        self.name = self.__class__.__name__
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise KeyError(f'Метод не переопределен для класса')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # А можно лучше оставить так как есть?
        # В данном случае понятнее, по моему, так.
        message = InfoMessage(
            self.name,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    RUN_RATE1: int = 18
    RUN_RATE2: int = 20

    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num1: float
        num2: float
        num1 = self.RUN_RATE1 * self.get_mean_speed() - self.RUN_RATE2
        num2 = self.weight * self.duration * self.MINUTES_IN_HOUR
        spent_calories = num1 * num2 / self.M_IN_KM
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WLK_RATE1: float = 0.035
    WLK_RATE2: float = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num1: float
        num2: float
        num3: float
        num1 = self.WLK_RATE1 * self.weight
        num2 = self.WLK_RATE2 * self.weight
        num3 = self.get_mean_speed() ** 2 // self.height
        sumnum = (num1 + num2 * num3)
        spent_calories = sumnum * self.duration * self.MINUTES_IN_HOUR
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_RATE1: float = 1.1
    SWM_RATE2: int = 2

    name: str
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.name = self.__class__.__name__
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        num1: float
        num1 = self.length_pool * self.count_pool
        mean_speed = num1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num2: float
        num2 = self.get_mean_speed() + self.SWM_RATE1
        spent_calories = num2 * self.SWM_RATE2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sports: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    try:
        return sports[workout_type](*data)
    except Exception:
        raise KeyError(f'{workout_type} - неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
