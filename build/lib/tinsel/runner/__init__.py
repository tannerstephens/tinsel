from argparse import ArgumentParser
from pathlib import Path
from importlib import import_module
from re import compile
from typing import Callable
from time import time
from os import path
from shutil import copytree
import sys

class Runner:
  DAY_REGEX = compile(r'day(\d+)')

  def __init__(self) -> None:
    self.directory = Path.cwd()
    self.days = self._load_all_days()

  def _load_all_days(self):
    days = {}

    for day_path in self.directory.glob('day*'):
      day = int(self.DAY_REGEX.match(day_path.name).groups()[0])
      module = import_module(f'{day_path.name}.run')

      days[day] = module

    return days

  def get_function_execution_time_and_result(self, f: Callable):
    '''Returns the provided functions execution time in ms and its result'''
    start = time()
    res = f()
    seconds = time() - start

    return round(seconds * 1000, 2), res

  def parse_arguments(self):
    parser = ArgumentParser()

    parser.add_argument('-d', '--day', help='Run a specific day', type=int)
    parser.add_argument('-r', '--run', help='Alias for --day', type=int, dest='day')
    parser.add_argument('-c', '--create', help='Create a new day folder from the template', type=int, const=-1, nargs='?')
    parser.add_argument('-a', '--all', help='Run all days', action='store_true')

    return parser.parse_args()

  def run_day(self, n):
    print(f'Day {n}')

    n = int(n)

    day_module = self.days[n]

    part1_time, part1_res = self.get_function_execution_time_and_result(
      day_module.part1)
    print(f'  Part 1: {part1_res} - {part1_time} ms')

    part2_time, part2_res = self.get_function_execution_time_and_result(
      day_module.part2)
    print(f'  Part 2: {part2_res} - {part2_time} ms\n')

    return part1_time + part2_time

  def run_all_days(self):
    day_keys = sorted(self.days.keys(), key=int)

    total_time = 0

    for day in day_keys:
      total_time += self.run_day(day)

    total_time = round(total_time, 2)
    average_time = round(total_time / len(self.days), 2)
    average_part = round(total_time / len(self.days) / 2, 2)

    print(f'Total Time: {total_time} ms')
    print(f'Average Day Time: {average_time} ms')
    print(f'Average Part Time: {average_part} ms')

  def create_from_template(self, n):
    class_path = path.dirname(path.abspath(__file__))

    breakpoint()

    copytree(f'{class_path}/day_template', f'{self.directory}/day{n}')

  def create_day(self, n):
    if n in self.days:
      print(f'ERROR! Day "{n}" already created!')
      return

    if n == -1:
      n = (max(self.days.keys(), key=int) + 1) if len(self.days) else 1

    self.create_from_template(n)

  def run(self):
    args = self.parse_arguments()

    if args.create:
      self.create_day(args.create)

    elif args.day:
      self.run_day(args.day)

    elif args.all:
      self.run_all_days()

    else:
      if not self.days:
        print(f'Day 1 has not yet been created. Run {sys.argv[0]} -c')
        return
      latest_day = max(self.days.keys(), key=int)
      self.run_day(latest_day)

if __name__ == '__main__':
  Runner().run()
