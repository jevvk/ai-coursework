import sys
import time
import select

from abkalah.agent import Agent

if __name__ == '__main__':
  agent = Agent()

  while True:
    msg = sys.stdin.readline()

    if msg:
      agent.receive(msg.rstrip())

    time.sleep(0.1)
