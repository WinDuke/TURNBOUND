# TURNBOUND

## Python ASCII Turn-Based Survival Roguelike

**TURNBOUND** — это стильный пошаговый ASCII roguelike с элементами выживания, созданный на Python с использованием Textual + Rich.

### Особенности игры

* 🎮 **Тактический пошаговый бой** — каждое действие имеет значение
* 🌊 **Волны врагов** — прогрессирующая сложность с боссами каждые 5 волн
* ⚔️ **4 уникальных персонажа** — Executioner, Astromancer, Plague Saint, Mirror Duelist
* 🎯 **Глубокая система билдов** — 33+ улучшений с синергиями
* 👹 **3 эпических босса** — The Hollow King, The Bell Saint, Choir of Teeth
* 🗺️ **Процедурные арены** — 4 биома с уникальной атмосферой
* ✨ **Rich ASCII графика** — цвета, анимации, эффекты в терминале

---

## Установка

```bash
cd turnbound
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

---

## Управление

| Клавиша | Действие |
|---------|----------|
| ↑↓←→ | Перемещение |
| Q, W, E, R | Навыки |
| SPACE | Пропуск хода |
| ESC | Пауза |

---

## Персонажи

### The Executioner
Брутальный боец, использующий кровь как ресурс. Чем меньше HP, тем сильнее урон.

**Навыки:**
- **Q — Cleave**: Широкая атака по области
- **W — Chain Hook**: Притягивает врага
- **E — Blood Surge**: Тратит HP для мощного урона
- **R — Execution**: Мгновенное убийство ниже 30% HP

### The Astromancer
Мастер пространства и времени. Навыки могут повторяться как эхо.

**Навыки:**
- **Q — Star Bolt**: Пронзающий снаряд
- **W — Warp Step**: Телепортация
- **E — Echo Seal**: Повтор предыдущего навыка
- **R — Collapse**: Активация всех эхо-эффектов

### The Plague Saint
Распространяет заражение по арене. Враги умирают от собственных болезней.

**Навыки:**
- **Q — Rot Touch**: Ядовитая атака
- **W — Spore Cloud**: Облако инфекции
- **E — Harvest**: Взрыв заражённых врагов
- **R — Bloom**: Массовая мутация

### The Mirror Duelist
Мастер контратак и предсказания. Идеальное время для удара.

**Навыки:**
- **Q — Feint**: Гарантированный крит
- **W — Mirror Step**: Рывок с иллюзией
- **E — Riposte**: Контр-стойка
- **R — Perfect Reflection**: Отражение навыка

---

## Система боя

### Формула урона
```
FinalDamage = (BaseDamage + Power) × CritMultiplier - Defense
```

### Типы урона
- **Physical** — обычные атаки
- **Fire** — горение и взрывы
- **Frost** — замедление и заморозка
- **Lightning** — цепная молния
- **Void** — игнорирование защиты
- **Poison** — урон со временем
- **Blood** — механики жертвы

### Статус-эффекты
- **Burn** — урон каждый ход
- **Poison** — стакающийся DOT
- **Shock** — увеличивает следующий урон
- **Freeze** — пропускает ходы
- **Bleed** — урон при движении
- **Vulnerable** — повышенный урон
- **Weakness** — сниженный урон

### Взаимодействия статусов
- **Shock + урон** = бонусный урон
- **Freeze + сильный удар** = shatter (доп. урон)
- **Burn + Poison** = взрывная комбинация

---

## Враги

### Типы врагов
- **Swarmers** (Zombie, Rat, Skeleton) — окружают числом
- **Hunters** (Spitter, Archer) — держат дистанцию
- **Tanks** (Knight, Golem) — блокируют движение
- **Casters** (Necromancer, Cultist) — контролируют зону
- **Support** (Priest, Shaman) — усиливают союзников

### Elite модификаторы
- **Aggressive** — приоритет атаки
- **Tactical** — умное позиционирование
- **Frenzied** — игнорирует защиту
- **Coward** — отступает при низком HP

---

## Боссы

### The Hollow King
Падший монарх, поглощённый тьмой.

**Фазы:**
1. **Duelist** — агрессивные точные удары
2. **Mirror Clones** — создаёт копии
3. **Darkness Arena** — арена во тьме

### The Bell Saint
Искажённый святой, чей колокол отсчитывает смерть.

**Механика:** Каждые 4 хода звонит колокол, меняя эффект:
1. Haste — босс атакует дважды
2. Curse Field — слабость всем
3. Silence — блокировка навыков
4. Judgment — массовый урон

### Choir of Teeth
Сама арена становится живым кошмаром.

**Механики:**
- Движущиеся стены
- Смещающиеся безопасные зоны
- Environmental hazards

---

## Система улучшений

### Редкость
- **Common** — простые модификаторы (+HP, +Defense)
- **Rare** — изменение механик (Dash ignites tiles)
- **Epic** — определяющие билд (Chain Lightning)
- **Legendary** — ломающие игру (Echo Cascade, Phoenix Engine)

### Примеры легендарных улучшений
- **Phoenix Engine** — огненные взрывы создают firestorms
- **Echo Cascade** — повторённые заклинания повторяются снова
- **Crimson Reactor** — получение урона восстанавливает энергию
- **Glass Momentum** — каждый dodge увеличивает crit damage

---

## Архитектура

### ECS-Lite
- **Entities** — integer IDs
- **Components** — только данные (Position, Health, Stats, etc.)
- **Systems** — логика (Combat, Movement, AI, Wave)

### Event Bus
События: `on_hit`, `on_crit`, `on_kill`, `on_wave_complete`, `on_boss_phase_change`

### Utility AI
Враги динамически оценивают действия:
```
Attack Score = 80
Retreat Score = 60
Use Skill Score = 90
Move Score = 40
```

---

## Запуск тестов

```bash
pytest tests/ -v
```

### Покрытие тестами
- ✅ Боевая система (9 тестов)
- ✅ Контент: персонажи, враги, улучшения (14 тестов)
- ✅ Босс-система (10 тестов)

**Всего: 33 теста**

---

## Структура проекта

```
turnbound/
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
├── README.md              # Документация
├── src/
│   ├── core/              # Ядро: game loop, event bus
│   ├── ecs/               # Entity-Component-System
│   ├── components/        # Компоненты сущностей
│   ├── systems/           # Игровые системы
│   ├── render/            # Рендеринг ASCII
│   ├── generation/        # Генерация арен
│   ├── content/           # Контент: персонажи, враги, боссы, улучшения
│   └── ui/                # Интерфейсы
└── tests/                 # Автотесты
```

---

## Требования

- Python 3.12+
- textual
- rich
- pytest (для тестов)

---

## Roadmap MVP

- [x] Phase 1 — Engine Core (ECS, render, input)
- [x] Phase 2 — Combat (damage, skills, statuses)
- [x] Phase 3 — AI (utility AI, pathfinding)
- [x] Phase 4 — Content (4 chars, 10 enemies, 3 bosses)
- [x] Phase 5 — Build System (upgrades, tag synergies)
- [ ] Phase 6 — Polish (animations, VFX, balancing)

---

## Лицензия

MIT License
