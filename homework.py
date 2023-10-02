from dataclasses import dataclass, asdict
from typing import List, Type, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    PATTERN_MESSAGE = ('Тип тренировки: {training_type}; '
                       'Длительность: {duration:.3f} ч.; '
                       'Дистанция: {distance:.3f} км; '
                       'Ср. скорость: {speed:.3f} км/ч; '
                       'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить сообщение с данными о тренировке."""
        return self.PATTERN_MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Не используеться для class ' + type(self).__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                  * self.get_mean_speed()
                                  + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight / self.M_IN_KM
                                 * (self.duration * self.MIN_IN_H))
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_MULTIPLIER = 0.029
    KMPH_IN_MPSEC = round(1000 / 3600, 3)
    CM_IN_M = 100

    height: int

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        spent_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                                  + (((self.get_mean_speed()
                                     * self.KMPH_IN_MPSEC)**2)
                                     / (self.height / self.CM_IN_M))
                                  * self.CALORIES_SPEED_MULTIPLIER
                                  * self.weight)
                                 * self.duration * self.MIN_IN_H)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 1.1
    CALORIES_DURATION_MULTIPLIER = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плаванье."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плаванье."""
        spent_calories: float = ((self.get_mean_speed()
                                  + self.CALORIES_WEIGHT_MULTIPLIER)
                                 * self.CALORIES_DURATION_MULTIPLIER
                                 * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str,
                 data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_traing_dict: dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    return type_traing_dict.get(workout_type)(*data)


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
