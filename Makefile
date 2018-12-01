init:
  pip install -r requirements.txt

test:
	java -jar game/ManKalah.jar "python -m azkalah/" "java -jar game/MKRefAgent.jar"
