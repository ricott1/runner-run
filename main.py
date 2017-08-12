from runner import *
import sys, curses, time, copy


def print_state(stdscr, p, g, runners, GOAL, steps):
	stdscr.addstr(0, 0, "time {}    ".format(steps))
	for i, r in enumerate(runners):
		stdscr.addstr(i+1, 0, r.print_state() + "  :" + "|" * int(r.position) + " " * (GOAL - int(r.position)) + ":GOAL")
	stdscr.refresh()

def main():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	N = 3
	GOAL = 10
	GENERATIONS = 20
	mutation_rate = 0.3
	structure = [3 * N, 6,3, 1]
	winners = []
	TIME_OUT = 10000
	WIN_CONDITION = 0
	best = TIME_OUT
	try:
		for g in xrange(GENERATIONS):
			GOAL += 1
			pool = [[Runner(j, p, g, 1, structure) for j in xrange(N)] for p in xrange(N)]
			if winners:
				for p, runners in enumerate(pool):
					for i, r in enumerate(runners):
						runners[i].brain = copy.deepcopy(winners[i].brain)
						runners[i].id += winners[i].id
						
						runners[i].brain.mutate(mutation_rate * p / g)
			winners = []
			for p, runners in enumerate(pool):
				arrived = 0
				steps = 0
				start = time.time()
				while True:
					state = ""
					inputs = [j for i in [[r.position, r.velocity, r.energy] for r in runners] for j in i] 
					
					for r in runners:
						if not r.isArrived:
							r.update(inputs)
						if r.position >= GOAL and not r.isArrived:
							arrived += 1
							r.isArrived = arrived
					steps += 1
					print_state(stdscr, p, g, runners, GOAL, steps)
					if arrived >= 1 + WIN_CONDITION or steps > TIME_OUT:
						winner = sorted([r for r in runners], key= lambda x: x.position, reverse=True)[WIN_CONDITION]
						winners.append(winner)
						best = min(steps, best)
						break
					time.sleep(0.01)

			

			
	finally:
		curses.echo()
		curses.nocbreak()
		
		raw_input()
		curses.endwin()
		print best




if __name__ == '__main__':
	main()