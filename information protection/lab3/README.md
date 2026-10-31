# Лабораторная работа № 3
## Средства безопасности операционной системы Linux (Ubuntu 24.04 LTS)

---

## 1. Цель работы

Изучить встроенные средства обеспечения безопасности Ubuntu 24.04 LTS, получить практические навыки настройки прав доступа, брандмауэра, аудита, мандатного контроля и защиты удалённого доступа по SSH.

---

## 2. Общие сведения

Ubuntu 24.04 LTS использует многоуровневую защиту: AppArmor для мандатного контроля доступа, UFW для управления брандмауэром, auditd для аудита событий, автоматические обновления безопасности, систему hardening-профилей CIS. Удалённый доступ по SSH защищается ключевой аутентификацией, отключением root-входа и настройками `sshd_config`.

---

## 3. Задание 1. Управление пользователями и правами

1. Создать двух пользователей: `student` и `auditor`:
   ```bash
   sudo adduser student
   sudo adduser auditor
   ```

2. Создать группу `security` и добавить в неё `auditor`:
   ```bash
   sudo groupadd security
   sudo usermod -aG security auditor
   ```

3. Изучить права доступа к файлам: создать файл, изменить его владельца и права:
   ```bash
   touch /tmp/testfile
   sudo chown student:security /tmp/testfile
   sudo chmod 640 /tmp/testfile
   ls -la /tmp/testfile
   ```

4. Сменить пароль пользователю `student`:
   ```bash
   sudo passwd student
   ```

5. Изучить команды `umask`, `chattr`, `lsattr`.

6. Изучить историю команд: `history`, увеличить размер истории через `HISTSIZE` в `~/.bashrc`.

---

## 4. Задание 2. Настройка UFW (брандмауэр)

1. Проверить статус UFW: `sudo ufw status verbose`.

2. Включить UFW с политикой «запретить всё входящее»:
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw enable
   ```

3. Разрешить SSH: `sudo ufw allow 22/tcp`.

4. Проверить правила: `sudo ufw status numbered`.

5. Попытаться подключиться к запрещённому порту (например, 80) с другой машины — убедиться, что соединение блокируется.

---

## 5. Задание 3. Аудит системы с auditd

1. Установить и запустить `auditd`:
   ```bash
   sudo apt install auditd audispd-plugins
   sudo systemctl enable --now auditd
   ```

2. Добавить правило для отслеживания изменений в файле `/etc/passwd`:
   ```bash
   sudo auditctl -w /etc/passwd -p wa -k passwd_changes
   ```

3. Выполнить действие — добавить пользователя: `sudo adduser testuser`.

4. Просмотреть события аудита:
   ```bash
   sudo ausearch -k passwd_changes
   ```

5. Настроить постоянные правила в `/etc/audit/rules.d/audit.rules`.

6. Добавить правило для отслеживания выполнения команд sudo:
   ```bash
   sudo auditctl -w /usr/bin/sudo -p x -k sudo_usage
   ```

---

## 6. Задание 4. AppArmor и мандатный контроль доступа

1. Проверить статус AppArmor: `sudo aa-status`.

2. Просмотреть список профилей: `ls /etc/apparmor.d/`.

3. Создать простой профиль для тестового приложения (например, `/usr/bin/testapp`) в режиме «жалобы» (complain):
   ```bash
   sudo aa-complain /usr/bin/testapp
   ```

4. Проверить логи AppArmor: `sudo dmesg | grep apparmor`.

5. Перевести профиль в режим «принуждения» (enforce):
   ```bash
   sudo aa-enforce /usr/bin/testapp
   ```

6. Убедиться, что приложение работает с ограничениями.

---

## 7. Задание 5. Автоматические обновления безопасности

1. Проверить статус `unattended-upgrades`:
   ```bash
   sudo systemctl status unattended-upgrades
   ```

2. Проверить конфигурацию: `cat /etc/apt/apt.conf.d/50unattended-upgrades`.

3. Убедиться, что автоматические обновления безопасности включены (по умолчанию в Ubuntu 24.04).

4. Выполнить ручное обновление: `sudo apt update && sudo apt upgrade`.

---

## 8. Задание 6. Защита удалённого доступа (SSH)

### 8.1 Настройка SSH-сервера

1. Установить OpenSSH-сервер (если не установлен):
   ```bash
   sudo apt install openssh-server
   sudo systemctl enable --now ssh
   ```

2. Проверить статус: `sudo systemctl status ssh`.

3. Открыть конфигурационный файл:
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```

4. Настроить следующие параметры:
   - `PermitRootLogin no` — запретить вход под root;
   - `PasswordAuthentication no` — отключить вход по паролю;
   - `PubkeyAuthentication yes` — разрешить вход по ключу;
   - `Port 2222` — изменить стандартный порт (опционально);
   - `MaxAuthTries 3` — ограничить число попыток аутентификации;
   - `LoginGraceTime 30` — ограничить время на ввод пароля;
   - `AllowUsers student auditor` — разрешить вход только указанным пользователям.

5. Перезапустить SSH: `sudo systemctl restart ssh`.

### 8.2 Настройка ключевой аутентификации

1. На клиентской машине сгенерировать пару ключей:
   ```bash
   ssh-keygen -t ed25519 -C "student@lab"
   ```

2. Скопировать публичный ключ на сервер:
   ```bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub student@<IP-сервера>
   ```

3. Проверить вход по ключу:
   ```bash
   ssh student@<IP-сервера>
   ```

4. Убедиться, что вход по паролю больше не работает.

### 8.3 Проверка защиты SSH

1. Попытаться войти под root — убедиться, что вход запрещён.

2. Попытаться войти по паролю — убедиться, что аутентификация отклоняется.

3. Попытаться войти с неверным ключом — убедиться, что соединение разрывается.

4. Проверить журнал SSH: `sudo journalctl -u ssh`.

5. Найти события неудачных попыток входа и успешной аутентификации по ключу.

6. Установить `fail2ban` для автоматической блокировки подозрительных IP:
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable --now fail2ban
   ```

---

## 9. Контрольные вопросы

1. Как работает AppArmor в Ubuntu? Чем отличается от SELinux?
2. Для чего используется auditd? Приведите пример правила.
3. Как настроить автоматические обновления безопасности в Ubuntu?
4. Почему рекомендуется отключать вход root по SSH?
5. В чём преимущество ключевой аутентификации перед парольной?
6. Что такое fail2ban и как он защищает SSH?
7. Как проверить, что UFW блокирует входящие соединения на запрещённые порты?
8. Какие параметры `sshd_config` отвечают за ограничение числа попыток входа?

---

## 10. Форма отчётности

Отчёт объёмом не более 5 страниц. Включить:

- скриншоты ключевых этапов (настройка UFW, auditd, AppArmor, SSH);
- таблицу с настройками безопасности и найденными событиями;
- вывод по работе: какие средства защиты Linux являются наиболее эффективными, какие ограничения у встроенных механизмов.

---

## Список литературы

1. Ubuntu Documentation. «Security features overview». https://documentation.ubuntu.com/security/
2. Ubuntu Blog. «Hardening automation for CIS benchmarks now available for Ubuntu 24.04 LTS». https://ubuntu.com/blog/
3. Ubuntu Documentation. «OpenSSH server». https://documentation.ubuntu.com/server/how-to/security/openssh-server/
4. Ubuntu Documentation. «AppArmor». https://documentation.ubuntu.com/
5. Ubuntu Documentation. «Firewall». https://documentation.ubuntu.com/server/how-to/security/firewalls/
