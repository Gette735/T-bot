C:\PycharmProjects\PythonProject\T-bot
├── t_bot/                     # Корневая директория проекта
│   ├── handlers/              # Директория с хэндлерами (функции бота)
│   │   ├── __init__.py        # Инициализация пакета handlers
│   │   ├── resume_bot.py      # Бот для составления резюме
│   │   ├── ai_translator.py   # Перевод с использованием GPT
│   │   ├── chat_gpt.py        # Общениес с ChatGPT
│   │   ├── quiz.py            # Викторины и вопросы
│   │   ├── random.py          # Генерация случайных данных
│   │   ├── talking.py         # Диалоги с историческими личностями
│   │   ├── menu.py            # Основное меню бота
│   │   └── talk.py            # Диалоги с GPT
│   ├── keyboards/             # Модули для работы с клавиатурами
│   │   ├── __init__.py        # Инициализация пакета keyboards
│   │   ├── keybords.py        # Модуль для Reply-клавиатур
│   │   ├── base.py            # Базовый класс для создания динамических инлайн-клавиатур
│   │   └── factories.py       # Фабрики для обработки коллбэков
│   └── utils/                 # Вспомогательные утилиты
│       ├── __init__.py        # Инициализация пакета utils
│       ├── the_state_machine.py  # Стэйт-машина (контроль состояний бота)
│       ├── config.py          # Работа с переменными окружения и конфигурацией
│       └── gpt_service.py     # Логика работы с GPT (API, запросы, обработка ответов)
├── main.py                    # Главный файл (точка входа в приложение)
└── __init__.py                # Инициализация корневого пакета

Command list:
- random - give you a random fact
- quiz - an ai-supported quiz with different topics
- translate - translate  any world or sentence to Eng/Span
- talk - talking with historical person
- resume - bot is helping you to create your resume
- gpt - talking with ChatGPT
