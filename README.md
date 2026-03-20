# horoscope-bot

A bot with daily horoscopes for different zodiac signs.

## Used tech

- aiogram
- apscheduler
- beautifulsoup4 for parsing 
- Redis as database
- Docker with docker-compose for deployment

## Commands

- /start - launch a bot
- /horoscope - horoscope for today
- /compatibility - compatibility of zodiac signs
- /subscribe - subscribe to the horoscope

## Easy start

Clone the repository:
```bash
git clone https://github.com/tauriene/horoscope-bot.git
```
---
Go to your project folder:
```bash
cd horoscope-bot
```
---
Run in terminal
```bash
docker-compose up --build
```