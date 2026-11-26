# Blackjack AI turnīra noteikumi un specifikācija

Spēlē piedalās vairāki boti pie viena galda pret Dīleri (ko vada pasniedzējs/students), kas testē visus botus.
Visi boti spēlē ar vienu kopīgu 4 kāršu kavu komplektu(208 kārtis), kas tiek pārmaisīta, kad izspēlēti ~75% kāršu.

## 1. Faila novietojums un struktūra
* Katrs dalībnieks izveido savu mapi: `blackjack/<vards_uzvards>/bot.py` (piem., `blackjack/janis_berzins/bot.py`).
* Failā **nedrīkst** izmantot `input()`, `print()` garus žurnālus vai ārējas bibliotēkas (tikai Python standarta bibliotēka: `random`, `time`, `math`, `collections` u.c.).
* Importējot `bot.py`, nedrīkst palaisties nekāds aprēķinu kods — visu testēšanu liec zem `if __name__ == "__main__":`.

## 2. Kāršu formāts
Katra kārts ir 2–3 simbolu virkne (`str`), piemēram: `"AS"`, `"10H"`, `"KD"`, `"2C"`:
* **Vērtība (`card[:-1]`):** `"2"`, `"3"`, `"4"`, `"5"`, `"6"`, `"7"`, `"8"`, `"9"`, `"10"`, `"J"`, `"Q"`, `"K"`, `"A"`.
* **Masts (`card[-1]`):** `"H"` (ērcens), `"D"` (kāravs), `"C"` (kreics), `"S"` (pīķis).
* **Punkti:** `2–10` atbilst nominālam; `J, Q, K` = `10` punkti; `A` (dūzis) = `11` vai `1` punkts.

## 3. Obligātie elementi failā `bot.py`

### `BOT_NAME: str`
Tavs bota nosaukums tabulai (bez garumzīmēm, lai korekti attēlojas konsolē), piemēram:
```python
BOT_NAME = "MonteCarloBot"
