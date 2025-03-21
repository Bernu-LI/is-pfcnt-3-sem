import sympy


def main():
    print("Эта программа рассчитывает узловые потенциалы и токи в схеме, состоящей из резисторов и источников ЭДС.")
    print("Для упрощения принимается, что узел 0 является опорным (его потенциал = 0 В).")
    print("======================================\n")

    # Считываем количество узлов и ветвей
    n = int(input("Введите количество узлов (включая узел 0): "))
    m = int(input("Введите количество ветвей: "))

    # Переменные узловых потенциалов (кроме нулевого узла)
    # Если всего n узлов, индексы узлов 0..(n-1),
    # то у нас будет (n-1) неизвестных потенциалов: V1, V2, ..., V_{n-1}
    V = sympy.symbols(f'V1:{n}', real=True)  # (V1, V2, ..., V_{n-1})

    # Составим список уравнений. Для каждого из (n-1) узлов (кроме 0)
    # запишем уравнение KCL: сумма всех токов в узел = 0
    # Также будут уравнения для идеальных источников ЭДС (разность потенциалов = E)

    equations = []

    # Храним все ветви в списке для последующего вычисления токов
    branches = []

    print("\nВведите описание каждой ветви в формате:")
    print("start_node end_node type value")
    print(" - start_node, end_node: номера узлов (целые)")
    print(" - type: R или E (резистор или ЭДС)")
    print(" - value: число (сопротивление в Ом или ЭДС в Вольтах)")
    print("Пример: 0 1 R 10\n")

    for _ in range(m):
        line = input(f"Ветвь {_ + 1}: ").strip().split()
        start_node = int(line[0])
        end_node = int(line[1])
        elem_type = line[2].upper()
        value = float(line[3])

        branches.append((start_node, end_node, elem_type, value))

    # Для KCL нам нужно накапливать токи в узлы (кроме 0).
    # Создадим словарь, где ключ = номер узла, а значение = выражение (sympy) суммы токов (пока 0).
    current_balance = {node: 0 for node in range(1, n)}  # узел 0 не пишем

    # Доп. список уравнений для идеальных источников (связь потенциалов)
    source_equations = []

    # Функция, чтобы получить символ sympy для потенциала узла.
    #  - для узла 0 возвращаем 0 (опорный потенциал),
    #  - для остальных возвращаем соответствующую переменную V[node].
    def V_node(node_idx):
        if node_idx == 0:
            return 0
        else:
            # индекс в списке V идёт от 0..(n-2), а сам узел идёт от 1..(n-1)
            # потому что узел 0 — опорный
            return V[node_idx - 1]

    for (start_node, end_node, elem_type, val) in branches:
        v_s = V_node(start_node)
        v_e = V_node(end_node)

        if elem_type == 'R':
            # Ток из start_node в end_node: (V_s - V_e)/R
            # В уравнениях KCL этот ток будет со знаком "+" для узла start_node
            # и со знаком "-" для узла end_node (т.к. он "выходит" из start_node, "входит" в end_node).
            I = (v_s - v_e) / val

            # Если start_node != 0, добавим в баланс тока
            if start_node != 0:
                current_balance[start_node] += I
            # Если end_node != 0, учтём ток (но уже со знаком минус, т.к. он входит в end_node)
            if end_node != 0:
                current_balance[end_node] -= I

        elif elem_type == 'E':
            # Идеальный источник ЭДС фиксирует (v_s - v_e) = E (или = +val).
            # По условию: потенциал start_node минус потенциал end_node = val.
            # Это дополнительное уравнение.
            source_equations.append(v_s - v_e - val)

            # Ток через идеальный источник не задаётся напрямую (теоретически неограничен).
            # Однако в реальных схемах мы бы могли добавить внутреннее сопротивление.
            # Для баланса токов в узлах также нужно учесть "I" через идеальный источник.
            # Но поскольку значение тока I не задано, для KCL мы должны ввести неизвестный ток источника.
            # Упростим задачу: будем считать, что в KCL через идеальный источник идет некоторый I.
            # Тогда KCL формально: I_источника вытекает из start_node, втекает в end_node.
            # Но нам нужен ещё один символ (ток) для каждого источника. Давайте введём его.

            I_symbol = sympy.Symbol(f'I_E_{start_node}_{end_node}', real=True)

            # Добавим этот ток в балансы
            if start_node != 0:
                current_balance[start_node] += I_symbol
            if end_node != 0:
                current_balance[end_node] -= I_symbol

            # Сохраним в списке ветвей (для вывода тока тоже)
            # Теперь в branches у нас (start_node, end_node, 'E', value, I_symbol)
            # вместо простого кортежа. Чтобы не ломать логику, создадим новый список.

    # Теперь формируем уравнения KCL для всех узлов (кроме 0)
    for node in range(1, n):
        eq = current_balance[node]
        equations.append(eq)

    # Добавим уравнения, связанные с идеальными источниками
    equations.extend(source_equations)

    # Теперь у нас могут быть дополнительные неизвестные: токи источников.
    # Нужно собрать все символы, которые фигурируют в уравнениях.
    # В уравнениях точно есть V1..V_{n-1}. Но могут появиться I_E_...
    all_symbols = set()
    for eq in equations:
        all_symbols.update(eq.free_symbols)

    # Превратим set в список с упорядочением
    all_symbols = list(all_symbols)

    # Решаем систему
    solutions = sympy.solve(equations, all_symbols, dict=True)

    if not solutions:
        print("\nСистема не имеет решения или переопределена. Проверьте входные данные.")
        return

    # Предположим, что решение единственное:
    sol = solutions[0]

    # Выводим найденные узловые потенциалы V1..V_{n-1}
    print("\nРЕЗУЛЬТАТЫ РАСЧЁТА:")
    print("Узловые потенциалы (В):")
    for node_idx in range(1, n):
        v_sym = V[node_idx - 1]  # это символ V1..V_{n-1}
        value_sol = sol.get(v_sym, 0)
        print(f"  V({node_idx}) = {value_sol} В")

    # Теперь найдём токи в каждой ветви.
    # Нам нужно восстановить формулу тока для резисторов и посмотреть, чему равен I_источника для ЭДС.
    print("\nТоки в ветвях (А):")

    # Для вычисления тока в резисторе: I = (V_s - V_e)/R
    # (учитываем положительное направление "из start_node в end_node")
    # Для источника: I = найденное значение I_E_start_end из решения sol
    for idx, (start_node, end_node, elem_type, val) in enumerate(branches, 1):
        v_s = V_node(start_node)
        v_e = V_node(end_node)

        if elem_type == 'R':
            # Подставляем решения узловых потенциалов
            I_expr = (v_s - v_e) / val
            # Заменяем V1..V_{n-1} в I_expr найденными числами
            I_val = I_expr.subs(sol)
            print(f"  Ветвь {idx}: R={val} Ом  (из узла {start_node} в узел {end_node})  I = {I_val.evalf()} А")
        else:
            # По соглашению, разность потенциалов v_s - v_e = val (ЭДС).
            # Ток через источник мы ввели как I_E_{start_node}_{end_node}, смотрим в sol
            I_symbol = sympy.Symbol(f'I_E_{start_node}_{end_node}', real=True)
            I_val = sol.get(I_symbol, 0)
            print(f"  Ветвь {idx}: E={val} В   (из узла {start_node} в узел {end_node})  I = {I_val.evalf()} А")

    print("\nРасчёт окончен.")


if __name__ == "__main__":
    main()
