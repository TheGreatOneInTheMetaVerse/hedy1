import textwrap

from parameterized import parameterized

import hedy
from hedy_sourcemap import SourceRange
# from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping  # , SkippedMapping


class TestsLevel18(HedyTester):
    level = 18

    @parameterized.expand([['(', ')'], ['（', '）']])
    def test_print_brackets(self, bracket_open, bracket_close):
        code = textwrap.dedent(f"""\
      print{bracket_open}'Hallo!'{bracket_close}""")

        expected = textwrap.dedent("""\
      print(f'''Hallo!''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            expected_commands=['print']
        )

    def test_print_var_brackets(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        print('ik heet', naam)""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        print(f'''ik heet{naam}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_print_comma(self):
        code = "print('ik heet ,')"
        expected = "print(f'''ik heet ,''')"
        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle())

    @parameterized.expand(['=', 'is'])
    def test_input(self, assigment):
        code = textwrap.dedent(f"""\
        leeftijd {assigment} input('Hoe oud ben jij?')
        print(leeftijd)""")
        expected = textwrap.dedent("""\
        leeftijd = input(f'''Hoe oud ben jij?''')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        print(f'''{leeftijd}''')""")

        self.multi_level_tester(
            max_level=20,
            code=code,
            expected=expected,
            translate=False,
            extra_check_function=self.is_not_turtle()
        )

    @parameterized.expand([':', '：'])
    def test_if_with_dequals_sign_colon(self, colon):
        code = textwrap.dedent(f"""\
      naam is 'Hedy'
      if naam == Hedy{colon}
          print('koekoek')""")

        expected = textwrap.dedent("""\
      naam = 'Hedy'
      if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
        print(f'''koekoek''')""")

        self.single_level_tester(code=code, expected=expected)

    # issue also in level 17, leaving for now.
    # def test_bigger(self):
    #     code = textwrap.dedent("""\
    #     leeftijd is input('Hoe oud ben jij?')
    #     if leeftijd > 12:
    #         print('Dan ben je ouder dan ik!')""")
    #     expected = textwrap.dedent("""\
    #     leeftijd = input('Hoe oud ben jij?')
    #     if int(leeftijd) > int('12'):
    #       print(f'Dan ben je ouder dan ik!')""")
    #
    #     self.multi_level_tester(
    #       code=code,
    #       expected=expected,
    #       extra_check_function=self.is_not_turtle(),
    #       test_name=self.name()
    #     )
    # def test_big_and_small(self):
    #     code = textwrap.dedent("""\
    #     leeftijd is input('Hoe oud ben jij?')
    #     if leeftijd < 12:
    #         print('Dan ben je jonger dan ik!')
    #     elif leeftijd > 12:
    #         print('Dan ben je ouder dan ik!')""")
    #     expected = textwrap.dedent("""\
    #     leeftijd = input('Hoe oud ben jij?')
    #     if int(leeftijd) < int('12'):
    #       print(f'Dan ben je jonger dan ik!')
    #     elif int(leeftijd) > int('12'):
    #       print(f'Dan ben je ouder dan ik!')""")
    #
    #     self.multi_level_tester(
    #       max_level=20,
    #       code=code,
    #       expected=expected,
    #       extra_check_function=self.is_not_turtle(),
    #       test_name=self.name()
    #     )

    def test_if_else(self):
        code = textwrap.dedent("""\
      antwoord is input('Hoeveel is 10 plus 10?')
      if antwoord is 20:
          print('Goedzo!')
          print('Het antwoord was inderdaad', antwoord)
      else:
          print('Foutje')
          print('Het antwoord moest zijn', antwoord)""")

        expected = textwrap.dedent("""\
      antwoord = input(f'''Hoeveel is 10 plus 10?''')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '20'):
        print(f'''Goedzo!''')
        print(f'''Het antwoord was inderdaad{antwoord}''')
      else:
        print(f'''Foutje''')
        print(f'''Het antwoord moest zijn{antwoord}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            translate=False,
            expected_commands=['input', 'if', 'print', 'print', 'print', 'print'],
            extra_check_function=self.is_not_turtle()
        )

    def test_for_loop(self):
        code = textwrap.dedent("""\
      a is 2
      b is 3
      for a in range(2, 4):
          a is a + 2
          b is b + 2""")
        expected = textwrap.dedent("""\
      a = 2
      b = 3
      step = 1 if 2 < 4 else -1
      for a in range(2, 4 + step, step):
        a = a + 2
        b = b + 2
        time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_for_nesting(self):
        code = textwrap.dedent("""\
      for i in range(1, 3):
          for j in range(1, 4):
              print('rondje: ', i, ' tel: ', j)""")
        expected = textwrap.dedent("""\
      step = 1 if 1 < 3 else -1
      for i in range(1, 3 + step, step):
        step = 1 if 1 < 4 else -1
        for j in range(1, 4 + step, step):
          print(f'''rondje: {i} tel: {j}''')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
      for دورة in range(١, ٥):
          print(دورة)""")

        expected = textwrap.dedent("""\
      step = 1 if 1 < 5 else -1
      for دورة in range(1, 5 + step, step):
        print(f'''{دورة}''')
        time.sleep(0.1)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_input_with_list(self):
        code = textwrap.dedent("""\
      color is ['green', 'blue']
      choice is input('Is your favorite color one of: ', color)""")

        expected = textwrap.dedent("""\
      color = ['green', 'blue']
      choice = input(f'''Is your favorite color one of: {color}''')
      try:
        choice = int(choice)
      except ValueError:
        try:
          choice = float(choice)
        except ValueError:
          pass""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=self.is_not_turtle()
        )

    def test_input_without_text_inside(self):
        code = "x = input()"
        expected = textwrap.dedent("""\
      x = input(f'''''')
      try:
        x = int(x)
      except ValueError:
        try:
          x = float(x)
        except ValueError:
          pass""")
        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=self.is_not_turtle()
        )

    def test_print_without_text_inside(self):
        self.multi_level_tester(
            code="print()",
            expected="print(f'''''')",
            extra_check_function=self.is_not_turtle()
        )

    # negative tests

    def test_while_undefined_var(self):
        code = textwrap.dedent("""\
        while antwoord != 25:
            print('hoera')""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException
        )

    def test_var_undefined_error_message(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        print('ik heet ', name)""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException
        )

        # deze extra check functie kan nu niet mee omdat die altijd op result werkt
        # evt toch splitsen in 2 (pos en neg?)
        # self.assertEqual('name', context.exception.arguments['name'])

    def test_input_without_argument(self):
        self.multi_level_tester(
            code="name is input",
            exception=hedy.exceptions.IncompleteCommandException
        )

    #
    # Test comment
    #
    def test_print_comment(self):
        code = "print('Hallo welkom bij Hedy!') # This is a comment"
        expected = "print(f'''Hallo welkom bij Hedy!''')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output
        )

    #
    # button tests
    #

    def test_if_button_is_pressed_print(self):
        code = textwrap.dedent("""\
        x = 'PRINT'
        x is button
        if PRINT is pressed:
            print('The button got pressed!')""")

        expected = HedyTester.dedent(f"""\
        x = 'PRINT'
        create_button(x)
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRINT':
              print(f'''The button got pressed!''')
              break
            # End of PyGame Event Handler""")

        self.single_level_tester(code=code, expected=expected)

    def test_nested_functions(self):
        code = textwrap.dedent("""\
        def simple_function():
            def nested_function():
                print(1)
        simple_function()""")

        expected = textwrap.dedent("""\
        pass
        simple_function()""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 3, 35), hedy.exceptions.NestedFunctionException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )
