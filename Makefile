agent: clean
	mkdir -p build
	zip -r build/agent.zip abkalah/
	(cd abkalah && zip ../build/agent.zip __main__.py)

clean:
	rm -rf build

test: agent
	java -jar game/ManKalah.jar "python -m azkalah/" "java -jar game/MKRefAgent.jar"
