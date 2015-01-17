clean:
	./pyvim.py clean -t vimrc plugins

deploy:
	./pyvim.py deploy -t vimrc pathogen wombat256 nerdcommenter ctrlp airline pythonmode

update:
	./pyvim.py deploy -t vimrc
