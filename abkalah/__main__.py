import sys
import time
import select

from abkalah.agent import Agent

agent = Agent()

while True:
  msg = sys.stdin.readline()

  if msg:
    agent.receive(msg.rstrip())

  time.sleep(0.1)

# while True:
#   input = select.select([sys.stdin], [], [], 1)[0]

#   if input:
#     msg = sys.stdin.readline().rstrip()
#     agent.receive(msg)

#   else:
#     continue
