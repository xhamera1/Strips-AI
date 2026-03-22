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

## 4. Eksperymenty z podcelami (subgoals)

### Czym są podcele?

**Podcele (subgoals)** to technika dekompozycji problemu planowania. Zamiast rozwiązywać cały problem od razu (stan początkowy → cel końcowy), rozbijamy cel na **mniejsze cele pośrednie** i rozwiązujemy je po kolei:

```
Stan początkowy → Podcel 1 → Podcel 2 → ... → Cel końcowy
```

**Dlaczego to pomaga?** Przeszukiwanie przestrzeni stanów ma złożoność wykładniczą. Jeśli pełny problem wymaga np. 9 akcji, algorytm musi przeszukać ogromną przestrzeń. Rozbijając na 3 podproblemy po ~3 akcje każdy, każdy podproblem ma **znacznie mniejszą przestrzeń** do przeszukania. Suma małych przestrzeni jest dużo mniejsza niż jedna wielka.

**Kompromis:** Podcele nie gwarantują optymalnego globalnego rozwiązania – plan może mieć więcej akcji niż optymalny (bo narzucamy kolejność osiągania celów). W zamian zyskujemy dramatyczne przyspieszenie.

### Zdefiniowane podcele

**5 klocków** (rozproszone → wieża [a,b,c,d,e]):
- **Podcel 1:** `{d_is_on: e}` — zbuduj dolną parę
- **Podcel 2:** `{c_is_on: d, d_is_on: e}` — zbuduj dolną trójkę
- **Cel końcowy:** pełna wieża a→b→c→d→e

**6 klocków** (wieża [a,b,c,d,e] + [f] → wieża [a,b,c,d,e,f]):
- **Podcel 1:** `{e_is_on: f}` — rozebraj wieżę i postaw e na f
- **Podcel 2:** `{d_is_on: e, c_is_on: d, e_is_on: f}` — odbuduj środek
- **Cel końcowy:** pełna wieża a→b→c→d→e→f

**7 klocków** (trzy stosy → dwie wieże):
- **Podcel 1:** `{e_is_on: g, f_is_on: table}` — zbuduj podstawę pierwszej wieży, uwolnij f
- **Podcel 2:** `{c_is_on: e, d_is_on: f, e_is_on: g}` — rozbuduj obie wieże
- **Cel końcowy:** dwie wieże [a,c,e,g] i [b,d,f]

### Wyniki z podcelami

**5 klocków z podcelami:**

| Etap | Bez heurystyki | Z heurystyką |
|------|---------------|-------------|
| Podcel 1 (d na e) | 0.001s, 6 stanów, 1 akcja | 0.001s, 2 stany, 1 akcja |
| Podcel 2 (c na d) | 0.000s, 2 stany, 1 akcja | 0.000s, 2 stany, 1 akcja |
| Cel końcowy | 0.002s, 11 stanów, 2 akcje | 0.001s, 4 stany, 2 akcje |
| **Łącznie** | **0.003s, 19 stanów, 4 akcje** | **0.002s, 8 stanów, 4 akcje** |

**6 klocków z podcelami:**

| Etap | Bez heurystyki | Z heurystyką |
|------|---------------|-------------|
| Podcel 1 (e na f) | 0.075s, 202 stany, 5 akcji | 0.021s, 91 stanów, 5 akcji |
| Podcel 2 (d na e, c na d) | 0.008s, 39 stanów, 2 akcje | 0.002s, 4 stany, 2 akcje |
| Cel końcowy | 0.004s, 21 stanów, 2 akcje | 0.000s, 3 stany, 2 akcje |
| **Łącznie** | **0.087s, 262 stany, 9 akcji** | **0.023s, 98 stanów, 9 akcji** |

**7 klocków z podcelami:**

| Etap | Bez heurystyki | Z heurystyką |
|------|---------------|-------------|
| Podcel 1 (e na g, f na stół) | 2.060s, 1069 stanów, 4 akcje | 0.009s, 30 stanów, 4 akcje |
| Podcel 2 (c na e, d na f) | 0.035s, 91 stanów, 2 akcje | 0.001s, 3 stany, 2 akcje |
| Cel końcowy | 0.009s, 35 stanów, 2 akcje | 0.001s, 3 stany, 2 akcje |
| **Łącznie** | **2.104s, 1 195 stanów, 8 akcji** | **0.011s, 36 stanów, 8 akcji** |

> ⚠️ **Najważniejszy wynik:** Problem 7 klocków **bez heurystyki** wymagał timeoutu (5 min) przy bezpośrednim rozwiązywaniu. Z podcelami rozwiązał się w **2.1 sekundy** (nawet bez heurystyki!). Z podcelami + heurystyką — zaledwie 0.011s.

---

## 5. Podsumowanie wyników

### Bezpośrednie rozwiązywanie (bez podceli)

| Problem | Heurystyka | Czas [s] | Rozwinięte stany | Akcje |
|---------|-----------|----------|-------------------|-------|
| 5 klocków | brak | 0.1369 | 459 | 4 |
| 5 klocków | ✅ blocks_heuristic | **0.0030** | **9** | 4 |
| 6 klocków | brak | 10.2716 | 4 255 | 9 |
| 6 klocków | ✅ blocks_heuristic | **0.0715** | **223** | 9 |
| 7 klocków | brak | 300.0 ❌ | 14 158 | — |
| 7 klocków | ✅ blocks_heuristic | **0.0030** | **15** | 7 |

### Z podcelami

| Problem | Heurystyka | Czas [s] | Rozwinięte stany | Akcje |
|---------|-----------|----------|-------------------|-------|
| 5 klocków | brak | 0.0034 | 19 | 4 |
| 5 klocków | ✅ blocks_heuristic | **0.0018** | **8** | 4 |
| 6 klocków | brak | 0.0867 | 262 | 9 |
| 6 klocków | ✅ blocks_heuristic | **0.0231** | **98** | 9 |
| 7 klocków | brak | 2.1037 | 1 195 | 8 |
| 7 klocków | ✅ blocks_heuristic | **0.0110** | **36** | 8 |

### Porównanie — wpływ podceli na rozwinięte stany (bez heurystyki)

| Problem | Bez podceli | Z podcelami | Redukcja |
|---------|-----------|-------------|----------|
| 5 klocków | 459 | 19 | **24×** |
| 6 klocków | 4 255 | 262 | **16×** |
| 7 klocków | 14 158 (timeout) | 1 195 | **12×** (i rozwiązany!) |

### 4.2 Duże problemy z podcelami (minimum 20 akcji)

Dodatkowo zdefiniowaliśmy i rozwiązaliśmy trzy problemy wymagające **minimum 20 instancji akcji**. Każdy problem uruchomiono zarówno bez heurystyki, jak i z heurystyką.

**Problem A: 12 klocków – wieża → dwie wieże bloki naprzemiennie** (`12blocks_subgoals.py`)
- Start: [a,b,c,d,e,f,g,h,i,j,k,l] (jedna wieża)
- Cel: [a,c,e,g,i,k] i [b,d,f,h,j,l]
- 5 podceli

| Metryka | Bez heurystyki | Z heurystyką |
|---------|---------------|-------------|
| Rozwiązano? | ❌ Nie (timeout na podcelu 2) | ✅ Tak |
| Czas | 300+ s | **0.39 s** |
| Rozwinięte stany | 7 112 | **29** |
| **Liczba akcji** | — | **21** |

---

**Problem B: 15 klocków – pięć stosów po 3 → trzy stosy po 5** (`15blocks_subgoals.py`)
- Start: [a,b,c], [d,e,f], [g,h,i], [j,k,l], [m,n,o]
- Cel: [a,e,i,l,o], [b,f,j,m,c], [d,h,k,n,g]
- 4 podcele

| Metryka | Bez heurystyki | Z heurystyką |
|---------|---------------|-------------|
| Rozwiązano? | ❌ Nie (timeout na podcelu 1) | ✅ Tak |
| Czas | 300+ s | **0.36 s** |
| Rozwinięte stany | 6 029 | **27** |
| **Liczba akcji** | — | **22** |

---

**Problem C: 14 klocków – wieża → trzy wieże naprzemieniowe** (`14blocks_subgoals.py`)
- Start: [a,b,c,d,e,f,g,h,i,j,k,l,m,n] (jedna wieża)
- Cel: [a,d,g,j,m], [b,e,h,k,n], [c,f,i,l]
- 5 podceli

| Metryka | Bez heurystyki | Z heurystyką |
|---------|---------------|-------------|
| Rozwiązano? | ❌ Nie (timeout na podcelu 2) | ✅ Tak |
| Czas | 345+ s (podcel 1: 45s, podcel 2: timeout) | **0.74 s** |
| Rozwinięte stany | 9 275 | **30** |
| **Liczba akcji** | — | **24** |

> ⚠️ **Wniosek:** Dla dużych problemów (12–15 klocków) **samo rozbicie na podcele nie wystarcza** — bez heurystyki solver wciąż trafia na timeout. Dopiero **połączenie podceli z heurystyką** pozwala rozwiązać te problemy w ułamku sekundy, rozwijając zaledwie ~30 stanów zamiast tysięcy.

---

## 6. Wnioski

1. **Heurystyka jest kluczowa dla wydajności.** We wszystkich eksperymentach zastosowanie heurystyki `blocks_heuristic` drastycznie zmniejszyło liczbę rozwijanych stanów i czas rozwiązywania (od 46× do ~100 000× szybciej).

2. **Bez heurystyki duże problemy są nierozwiązywalne w rozsądnym czasie.** Problem 7 klocków bez heurystyki nie został rozwiązany w limicie 5 minut (14 158 rozwinięć), natomiast z heurystyką rozwiązanie znaleziono w 0.003s przy 15 rozwinięciach.

3. **Podcele dramatycznie redukują przestrzeń przeszukiwania.** Rozbicie problemu na podcele zmniejszyło liczbę stanów od 12× do 24×. Co najważniejsze — problem 7 klocków, który **bez podceli nie rozwiązywał się w 5 minut**, z podcelami rozwiązał się w 2.1s (bez heurystyki) lub 0.011s (z heurystyką).

4. **Podcele mogą dawać nieoptymalne rozwiązania.** Problem 7 klocków bezpośrednio wymaga 7 akcji (optymalnie), ale z podcelami rozwiązanie ma 8 akcji — narzucona kolejność podceli wymusza dodatkowy ruch. Jest to kompromis: tracimy optymalność, ale zyskujemy możliwość rozwiązania w rozsądnym czasie.

5. **Heurystyka + podcele = najlepsza kombinacja.** Łącząc obie techniki, nawet najtrudniejszy problem (7 klocków) rozwiązał się w 0.011s przy 36 rozwinięciach — ponad 1000× szybciej niż sam forward planning bez żadnych optymalizacji.

6. **Złożoność Blocks World rośnie wykładniczo.** Dla *n* klocków przestrzeń stanów rośnie jako ~*n*!, co widać po wzroście czasu. Zarówno heurystyka, jak i podcele to komplementarne techniki „przycinania" tej przestrzeni.
