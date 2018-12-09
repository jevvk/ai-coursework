import sys
import select

from abkalah.agent import Agent

agent = Agent()

while True:
  input = select.select([sys.stdin], [], [], 1)[0]

  if input:
    msg = sys.stdin.readline().rstrip()

    agent.receive(msg)
  else:
    continue
