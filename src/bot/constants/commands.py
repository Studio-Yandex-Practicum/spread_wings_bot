# Команда должна обязательно писаться с маленькой буквы
# Если написать команду /Start будет возникать ошибка Bot_command_invalid
# Это особенность телеграма

COMMANDS = [
    ("/start", "Запустить/перезапустить бота"),
    ("/help", "Показать, что умеет бот"),
    ("/upmenu", "Обновить список команд и меню"),
]
