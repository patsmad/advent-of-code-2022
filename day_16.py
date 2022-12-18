from get_input import get_input
import re

day_num = 16
raw_input = get_input(day_num)

test_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()

input = raw_input

class Valve:
    def __init__(self, name, rate=None):
        self.name = name
        self.rate = rate
        self.edges = []

class Graph:
    pattern = 'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
    def __init__(self, graph_input):
        self.valves = {}
        for line in graph_input.split('\n'):
            valve, rate, to_valves = re.match(self.pattern, line).groups()
            if valve not in self.valves:
                self.valves[valve] = Valve(valve)
            self.valves[valve].rate = int(rate)
            for edge in to_valves.split(', '):
                if edge not in self.valves:
                    self.valves[edge] = Valve(edge)
                self.valves[valve].edges.append(self.valves[edge])
        self.total_rate = sum([v.rate for v in self.valves.values()])
        self.bfs_valves = {valve.name: Valve(valve.name, valve.rate) for valve in self.valves.values()}
        non_zero_valves = [v for v in self.valves.values() if v.rate > 0 or v.name == 'AA']
        for valve in non_zero_valves:
            for other_valve in non_zero_valves:
                if valve != other_valve and other_valve != self.valves['AA']:
                    self.bfs_valves[valve.name].edges.append((self.bfs(valve, other_valve), self.bfs_valves[other_valve.name]))

    def bfs(self, start_valve, end_valve):
        seen_valves = [start_valve]
        queue = [(1, v) for v in start_valve.edges]
        while len(queue) > 0:
            steps, new_valve = queue.pop(0)
            seen_valves.append(new_valve)
            if new_valve == end_valve:
                return steps
            for edge_valve in new_valve.edges:
                if edge_valve not in seen_valves:
                    queue.append((steps + 1, edge_valve))

    def bfs_dfs(self):
        max_flow = 0
        valve_state = {v[1].name: False for v in self.bfs_valves['AA'].edges}
        queue = [(0, 0, valve_state.copy(), 30, v[0], v[1]) for v in self.bfs_valves['AA'].edges]
        while len(queue) > 0:
            total_flow, curr_flow, valve_state, minutes_remaining, steps, next_valve = queue.pop()
            if minutes_remaining < steps:
                steps = minutes_remaining
            minutes_remaining -= steps
            total_flow += curr_flow * steps
            if minutes_remaining == 0:
                if total_flow > max_flow:
                    max_flow = total_flow
            else:
                max_potential_flow = self.total_rate * minutes_remaining
                if total_flow + max_potential_flow > max_flow:
                    if not valve_state[next_valve.name]:
                        total_flow += curr_flow
                        minutes_remaining -= 1
                        curr_flow += next_valve.rate
                        valve_state[next_valve.name] = True
                    if minutes_remaining == 0 or sum(valve_state.values()) == len(valve_state):
                        steps = minutes_remaining
                        total_flow += curr_flow * steps
                        if total_flow > max_flow:
                            max_flow = total_flow
                    else:
                        available_edges = [edge_valve for edge_valve in next_valve.edges if not valve_state[edge_valve[1].name]]
                        for edge_valve in available_edges:
                            queue.append((total_flow, curr_flow, valve_state.copy(), minutes_remaining, edge_valve[0], edge_valve[1]))
        print(max_flow)

    def bfs_dfs_2(self):
        max_flow = 0
        start_positions = self.bfs_valves['AA'].edges
        valve_state = {v[1].name: False for v in start_positions}
        queue = []
        for i in range(len(start_positions)):
            for j in range(i + 1, len(start_positions)):
                queue.append((0, 0, valve_state.copy(), 26, start_positions[i][0], start_positions[i][1], start_positions[j][0], start_positions[j][1]))
        while len(queue) > 0:
            total_flow, curr_flow, valve_state, minutes_remaining, my_steps, my_next_valve, elephant_steps, elephant_next_valve = queue.pop()
            steps = my_steps if my_steps <= elephant_steps else elephant_steps
            next_valves = []
            replace_me, replace_elephant = False, False
            if my_steps <= elephant_steps or valve_state[my_next_valve.name]:
                replace_me = True
                if not valve_state[my_next_valve.name]:
                    next_valves.append(my_next_valve)
            if elephant_steps <= my_steps or valve_state[elephant_next_valve.name]:
                replace_elephant = True
                if elephant_next_valve != my_next_valve and not valve_state[elephant_next_valve.name]:
                    next_valves.append(elephant_next_valve)
            if minutes_remaining < steps:
                steps = minutes_remaining
            minutes_remaining -= steps
            total_flow += curr_flow * steps
            if minutes_remaining == 0:
                if total_flow > max_flow:
                    max_flow = total_flow
                    print(max_flow)
            else:
                max_potential_flow = self.total_rate * minutes_remaining
                if total_flow + max_potential_flow > max_flow:
                    if len(next_valves) > 0:
                        total_flow += curr_flow
                        minutes_remaining -= 1
                        steps += 1
                        curr_flow += sum([next_valve.rate for next_valve in next_valves])
                        for next_valve in next_valves:
                            valve_state[next_valve.name] = True
                    if minutes_remaining == 0 or sum(valve_state.values()) == len(valve_state):
                        steps = minutes_remaining
                        total_flow += curr_flow * steps
                        if total_flow > max_flow:
                            max_flow = total_flow
                            print(max_flow)
                    else:
                        if replace_me:
                            my_edges = [edge_valve for edge_valve in my_next_valve.edges if not valve_state[edge_valve[1].name]]
                        else:
                            my_edges = [(my_steps - steps, my_next_valve)]
                        for my_edge in my_edges:
                            if replace_elephant:
                                elephant_edges = [edge_valve for edge_valve in elephant_next_valve.edges if not valve_state[edge_valve[1].name]]
                            else:
                                elephant_edges = [(elephant_steps - steps, elephant_next_valve)]
                            for elephant_edge in elephant_edges:
                                if len(my_edges) == 0 and len(elephant_edges) == 0:
                                    steps = minutes_remaining
                                    minutes_remaining -= steps
                                    total_flow += curr_flow * steps
                                    if total_flow > max_flow:
                                        max_flow = total_flow
                                        print(max_flow)
                                else:
                                    queue.append((total_flow, curr_flow, valve_state.copy(), minutes_remaining, my_edge[0], my_edge[1], elephant_edge[0], elephant_edge[1]))

        print(max_flow)

g = Graph(input)
g.bfs_dfs()

# part 2

g = Graph(input)
g.bfs_dfs_2()