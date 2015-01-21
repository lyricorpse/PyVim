clean:
	./pyvim.py clean -t vimrc plugins

deploy:
	./pyvim.py deploy -t vimrc pathogen wombat256 nerdcommenter ctrlp airline pythonmode snipmate nerdtree markdown ncl

update:
	./pyvim.py deploy -t vimrc
