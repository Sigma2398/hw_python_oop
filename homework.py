""" Константные переменные, которые пригодятся далее """
MILLI: int = 1000
MINUT_60: int = 60
STEP_LENGTH: float = 0.65
FLIPPER_LENGTH: float = 1.38


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    name: str
    action: int
    duration: float
    weight: float
    weight: float
    M_IN_KM: int = MILLI
    LEN_STEP: float = STEP_LENGTH

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        self.name = 'Training'
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = MILLI
        self.LEN_STEP = STEP_LENGTH

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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = 0.0
        return spent_calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
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

    name: str
    action: int
    duration: float
    weight: float

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.name = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num1: float
        num2: float
        num1 = self.RUN_RATE1 * self.get_mean_speed() - self.RUN_RATE2
        num2 = self.weight * self.duration * MINUT_60
        spent_calories = num1 * num2 / self.M_IN_KM
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WLK_RATE1: float = 0.035
    WLK_RATE2: float = 0.029

    name: str
    action: int
    duration: float
    weight: float
    height: float

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.name = 'SportsWalking'
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
        spent_calories = (num1 + num2 * num3) * self.duration * MINUT_60
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_RATE1: float = 1.1
    SWM_RATE2: int = 2

    name: str
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int
    LEN_STEP: float = FLIPPER_LENGTH

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.name = 'Swimming'
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = FLIPPER_LENGTH

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
    sports = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    for sport in sports:
        try:
            if sport == workout_type:
                training = sports[sport](*data)
                return training
        except ValueError:
            raise ValueError('Неизвестный вид тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
