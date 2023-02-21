# -*- coding: UTF-8 -*-
# This file is part of the jetson_stats package (https://github.com/rbonghi/jetson_stats or http://rnext.it).
# Copyright (c) 2019-2023 Raffaello Bonghi.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import curses
from .colors import NColors
from .common import size_to_string


header = {
    "PID": {'clm': 7, 'fn': lambda x: str(x)},
    "USER": {'clm': 12, 'fn': lambda x: x},
    "PRI": {'clm': 6, 'fn': lambda x: str(x)},
    "S": {'clm': 4, 'fn': lambda x: x},
    "CPU%": {'clm': 12, 'fn': lambda x: "{:.2f}".format(x)},
    "GPU MEM": {'clm': 12, 'fn': lambda x: size_to_string(x, 'k')},
    "Command": {'clm': 20, 'fn': lambda x: x},
}


class ProcessTable(object):

    def __init__(self, stdscr, processes):
        self.stdscr = stdscr
        self.processes = processes
        self.line_sort = 5
        self.type_reverse = True

    def draw(self, pos_y, pos_x, width, height, key, mouse):
        # Plot low bar background line
        self.stdscr.addstr(pos_y, 0, " " * width, NColors.igreen())
        title_counter = 0
        for idx, (title, info) in enumerate(header.items()):
            try:
                # Check if pressed
                if mouse and mouse[1] == pos_y and title_counter <= mouse[0] <= title_counter + info['clm']:
                    if self.line_sort != idx:
                        self.line_sort = idx
                        self.type_reverse = True
                    else:
                        self.type_reverse = not self.type_reverse
                # Draw title
                title = "[{}]".format(title) if idx == self.line_sort else title
                self.stdscr.addstr(pos_y, title_counter, title, NColors.igreen() | curses.A_BOLD)
                title_counter += info['clm']
            except curses.error:
                break
        # Sort table for selected line
        sorted_processes = sorted(self.processes, key=lambda x: x[self.line_sort], reverse=self.type_reverse)
        # Draw all processes
        for nprocess, process in enumerate(sorted_processes):
            # Skip unit size process
            counter = 0
            for (value, info) in zip(process, header.values()):
                # Print all values in a nice view
                try:
                    self.stdscr.addstr(pos_y + nprocess + 1, counter, info['fn'](value), curses.A_NORMAL)
                    counter += info['clm']
                except curses.error:
                    break
        return len(self.processes)