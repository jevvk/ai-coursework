agent: clean
	mkdir -p build
	zip -r build/agent.zip abkalah/
	(cd abkalah && zip ../build/agent.zip __main__.py)

replace:
	cp build/agent.zip build/base.zip

clean:
	rm -f build/agent.zip || true

test-ref-1: agent
	java -jar game/ManKalah.jar "python3 build/agent.zip" "java -jar game/MKRefAgent.jar"

test-ref-2: agent
	java -jar game/ManKalah.jar "java -jar game/MKRefAgent.jar" "python3 build/agent.zip"

test-jimmy-1: agent
	java -jar game/ManKalah.jar "python3 build/agent.zip" "java -jar game/JimmyPlayer.jar"

test-jimmy-2: agent
	java -jar game/ManKalah.jar "java -jar game/JimmyPlayer.jar" "python3 build/agent.zip"

test-group2-1: agent
	java -jar game/ManKalah.jar "python3 build/agent.zip" "java -jar game/Group2Agent.jar"

test-group2-2: agent
	java -jar game/ManKalah.jar "java -jar game/Group2Agent.jar" "python3 build/agent.zip"

test-base-1: agent
	java -jar game/ManKalah.jar "python3 build/agent.zip" "python3 build/base.zip"

test-base-2: agent
	java -jar game/ManKalah.jar "python3 build/base.zip" "python3 build/agent.zip"

