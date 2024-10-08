class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
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
    # Расстояние, которое спортсмен преодолевает за один шаг или гребок
    LEN_STEP: float = 0.65
    # сколько метров в 1 км
    M_IN_KM = 1000
    # сколько минут в часе
    MINUTES_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.duration_minutes = duration * self.MINUTES_IN_HOUR
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    # константы для расчета потраченных калорий при беге
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration_minutes
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # константы для расчета потраченных калорий при ходьбе
    CALORIES_MEAN_WALK_MULTIPLIER1 = 0.035
    CALORIES_MEAN_WALK_MULTIPLIER2 = 0.029
    KM_H_M_SEC = 0.278
    SM_IN_M = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65
        self.height = height
        self.height_m = height / self.SM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.CALORIES_MEAN_WALK_MULTIPLIER1 * self.weight
             + ((self.KM_H_M_SEC * self.get_mean_speed())**2 / self.height_m)
             * self.CALORIES_MEAN_WALK_MULTIPLIER2 * self.weight)
            * self.duration_minutes
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    # константы для расчета потраченных калорий при беге

    CALORIES_MEAN_SWIM_MULTIPLIER = 2
    CALORIES_MEAN_SWIM_SHIFT = 1.1
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        mean_speed = ((self.length_pool * self.count_pool / self.M_IN_KM)
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.get_mean_speed()
             + self.CALORIES_MEAN_SWIM_SHIFT)
            * self.CALORIES_MEAN_SWIM_MULTIPLIER * self.weight * self.duration
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    if workout_type in training_codes:
        return training_codes[workout_type](*data)


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
