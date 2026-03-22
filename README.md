# STRIPS – Blocks World

## Autorzy

| | Autor 1 | Autor 2 |
|---|---------|---------|
| **Imię i nazwisko** | Karol Bystrek | Patryk Chamera |
| **E-mail** | karbystrek@student.agh.edu.pl | pchamera@student.agh.edu.pl |

---

## 1. Opis zadania i wybrany wariant

### Czym jest STRIPS?

**STRIPS** (Stanford Research Institute Problem Solver) to klasyczny formalizm do opisu problemów planowania w sztucznej inteligencji. W STRIPS świat opisujemy za pomocą:

- **Stanów** – zbiory faktów (cech i ich wartości) opisujących aktualną sytuację,
- **Akcji** – operacje zmieniające stan świata, zdefiniowane przez:
  - *Warunki wstępne (preconditions)* – co musi być spełnione, aby akcja mogła zostać wykonana,
  - *Efekty (effects)* – jakie zmiany w stanie świata wprowadza akcja.

### Blocks World – świat klocków

Wybraną dziedziną jest **Blocks World** – jeden z najbardziej znanych benchmarków w planowaniu AI.

**Zasady:**

- Na stole leżą klocki, które mogą być ułożone w stosy (wieże).
- Klocek może leżeć na stole lub na dokładnie jednym innym klocku.
- Na każdym klocku może leżeć co najwyżej jeden inny klocek.
- Klocek jest **wolny (clear)**, jeśli nic na nim nie leży.
- Przenieść można **tylko klocek wolny** – na stół (zawsze) lub na inny wolny klocek.
- Jedyną akcją jest `move_X_from_Y_to_Z` – przeniesienie klocka X z pozycji Y na pozycję Z.

**Reprezentacja stanu** składa się z dwóch typów cech dla każdego klocka `X`:

| Cecha | Opis | Przykład |
|-------|------|----------|
| `X_is_on` | Na czym leży klocek X | `a_is_on = b` (a leży na b) |
| `clear_X` | Czy klocek X jest wolny | `clear_a = True` (nic nie leży na a) |

---

## 2. Implementacja

### Użyte biblioteki

| Biblioteka | Rola |
|-----------|------|
| **AIPython** (`aipython/`) | Gotowy framework AI – dostarcza formalizm STRIPS, Forward Planner i algorytm A* |
| **Python 3** (stdlib) | `threading` (timeout), `time`, `datetime`, `os` |

### Struktura projektu

```
lab2/
├── aipython/                        # Biblioteka AIPython (gotowa, nie modyfikowana)
│   ├── stripsProblem.py             #   Strips, STRIPS_domain, Planning_problem, create_blocks_world()
│   ├── stripsForwardPlanner.py      #   Forward_STRIPS – forward planner
│   ├── searchMPP.py                 #   SearcherMPP – A* z Multiple-Path Pruning
│   └── searchGeneric.py             #   AStarSearcher – bazowy A*
│
├── blocks_world_helper.py           # ★ Nasz kod – helper, heurystyka, solver z timeoutem
├── 5blocks.py                       # ★ Nasz kod – Eksperyment 1
├── 6blocks.py                       # ★ Nasz kod – Eksperyment 2
├── 7blocks.py                       # ★ Nasz kod – Eksperyment 3
├── output/                          # Wyniki eksperymentów (generowane automatycznie)
└── requirements.txt
```

### Forward Planning

**Forward Planning** (planowanie w przód) to strategia przeszukiwania przestrzeni stanów od stanu początkowego do celu:

1. Zaczynamy od stanu początkowego.
2. Sprawdzamy, które akcje mają spełnione warunki wstępne.
3. Generujemy nowe stany będące efektem każdej możliwej akcji.
4. Powtarzamy aż znajdziemy stan spełniający cel.

W naszym projekcie Forward Planning realizuje klasa `Forward_STRIPS`, która zamienia `Planning_problem` na przestrzeń przeszukiwania dla algorytmu **A\* z Multiple-Path Pruning** (`SearcherMPP`). A\* wybiera węzły wg `f(n) = g(n) + h(n)`, gdzie `g(n)` to koszt dotychczasowy, a `h(n)` to heurystyka.

### Heurystyka: `blocks_heuristic`

```python
def blocks_heuristic(state, goal):
    return sum(1 for prop, value in goal.items() if state.get(prop) != value)
```

**Jak działa?** Zlicza liczbę faktów w celu, które **nie są jeszcze spełnione** w bieżącym stanie – czyli ile klocków jest jeszcze w złym miejscu.

**Dlaczego jest poprawna?** Jest to heurystyka **dopuszczalna** (admissible) – nigdy nie przeszacowuje kosztu, ponieważ każdy niespełniony fakt wymaga co najmniej jednej akcji. Dzięki temu A\* gwarantuje znalezienie **optymalnego rozwiązania**.

**Dlaczego pomaga?** Bez heurystyki (`h = 0`) A\* staje się de facto przeszukiwaniem BFS, rozwijając stany „na ślepo". Heurystyka pozwala priorytetyzować stany bliższe celowi, dramatycznie redukując liczbę rozwijanych stanów.

---

## 3. Eksperymenty

### Eksperyment 1: 5 klocków – rozproszone w jedną wieżę

**Opis:** 5 klocków (a, b, c, d, e) leży osobno na stole. Cel: ułożyć je w jedną wieżę a→b→c→d→e.

**Stan początkowy:**
```
    ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
    │ a │ │ b │ │ c │ │ d │ │ e │
    └───┘ └───┘ └───┘ └───┘ └───┘
  ══════════════════════════════════
               STÓŁ
```

**Stan docelowy:**
```
              ┌───┐
              │ a │
              ├───┤
              │ b │
              ├───┤
              │ c │
              ├───┤
              │ d │
              ├───┤
              │ e │
              └───┘
  ══════════════════════════════════
               STÓŁ
```

**Wyniki:**

| Metryka | Bez heurystyki | Z heurystyką | Porównanie |
|---------|---------------|-------------|------------|
| Rozwiązano? | ✅ Tak | ✅ Tak | — |
| Czas | 0.1369 s | 0.0030 s | **~46× szybciej** |
| Rozwinięte stany | 459 | 9 | **~51× mniej** |
| Liczba akcji | 4 | 4 | Identyczna |

**Przebieg rozwiązania krok po kroku:**

**Krok 0 – stan początkowy:**
```
    ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
    │ a │ │ b │ │ c │ │ d │ │ e │
    └───┘ └───┘ └───┘ └───┘ └───┘
  ══════════════════════════════════
```

**Krok 1 – `move_d_from_table_to_e`:** przenosimy klocek `d` na klocek `e`
```
                            ┌───┐
    ┌───┐ ┌───┐ ┌───┐       │ d │
    │ a │ │ b │ │ c │       ├───┤
    └───┘ └───┘ └───┘       │ e │
                            └───┘
  ══════════════════════════════════
```

**Krok 2 – `move_c_from_table_to_d`:** przenosimy klocek `c` na klocek `d`
```
                      ┌───┐
                      │ c │
    ┌───┐ ┌───┐       ├───┤
    │ a │ │ b │       │ d │
    └───┘ └───┘       ├───┤
                      │ e │
                      └───┘
  ══════════════════════════════════
```

**Krok 3 – `move_b_from_table_to_c`:** przenosimy klocek `b` na klocek `c`
```
                ┌───┐
                │ b │
                ├───┤
    ┌───┐       │ c │
    │ a │       ├───┤
    └───┘       │ d │
                ├───┤
                │ e │
                └───┘
  ══════════════════════════════════
```

**Krok 4 – `move_a_from_table_to_b`:** przenosimy klocek `a` na klocek `b`
```
              ┌───┐
              │ a │
              ├───┤
              │ b │
              ├───┤
              │ c │
              ├───┤
              │ d │
              ├───┤
              │ e │
              └───┘
  ══════════════════════════════════
            ✅ CEL!
```

---

### Eksperyment 2: 6 klocków – połączenie wieży z osobnym klockiem

**Opis:** 6 klocków w dwóch stosach: wieża 5-klockowa [a,b,c,d,e] oraz samotny klocek [f] na stole. Cel: ułożyć wszystkie 6 klocków w jedną wieżę a→b→c→d→e→f (f na dole). Problem wymaga rozebrania wieży, przeniesienia klocka e na f, a następnie odbudowania wieży.

**Stan początkowy:**
```
        ┌───┐
        │ a │
        ├───┤
        │ b │
        ├───┤
        │ c │  ┌───┐
        ├───┤  │ f │
        │ d │  └───┘
        ├───┤
        │ e │
        └───┘
  ══════════════════════════════════
               STÓŁ
```

**Stan docelowy:**
```
              ┌───┐
              │ a │
              ├───┤
              │ b │
              ├───┤
              │ c │
              ├───┤
              │ d │
              ├───┤
              │ e │
              ├───┤
              │ f │
              └───┘
  ══════════════════════════════════
               STÓŁ
```

**Wyniki:**

| Metryka | Bez heurystyki | Z heurystyką | Porównanie |
|---------|---------------|-------------|------------|
| Rozwiązano? | ✅ Tak | ✅ Tak | — |
| Czas | 10.2716 s | 0.0715 s | **~144× szybciej** |
| Rozwinięte stany | 4 255 | 223 | **~19× mniej** |
| Liczba akcji | 9 | 9 | Identyczna |

**Przebieg rozwiązania krok po kroku:**

**Krok 0 – stan początkowy:**
```
        ┌───┐
        │ a │
        ├───┤
        │ b │
        ├───┤
        │ c │  ┌───┐
        ├───┤  │ f │
        │ d │  └───┘
        ├───┤
        │ e │
        └───┘
  ════════════════════
```

**Krok 1 – `move_a_from_b_to_table`:** zdejmujemy `a` z wieży na stół
```
        ┌───┐
        │ b │
        ├───┤
        │ c │  ┌───┐  ┌───┐
        ├───┤  │ f │  │ a │
        │ d │  └───┘  └───┘
        ├───┤
        │ e │
        └───┘
  ════════════════════
```

**Krok 2 – `move_b_from_c_to_table`:** zdejmujemy `b` na stół
```
        ┌───┐
        │ c │  ┌───┐  ┌───┐  ┌───┐
        ├───┤  │ f │  │ a │  │ b │
        │ d │  └───┘  └───┘  └───┘
        ├───┤
        │ e │
        └───┘
  ════════════════════
```

**Krok 3 – `move_c_from_d_to_table`:** zdejmujemy `c` na stół
```
                                    ┌───┐
        ┌───┐  ┌───┐  ┌───┐  ┌───┐  │ c │
        │ d │  │ f │  │ a │  │ b │  └───┘
        ├───┤  └───┘  └───┘  └───┘
        │ e │
        └───┘
  ══════════════════════════════════════
```

**Krok 4 – `move_d_from_e_to_a`:** odkładamy `d` tymczasowo na `a`
```
                      ┌───┐
                      │ d │
        ┌───┐  ┌───┐  ├───┤  ┌───┐  ┌───┐
        │ e │  │ f │  │ a │  │ b │  │ c │
        └───┘  └───┘  └───┘  └───┘  └───┘
  ══════════════════════════════════════
```

**Krok 5 – `move_e_from_table_to_f`:** przenosimy `e` na `f`
```
                ┌───┐  ┌───┐
                │ e │  │ d │
                ├───┤  ├───┤  ┌───┐  ┌───┐
                │ f │  │ a │  │ b │  │ c │
                └───┘  └───┘  └───┘  └───┘
  ══════════════════════════════════════
```

**Krok 6 – `move_d_from_a_to_e`:** przenosimy `d` na `e`
```
         ┌───┐
         │ d │
         ├───┤
         │ e │
         ├───┤  ┌───┐  ┌───┐  ┌───┐
         │ f │  │ a │  │ b │  │ c │
         └───┘  └───┘  └───┘  └───┘
  ══════════════════════════════════════
```

**Krok 7 – `move_c_from_table_to_d`:** przenosimy `c` na `d`
```
         ┌───┐
         │ c │
         ├───┤
         │ d │
         ├───┤
         │ e │
         ├───┤  ┌───┐  ┌───┐
         │ f │  │ a │  │ b │
         └───┘  └───┘  └───┘
  ══════════════════════════════════════
```

**Krok 8 – `move_b_from_table_to_c`:** przenosimy `b` na `c`
```
         ┌───┐
         │ b │
         ├───┤
         │ c │
         ├───┤
         │ d │
         ├───┤
         │ e │
         ├───┤  ┌───┐
         │ f │  │ a │
         └───┘  └───┘
  ══════════════════════════════════════
```

**Krok 9 – `move_a_from_table_to_b`:** przenosimy `a` na `b`
```
              ┌───┐
              │ a │
              ├───┤
              │ b │
              ├───┤
              │ c │
              ├───┤
              │ d │
              ├───┤
              │ e │
              ├───┤
              │ f │
              └───┘
  ════════════════════
           ✅ CEL!
```

---

### Eksperyment 3: 7 klocków – trzy stosy w dwie wieże

**Opis:** 7 klocków w trzech stosach: [a,b], [c,d,e], [f,g]. Cel: przeorganizować w dwie wieże [a,c,e,g] i [b,d,f].

**Stan początkowy:**
```
              ┌───┐
    ┌───┐     │ c │   ┌───┐
    │ a │     ├───┤   │ f │
    ├───┤     │ d │   ├───┤
    │ b │     ├───┤   │ g │
    └───┘     │ e │   └───┘
              └───┘
  ══════════════════════════════════
               STÓŁ
```

**Stan docelowy:**
```
    ┌───┐
    │ a │    ┌───┐
    ├───┤    │ b │
    │ c │    ├───┤
    ├───┤    │ d │
    │ e │    ├───┤
    ├───┤    │ f │
    │ g │    └───┘
    └───┘
  ══════════════════════════════════
               STÓŁ
```

**Wyniki:**

| Metryka | Bez heurystyki | Z heurystyką | Porównanie |
|---------|---------------|-------------|------------|
| Rozwiązano? | ❌ **Nie** (timeout 5 min) | ✅ Tak | — |
| Czas | 300.0 s (limit) | 0.0030 s | **~100 000× szybciej** |
| Rozwinięte stany | 14 158 | 15 | **~944× mniej** |
| Liczba akcji | — | 7 | — |

> ⚠️ **Bez heurystyki algorytm nie był w stanie znaleźć rozwiązania w ciągu 5 minut** (timeout), rozwijając ponad 14 tysięcy stanów. Z heurystyką problem został rozwiązany w **0.003 sekundy** przy zaledwie 15 rozwinięciach.

**Przebieg rozwiązania krok po kroku (z heurystyką):**

**Krok 0 – stan początkowy:**
```
              ┌───┐
    ┌───┐     │ c │    ┌───┐
    │ a │     ├───┤    │ f │
    ├───┤     │ d │    ├───┤
    │ b │     ├───┤    │ g │
    └───┘     │ e │    └───┘
              └───┘
  ══════════════════════════════════
```

**Krok 1 – `move_f_from_g_to_table`:** zdejmujemy `f` z `g` na stół
```
              ┌───┐
    ┌───┐     │ c │
    │ a │     ├───┤    ┌───┐  ┌───┐
    ├───┤     │ d │    │ g │  │ f │
    │ b │     ├───┤    └───┘  └───┘
    └───┘     │ e │
              └───┘
  ══════════════════════════════════
```

**Krok 2 – `move_c_from_d_to_a`:** przenosimy `c` na `a`
```
    ┌───┐
    │ c │
    ├───┤    ┌───┐
    │ a │    │ d │    ┌───┐  ┌───┐
    ├───┤    ├───┤    │ g │  │ f │
    │ b │    │ e │    └───┘  └───┘
    └───┘    └───┘
  ══════════════════════════════════
```

**Krok 3 – `move_d_from_e_to_f`:** przenosimy `d` na `f`
```
    ┌───┐
    │ c │
    ├───┤                    ┌───┐
    │ a │    ┌───┐  ┌───┐    │ d │
    ├───┤    │ e │  │ g │    ├───┤
    │ b │    └───┘  └───┘    │ f │
    └───┘                    └───┘
  ══════════════════════════════════
```

**Krok 4 – `move_e_from_table_to_g`:** przenosimy `e` na `g`
```
    ┌───┐
    │ c │
    ├───┤    ┌───┐          ┌───┐
    │ a │    │ e │          │ d │
    ├───┤    ├───┤          ├───┤
    │ b │    │ g │          │ f │
    └───┘    └───┘          └───┘
  ══════════════════════════════════
```

**Krok 5 – `move_c_from_a_to_e`:** przenosimy `c` na `e`
```
              ┌───┐
    ┌───┐     │ c │          ┌───┐
    │ a │     ├───┤          │ d │
    ├───┤     │ e │          ├───┤
    │ b │     ├───┤          │ f │
    └───┘     │ g │          └───┘
              └───┘
  ══════════════════════════════════
```

**Krok 6 – `move_a_from_b_to_c`:** przenosimy `a` na `c`
```
    ┌───┐
    │ a │
    ├───┤
    │ c │                    ┌───┐
    ├───┤                    │ d │
    │ e │    ┌───┐           ├───┤
    ├───┤    │ b │           │ f │
    │ g │    └───┘           └───┘
    └───┘
  ══════════════════════════════════
```

**Krok 7 – `move_b_from_table_to_d`:** przenosimy `b` na `d`
```
    ┌───┐    ┌───┐
    │ a │    │ b │
    ├───┤    ├───┤
    │ c │    │ d │
    ├───┤    ├───┤
    │ e │    │ f │
    ├───┤    └───┘
    │ g │
    └───┘
  ══════════════════════════════════
           ✅ CEL!
```

---

## 4. Podsumowanie wyników

| Problem | Heurystyka | Czas [s] | Rozwinięte stany | Akcje |
|---------|-----------|----------|-------------------|-------|
| 5 klocków | brak | 0.1369 | 459 | 4 |
| 5 klocków | ✅ blocks_heuristic | **0.0030** | **9** | 4 |
| 6 klocków | brak | 10.2716 | 4 255 | 9 |
| 6 klocków | ✅ blocks_heuristic | **0.0715** | **223** | 9 |
| 7 klocków | brak | 300.0 ❌ | 14 158 | — |
| 7 klocków | ✅ blocks_heuristic | **0.0030** | **15** | 7 |

---

## 5. Wnioski

1. **Heurystyka jest kluczowa dla wydajności.** We wszystkich eksperymentach zastosowanie heurystyki `blocks_heuristic` drastycznie zmniejszyło liczbę rozwijanych stanów (od 19× do 944×) i czas rozwiązywania (od 46× do ~100 000×).

2. **Bez heurystyki duże problemy są nierozwiązywalne w rozsądnym czasie.** Problem 7 klocków bez heurystyki nie został rozwiązany w limicie 5 minut (14 158 rozwinięć), natomiast z heurystyką rozwiązanie znaleziono w 0.003s przy 15 rozwinięciach. Problem 6 klocków bez heurystyki wymagał ponad 10 sekund i 4 255 stanów, a z heurystyką – zaledwie 0.07s i 223 stany.

3. **Heurystyka nie wpływa na optymalność rozwiązania.** Ponieważ nasza heurystyka jest dopuszczalna (admissible), A\* gwarantuje znalezienie planu o minimalnej liczbie akcji – zarówno z heurystyką, jak i bez niej rozwiązania mają tę samą długość (4, 9, 7 akcji).

4. **Złożoność Blocks World rośnie wykładniczo.** Dla *n* klocków przestrzeń stanów rośnie jako ~*n*!, co widać po wzroście czasu: 5 klocków (0.14s) → 6 klocków (10.27s) → 7 klocków (timeout). Heurystyka pozwala efektywnie „przycinać" tę przestrzeń.

5. **Forward Planning z A\* i dopuszczalną heurystyką** to skuteczna metoda rozwiązywania problemów Blocks World – łączy gwarancję optymalności z efektywnym przeszukiwaniem przestrzeni stanów.
